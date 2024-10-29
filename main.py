from build import InputObject
from build.Graph import Graph
import time
from Output import Output

def main():
    list_route_var = InputObject.read_route_var()
    list_path = InputObject.read_path()
    list_stop = InputObject.read_stop()
    list_stop_id = InputObject.compress_stop_id(list_stop)
    dict_index_stop_id = InputObject.get_list_id(list_stop_id)

    # Build edge from raw data
    #list_edge = InputObject.read_edge_from_route_var(list_route_var, list_stop, list_path, dict_index_stop_id)
    # Or build edge from refinded data
    list_edge = InputObject.read_edge_from_file("storage/edge.txt")

    graph = Graph(list_stop_id, list_edge)
    
    graph.build_ch_graph() # Preprocess contraction hierarchies
    graph.save_CH_graph_to_disk() # Save CH to disk (if needed)

    #graph.load_CH_graph_from_disk() # Or preload file CH from disk
    
    graph.compute_TNR(100) # Preprocess transit node routing
    graph.save_TNR_graph_to_disk() # Save TNR to disk (if needed)
    
    #graph.load_TNR_graph_from_disk() # Or preload file TNR from disk
   
    output = Output("test.txt", graph)
    output.compare_all_kind_of_search_algorithm()

main()