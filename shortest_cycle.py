import argparse
import sys
from collections import defaultdict
import heapq

class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = defaultdict(list)
    
    def add_edge(self, source, destination, weight):
        self.vertices.add(source)
        self.vertices.add(destination)
        self.edges[source].append((destination, weight))
    
    # Describing the structure of testcase files
    def parse_graph_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(':')
                    if len(parts) != 2:
                        raise ValueError(f"Oops! Invalid line format: {line}")
                    
                    source = int(parts[0].strip())
                    destinations = parts[1].strip().split()
                    
                    if len(destinations) % 2 != 0:
                        raise ValueError(f"Sorry! Invalid destination format: {parts[1]}")
                    
                    for i in range(0, len(destinations), 2):
                        destination = int(destinations[i])
                        weight = int(destinations[i + 1])
                        self.add_edge(source, destination, weight)
        except FileNotFoundError:
            print(f"Error: File named {file_path} not found.")
            sys.exit(1)
        except (ValueError, IndexError) as e:
            print(f"Error parsing the file: {e}")
            sys.exit(1)

    def dijkstra(self, source):
        
      #  Running Dijkstra's algorithm from source vertex
      #  Returns a dictionary of shortest distances to each vertex
    
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[source] = 0
        priority_queue = [(0, source)]
        
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            
            # If we've found a shorter path already, skip
            if current_distance > distances[current_vertex]:
                continue
            
            # Check all neighbors
            for neighbor, weight in self.edges[current_vertex]:
                distance = current_distance + weight
                
                # If we found a shorter path to the neighbor
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances

    def find_shortest_cycle(self):
        """
        Find the shortest cycle in the directed graph
        """
        # Initialize minimum cycle length to infinity
        min_cycle_length = float('infinity')
        
        # For each vertex, try to find the shortest cycle going through it
        for vertex in self.vertices:
            # For each outgoing edge (vertex, neighbor)
            for neighbor, edge_weight in self.edges[vertex]:
                # Remove this edge temporarily
                self.edges[vertex].remove((neighbor, edge_weight))
                
                # Run Dijkstra from the neighbor to find shortest path back to vertex
                distances = self.dijkstra(neighbor)
                
                # If there's a path back to vertex, we have a cycle
                if distances[vertex] != float('infinity'):
                    cycle_length = edge_weight + distances[vertex]
                    min_cycle_length = min(min_cycle_length, cycle_length)
                
                # Put the edge back
                self.edges[vertex].append((neighbor, edge_weight))
        
        # If no cycle is found
        if min_cycle_length == float('infinity'):
            return 0
        
        return min_cycle_length

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Find the shortest cycle in a directed graph.')
    parser.add_argument('--input', required=True, help='Input graph file')
    args = parser.parse_args()
    
    # Create graph and parse from file
    graph = Graph()
    try:
        graph.parse_graph_from_file(args.input)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Find shortest cycle
    shortest_cycle_length = graph.find_shortest_cycle()
    
    # Print output
    if shortest_cycle_length == 0:
        print("The length of the shortest cycle is: 0")
    else:
        print(f"The length of the shortest cycle is: {shortest_cycle_length}")

if __name__ == "__main__":
    main()