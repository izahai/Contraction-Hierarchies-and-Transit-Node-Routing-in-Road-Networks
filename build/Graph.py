from build import InputObject
import heapq
import sys
import time
import pickle
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class Graph: 
    class ShortCut:
        def __init__(self, u, v, w, ls_edge = []):
            self.fromm = u
            self.to = v
            self.weight = w
            self.ls_edge = ls_edge

    def __init__(self, list_node_id, list_edge):
        self.INF = sys.maxsize 

        self.num_node = len(list_node_id)     
        self.num_edge = len(list_edge)   
        self.list_node_id = list_node_id
        self.dict_index_stop_id = InputObject.get_list_id(list_node_id)
        self.list_edge = list_edge

        # Index 0 for upward graph, 1 for downward graph
        self.dist = [[self.INF] * self.num_node for _ in range(2)]
        self.visited = [[False] * self.num_node for _ in range(2)]
        self.ls_minHeap = [[],[]]
        
        # adj[0] for outgoing edge
        # adj[1] for incoming edge
        self.adj = [ [ [] for _ in range(self.num_node) ] for _ in range(2) ]
        self.original_adj = [ [] for _ in range(self.num_node) ]
        self.search_space = 0

        # Contraction hierarchies properties
        self.list_max_outgoing = [0] * self.num_node
        self.list_max_incoming = [0] * self.num_node

        self.pred_edge = [{} for _ in range(2)]
        self.intersect = -1
        
        self.dist_witness = [self.INF] * self.num_node
        self.bool_settled_node = [False] * self.num_node

        self.node_level_ch = [0] * self.num_node
        self.list_tmp_shortcut = []
        self.contracted_order = [self.INF] * self.num_node
        
        self.simulated_contraction = True
        self.current_contrc_node_importance = 0
        self.importance_min_heap = [(0,0) for _ in range(self.num_node)]
        self.contracted = False
        # ---

        # Transit node routing properties
        self.num_transit_node = 0
        self.num_TNR_search = 0

        self.is_transit_node = [False] * self.num_node
        self.ls_transit_node = None
        self.get_idx_tn = {}
        self.voronoi_region_id = [-1] * self.num_node
        self.transit_path = []
        self.TNRed = False

        self.forward_search_space = [{} for _ in range(self.num_node)]
        self.forward_access_node_dist = [{} for _ in range(self.num_node)]
        self.forward_TNR_ed = [False] * self.num_node
        
        self.backward_search_space = [{} for _ in range(self.num_node)]
        self.backward_access_node_dist = [{} for _ in range(self.num_node)]
        self.backward_TNR_ed = [False] * self.num_node

        for edge in list_edge:
            self.add_edge(edge)
            self.original_adj[edge[0]].append((edge[2], edge[1], edge[3]))

        print(Fore.BLUE + f" ~ Graph created with {self.num_node} nodes and {self.num_edge} edges")
    
    def reset_containers(self):
        self.dist[0] = [self.INF] * self.num_node
        self.dist[1] = [self.INF] * self.num_node
        self.visited[0] = [False] * self.num_node
        self.visited[1] = [False] * self.num_node
        self.pred_edge[0] = {}
        self.pred_edge[1] = {}
        self.intersect = -1

    def relax(self, idx_edge, weight, idx_relaxing, idx_relaxed, side):
        if self.dist[side][idx_relaxing] > self.dist[side][idx_relaxed] + weight:
            self.dist[side][idx_relaxing] = self.dist[side][idx_relaxed] + weight
            heapq.heappush(self.ls_minHeap[side], (self.dist[side][idx_relaxing], idx_relaxing))
            if side == 0:
                self.pred_edge[0][idx_relaxing] = idx_edge
            else:
                self.pred_edge[1][idx_relaxing] = idx_edge
            
    def process_node(self, idx, side):
        # Side 0 -> outgoing edges -> upward search
        # Side 1 -> incoming edges -> downward search
        for edge in self.adj[side][idx]:
            self.relax(edge[2], edge[0], edge[1], idx, side)

    def shortest_path_by_CH(self, src, tg, just_dist = False):
        self.reset_containers()
        
        src = self.dict_index_stop_id[src]
        tg = self.dict_index_stop_id[tg]

        estimate = self.INF

        self.ls_minHeap[0] = [(0, src)]
        self.ls_minHeap[1] = [(0, tg)]

        self.dist[0][src] = self.dist[1][tg] = 0
        
        need_process = True
        while self.ls_minHeap[0] or self.ls_minHeap[1]: 
            # Upward search
            if self.ls_minHeap[0]:
                dist1, u = heapq.heappop(self.ls_minHeap[0])
                self.search_space += 1
                need_process = True
                for inc_nb in self.adj[1][u]: # For each incoming neighbor 
                    if self.dist[0][inc_nb[1]] + inc_nb[0] < self.dist[0][u]:
                        need_process = False
                        break
                if self.dist[0][u] < estimate:
                    if need_process:
                        self.process_node(u, 0)
                else: 
                    self.ls_minHeap[0].clear()

                self.visited[0][u] = True

                if self.visited[1][u] and self.dist[0][u] + self.dist[1][u] < estimate:
                    estimate = self.dist[0][u] + self.dist[1][u]
                    self.intersect = u
                    #print(f"Intersect: {self.intersect} - Estimate: {estimate} - Dist1: {dist1} - Dist2: {self.dist[1][u]}")
            
            # Downward search
            if self.ls_minHeap[1]:
                dist2, u = heapq.heappop(self.ls_minHeap[1])
                self.search_space += 1
                need_process = True
                for outg_nb in self.adj[0][u]: # for each outgoing neighbor
                    if self.dist[1][outg_nb[1]] + outg_nb[0] < self.dist[1][u]:
                        need_process = False
                        break
                
                if self.dist[1][u] < estimate:
                    if need_process:
                        self.process_node(u, 1)
                else:
                    self.ls_minHeap[1].clear()

                self.visited[1][u] = True

                if self.visited[0][u] and self.dist[0][u] + self.dist[1][u] < estimate:
                    estimate = self.dist[0][u] + self.dist[1][u]
                    self.intersect = u
                    #print(f"Intersect: {self.intersect} - Estimate: {estimate} - Dist1: {self.dist[0][u]} - Dist2: {dist2}")
        
            #print(f"Estimate: {estimate} sum: {dist1+dist2} dist1: {dist1} dist2: {dist2}")
            # if dist1 + dist2 > estimate:
            #     break
        if estimate == self.INF:
            return -1, [], []
        
        if just_dist:
            return estimate, [], []
        
        stop_path, coord_path = self.trace_path(src, tg)
        return estimate, stop_path, coord_path

    def add_edge(self, edge):

        self.adj[0][edge[0]].append((edge[2], edge[1], edge[3]))
        self.adj[1][edge[1]].append((edge[2], edge[0], edge[3]))

        # Updata max, min of vertex
        if self.list_max_outgoing[edge[0]] < edge[2]:
            self.list_max_outgoing[edge[0]] = edge[2]
        if self.list_max_incoming[edge[1]] < edge[2]:
            self.list_max_incoming[edge[1]] = edge[2]

    def trace_path(self, src, tg):
        if self.intersect == -1:
            return [], []
        path_coord = []
        path_stop = []
        trace = self.intersect
        path_stop.append(self.intersect)
        
        while trace != src:
            idx_edge = self.pred_edge[0][trace]
            if isinstance(idx_edge, list):
                for idx in reversed(idx_edge):
                    edge = self.list_edge[idx]
                    path_stop.append(edge[0])
                    path_coord.append(edge[5])
                    trace = edge[0]
            else:
                edge = self.list_edge[idx_edge]
                path_stop.append(edge[0])
                path_coord.append(edge[5])
                trace = edge[0]
        
        path_stop.reverse()
        path_coord.reverse()

        trace = self.intersect
        while trace != tg:
            idx_edge = self.pred_edge[1][trace]
            if isinstance(idx_edge, list):
                for idx in (idx_edge):
                    edge = self.list_edge[idx]
                    path_stop.append(edge[1])
                    path_coord.append(edge[5])
                    trace = edge[1]
            else:
                edge = self.list_edge[idx_edge]
                path_stop.append(edge[1])
                path_coord.append(edge[5])
                trace = edge[1]
                
        return path_stop, path_coord

    # Normal Dijkstra algorithm    
    def dijkstra_2_stop(self, src, tg):
        src = self.dict_index_stop_id[src]
        tg = self.dict_index_stop_id[tg]
        
        self.dist[0] = [self.INF] * self.num_node
        self.visited[0] = [False] * self.num_node
        self.pred_edge[0] = {}

        self.ls_minHeap[0] = [(0, src)]
        self.dist[0][src] = 0

        while self.ls_minHeap[0]:
            u = heapq.heappop(self.ls_minHeap[0])[1]
            if self.visited[0][u]:
                continue
            self.search_space += 1
            self.visited[0][u] = True
            if u == tg:
                break
            for outg_edge in self.original_adj[u]:
                if self.dist[0][outg_edge[1]] > self.dist[0][u] + outg_edge[0]:
                    self.dist[0][outg_edge[1]] = self.dist[0][u] + outg_edge[0]
                    heapq.heappush(self.ls_minHeap[0], (self.dist[0][outg_edge[1]], outg_edge[1]))
                    self.pred_edge[0][outg_edge[1]] = outg_edge[2]               
         
        path_stop = []
        path_coord = []
        trace = tg

        if self.dist[0][tg] != self.INF:
            path_stop.append(trace)
            while trace != src:
                idx_edge = self.pred_edge[0][trace] 
                edge = self.list_edge[idx_edge]
                path_stop.append(edge[0])
                path_coord.append(edge[5])
                trace = edge[0]
            path_stop.reverse()
            path_coord.reverse()

        if self.dist[0][tg] == self.INF:
            return -1, [], []
        return self.dist[0][tg], path_stop, path_coord

    def output_edge(self):
        with open('output/outputEdge.txt', 'w') as f:
            for i in range(len(self.adj[0])):
                for edge in self.adj[0][i]:
                    f.write(f"{i} {edge[1]} {edge[0]} {edge[2]}\n")

    # Contraction hierarchies algorithm
    def update_neighbors_node_level_ch(self, idx_node):
        outgoing_edges = self.adj[0][idx_node]
        incoming_edges = self.adj[1][idx_node]

        current_node_level = self.node_level_ch[idx_node] + 1

        for nb in outgoing_edges:
            if self.node_level_ch[nb[1]] < current_node_level:
                self.node_level_ch[nb[1]] = current_node_level
        for nb in incoming_edges:
            if self.node_level_ch[nb[1]] < current_node_level:
                self.node_level_ch[nb[1]] = current_node_level

    def sum_contracted_neighbors_and_node_level(self, idx_node):
        num_contracted_neighbors = 0
        current_level = 0

        outgoing_edges = self.adj[0][idx_node]
        incoming_edges = self.adj[1][idx_node]

        for outg_edge in outgoing_edges:
            if self.contracted_order[outg_edge[1]] != self.INF:
                num_contracted_neighbors += 1
                if self.node_level_ch[outg_edge[1]] > current_level:
                    current_level = self.node_level_ch[outg_edge[1]]

        for inc_edge in incoming_edges:
            if self.contracted_order[inc_edge[1]] != self.INF:
                num_contracted_neighbors += 1
                if self.node_level_ch[inc_edge[1]] > current_level:
                    current_level = self.node_level_ch[inc_edge[1]]
        
        return num_contracted_neighbors + current_level + 1
    
    def witness_search(self, source, contr_node, limit):    
        queue = []
        queue.append((0, source))
        #self.settled_node.append(source)
        self.dist_witness[source] = 0

        #hops = 10000
        while queue: #and hops > 0:
            #hops -= 1
            _, u = heapq.heappop(queue)
            
            if self.bool_settled_node[u]:
                continue
            self.bool_settled_node[u] = True
            if limit < self.dist_witness[u]:
                break

            outgoing_edges = self.adj[0][u]     

            for outg_edge in outgoing_edges:
                if self.contracted_order[outg_edge[1]] < self.contracted_order[contr_node] or outg_edge[1] == contr_node:
                    continue
                if self.dist_witness[outg_edge[1]] > self.dist_witness[u] + outg_edge[0]:
                    self.dist_witness[outg_edge[1]] = self.dist_witness[u] + outg_edge[0]
                    heapq.heappush(queue, (self.dist_witness[outg_edge[1]], outg_edge[1]))
        return
    
    def contract_node(self, contr_node):
        self.list_tmp_shortcut.clear()
        
        added_shortcut = 0
        shortcut_cover = 0

        outgoing_edges = self.adj[0][contr_node]
        incoming_edges = self.adj[1][contr_node]

        for inc_edge in incoming_edges:
            if self.contracted_order[inc_edge[1]] < self.contracted_order[contr_node] or not outgoing_edges:
                continue
            self.witness_search(inc_edge[1], contr_node, self.list_max_outgoing[contr_node] + self.list_max_incoming[contr_node])
            
            at_least_one_shortcut = False

            for outg_edge in outgoing_edges:
                if self.contracted_order[outg_edge[1]] < self.contracted_order[contr_node] or outg_edge[1] == inc_edge[1]:
                    continue
                
                is_shortcut_needed = True
                
                if self.dist_witness[outg_edge[1]] <= inc_edge[0] + outg_edge[0]:
                    is_shortcut_needed = False

                already_added_shortcut = False
                for idx in range(len(self.list_tmp_shortcut)):
                    if self.list_tmp_shortcut[idx].fromm == inc_edge[1] and self.list_tmp_shortcut[idx].to == outg_edge[1]: 
                        if self.list_tmp_shortcut[idx].weight > inc_edge[0] + outg_edge[0]:
                            self.list_tmp_shortcut[idx].weight = inc_edge[0] + outg_edge[0]
                            ls_edge =  []
                            if isinstance(inc_edge[2], list):
                                ls_edge = inc_edge[2].copy()
                            else:
                                ls_edge.append(inc_edge[2])
                            if isinstance(outg_edge[2], list):
                                ls_edge += outg_edge[2].copy()
                            else:
                                ls_edge.append(outg_edge[2])
                            self.list_tmp_shortcut[idx].ls_edge = ls_edge
                        already_added_shortcut = True
                        break
                    
                if is_shortcut_needed:
                    added_shortcut += 1
                    at_least_one_shortcut = True
                    if not self.simulated_contraction and not already_added_shortcut:
                        ls_edge =  []
                        if isinstance(inc_edge[2], list):
                            ls_edge = inc_edge[2].copy()
                        else:
                            ls_edge.append(inc_edge[2])
                        if isinstance(outg_edge[2], list):
                            ls_edge += outg_edge[2].copy()
                        else:
                            ls_edge.append(outg_edge[2])
                        self.list_tmp_shortcut.append(self.ShortCut(inc_edge[1], outg_edge[1], inc_edge[0] + outg_edge[0], ls_edge))
        
            if at_least_one_shortcut:
                shortcut_cover += 1
            
            self.dist_witness = [self.INF] * self.num_node
            self.bool_settled_node =[False] * self.num_node

        self.current_contrc_node_importance = (
            added_shortcut - len(outgoing_edges) - len(incoming_edges)
            + shortcut_cover + self.sum_contracted_neighbors_and_node_level(contr_node)
        )
        return
    
    def initialize_nodes_important_min_heap(self):
        for v in range(self.num_node):
            self.contract_node(v)
            self.importance_min_heap[v] = (self.current_contrc_node_importance, v)
        heapq.heapify(self.importance_min_heap)     

    def build_ch_graph(self):
        print("<--------------------------------------------------------->")
        print("    ---> Build contraction hierarchies graph(CH) ... ")
        start = time.time()
        
        self.initialize_nodes_important_min_heap()
        init_time = (time.time() - start) * 1000
        print(f"        ---> Initialize raw nodes importance order: {init_time} ms")
        
        self.simulated_contraction = False
        i = 0
        while self.importance_min_heap:
            _, contr_node = heapq.heappop(self.importance_min_heap)
            self.contract_node(contr_node)
            if not self.importance_min_heap or self.current_contrc_node_importance <= self.importance_min_heap[0][0]:
                for shortcut in self.list_tmp_shortcut:
                    edge = (shortcut.fromm, shortcut.to, shortcut.weight, shortcut.ls_edge)
                    self.add_edge(edge)
                self.update_neighbors_node_level_ch(contr_node)
                self.contracted_order[contr_node] = i
                i += 1  
            else:
                heapq.heappush(self.importance_min_heap, (self.current_contrc_node_importance, contr_node))
        self.contracted = True

        total_time = (time.time() - start) * 1000
        print(f"        ---> Contract graph & create shortcuts: {total_time - init_time} ms")

        new_num_edge = 0
        for i in range(self.num_node):
            new_num_edge += len(self.adj[0][i])
        print(Fore.MAGENTA + f" ~ Total preprocess CH: {total_time} ms")
        print(Fore.YELLOW + f" ~ Number of shortcut created: {new_num_edge - self.num_edge} edges")

        self.num_edge = new_num_edge
        
    # Transit node routing algorithm
    def get_forward_path_local_TNR(self, forward_path, goal):
        stop_path = []
        coord_path = []
        
        trace = goal
        idx_edge = forward_path[trace]
        while idx_edge != -1:
            if isinstance(idx_edge, list):
                for idx in reversed(idx_edge):
                    edge = self.list_edge[idx]
                    stop_path.append(edge[0])
                    coord_path.append(edge[5])
                    trace = edge[0]
            else:
                edge = self.list_edge[idx_edge]
                stop_path.append(edge[0])
                coord_path.append(edge[5])
                trace = edge[0]
            idx_edge = forward_path[trace]
        
        stop_path.reverse()
        coord_path.reverse()
        return stop_path, coord_path

    def get_backward_path_local_TNR(self, backward_path, goal):
        stop_path = []
        coord_path = []
        
        trace = goal
        idx_edge = backward_path[trace]
        while idx_edge != -1:
            if isinstance(idx_edge, list):
                for idx in idx_edge:
                    edge = self.list_edge[idx]
                    stop_path.append(edge[1])
                    coord_path.append(edge[5])
                    trace = edge[1]
            else:
                edge = self.list_edge[idx_edge]
                stop_path.append(edge[1])
                coord_path.append(edge[5])
                trace = edge[1]
            idx_edge = backward_path[trace]
        
        return stop_path, coord_path
    
    def compute_TNR(self, num_transit_node : int):
        start = time.time()
        if not self.contracted:
            print("\nError: The graph has not contracted, run build contraction hierarchy graph first.")
            return
        if self.TNRed:
            print("\nError: The graph has already calculated transit node routing (TNR)")
            return
        if self.num_node < num_transit_node:
            print("\nError: The num of transit node must be less than the num of node in the graph")
            return
        
        print("<--------------------------------------------------------->")
        print(f"    ---> Compute(TNR) for {num_transit_node} transit nodes...")
        self.num_transit_node = num_transit_node
        self.ls_transit_node = [int] * num_transit_node 
        
        self.select_transit_node()        
        self.compute_voronoi_region()
        self.remove_redundant_edge_access()
        self.compute_dis_all_TN()
        self.compute_local_filter()

        self.TNRed = True
        print(Fore.MAGENTA + f" ~ Total preprocess Transit Node Routing(TNR): {time.time() - start} seconds")
        
    def select_transit_node(self):
        important_order = self.num_node - self.num_transit_node
        u = 0
        for i in range(self.num_node):
            if (self.contracted_order[i] >= important_order):
                self.is_transit_node[i] = True
                self.ls_transit_node[u] = i
                self.get_idx_tn[i] = u
                u += 1

    def compute_dis_all_TN(self):
        start_d = time.time()
        self.transit_path = [[[] for _ in range(self.num_transit_node)] for _ in range(self.num_transit_node)]
        for idx1 in self.ls_transit_node:
            for idx2 in self.ls_transit_node:
                tn1 = self.get_idx_tn[idx1]
                tn2 = self.get_idx_tn[idx2]
                if idx1 == idx2:
                    self.transit_path[tn1][tn2] = (0, [idx1], [])
                    continue
                stop_id_1 = self.list_node_id[idx1]
                stop_id_2 = self.list_node_id[idx2]
                dis, path_stop, path_coord = self.shortest_path_by_CH(stop_id_1, stop_id_2)
                
                self.transit_path[tn1][tn2] = (dis, path_stop, path_coord)
        print(f"        ---> Compute many-to-many transit node distance: {(time.time() - start_d)*1000} ms")
                
    def compute_voronoi_region(self):
        start_v = time.time()
        voronoi_dist = [self.INF] * self.num_node
        voronoi_visited = [False] * self.num_node
        voronoi_minHeap = []
        for idx in self.ls_transit_node:
            voronoi_minHeap.append((0, idx))
            voronoi_dist[idx] = 0
            self.voronoi_region_id[idx] = idx
        
        while voronoi_minHeap:
            vertex = heapq.heappop(voronoi_minHeap)[1]
            if voronoi_visited[vertex]:
                continue
            voronoi_visited[vertex] = True
            for inc_edge in self.adj[1][vertex]:
                if not isinstance(inc_edge[2], list): # Check the edge is not a shortcut
                    if voronoi_dist[inc_edge[1]] > voronoi_dist[vertex] + inc_edge[0]:
                        voronoi_dist[inc_edge[1]] = voronoi_dist[vertex] + inc_edge[0]
                        heapq.heappush(voronoi_minHeap, (voronoi_dist[inc_edge[1]], inc_edge[1]))
                        self.voronoi_region_id[inc_edge[1]] = self.voronoi_region_id[vertex]
            
            # for og_edge in self.adj[0][vertex]:
            #     if not isinstance(og_edge[2], list):
            #         if voronoi_dist[og_edge[1]] > voronoi_dist[vertex] + og_edge[0]:
            #             voronoi_dist[og_edge[1]] = voronoi_dist[vertex] + og_edge[0]
            #             heapq.heappush(voronoi_minHeap, (voronoi_dist[og_edge[1]], og_edge[1]))
            #             self.voronoi_region_id[og_edge[1]] = self.voronoi_region_id[vertex]
        self.compute_voronoi_region_2()
        print(f"        ---> Divide voronoi region: {(time.time() - start_v)*1000} ms")

    def compute_voronoi_region_2(self):
        start_v = time.time()
        voronoi_dist = [self.INF] * self.num_node
        voronoi_visited = [False] * self.num_node
        voronoi_minHeap = []
        for idx in self.ls_transit_node:
            voronoi_minHeap.append((0, idx))
            voronoi_dist[idx] = 0
            self.voronoi_region_id[idx] = idx
        
        while voronoi_minHeap:
            vertex = heapq.heappop(voronoi_minHeap)[1]
            if voronoi_visited[vertex]:
                continue
            voronoi_visited[vertex] = True
            for og_edge in self.adj[0][vertex]:
                if not isinstance(og_edge[2], list):
                    if voronoi_dist[og_edge[1]] > voronoi_dist[vertex] + og_edge[0]:
                        voronoi_dist[og_edge[1]] = voronoi_dist[vertex] + og_edge[0]
                        heapq.heappush(voronoi_minHeap, (voronoi_dist[og_edge[1]], og_edge[1]))
                        self.voronoi_region_id[og_edge[1]] = self.voronoi_region_id[vertex]
    
    def compute_local_filter(self):
        start = time.time()
        contraction_max_heap = []
        
        for i in range(self.num_node):
            heapq.heappush(contraction_max_heap, (-self.contracted_order[i], i))

        while contraction_max_heap:
            src = heapq.heappop(contraction_max_heap)[1]

            if not self.forward_TNR_ed[src]:
                search_heap = []
                heapq.heappush(search_heap, (0, src))
                dist_search = [self.INF] * self.num_node
                dist_search[src] = 0

                while search_heap:
                    query_node = heapq.heappop(search_heap)[1]

                    if not self.is_transit_node[query_node]:
                        self.forward_search_space[src][self.voronoi_region_id[query_node]] = True
                        
                        if self.forward_TNR_ed[query_node]:
                            for voronoid_id in self.forward_search_space[query_node].keys():
                                self.forward_search_space[src][voronoid_id] = True
                            for access_node in self.forward_access_node_dist[query_node].keys():
                                self.forward_access_node_dist[src][access_node] = -1
                        else:
                            for outgoing_edge in self.adj[0][query_node]:
                                if dist_search[outgoing_edge[1]] > dist_search[query_node] + outgoing_edge[0]:
                                    dist_search[outgoing_edge[1]] = dist_search[query_node] + outgoing_edge[0]
                                    heapq.heappush(search_heap, (dist_search[outgoing_edge[1]], outgoing_edge[1]))
                    else:
                        self.forward_access_node_dist[src][query_node] = -1

                for access_node in self.forward_access_node_dist[src].keys():
                    stop_id_1 = self.list_node_id[src]
                    stop_id_2 = self.list_node_id[access_node]
                    self.forward_access_node_dist[src][access_node], _, _ = self.shortest_path_by_CH(stop_id_1, stop_id_2, just_dist=True)
                
                access_node_mask = {}
                for ac1, d1 in self.forward_access_node_dist[src].items():
                    for ac2, d2 in self.forward_access_node_dist[src].items():
                        if ac1 == ac2:
                            continue
                        tn1 = self.get_idx_tn[ac1]
                        tn2 = self.get_idx_tn[ac2]
                        if d1 + self.transit_path[tn1][tn2][0] <= d2:
                            access_node_mask[ac2] = True
                
                for ac in access_node_mask.keys():
                    del self.forward_access_node_dist[src][ac]
                
                self.forward_TNR_ed[src] = True
            
            if not self.backward_TNR_ed[src]:
                search_heap = []
                heapq.heappush(search_heap, (0, src))
                dist_search = [self.INF] * self.num_node
                dist_search[src] = 0

                while search_heap:
                    query_node = heapq.heappop(search_heap)[1]

                    if not self.is_transit_node[query_node]:
                        self.backward_search_space[src][self.voronoi_region_id[query_node]] = True
                        
                        if self.backward_TNR_ed[query_node]:
                            for voronoid_id in self.backward_search_space[query_node].keys():
                                self.backward_search_space[src][voronoid_id] = True
                            for access_node in self.backward_access_node_dist[query_node].keys():
                                self.backward_access_node_dist[src][access_node] = -1
                        else:
                            for incoming_edge in self.adj[1][query_node]:
                                if dist_search[incoming_edge[1]] > dist_search[query_node] + incoming_edge[0]:
                                    dist_search[incoming_edge[1]] = dist_search[query_node] + incoming_edge[0]
                                    heapq.heappush(search_heap, (dist_search[incoming_edge[1]], incoming_edge[1]))
                    else:
                        self.backward_access_node_dist[src][query_node] = -1
                
                for access_node in self.backward_access_node_dist[src].keys():
                    stop_id_1 = self.list_node_id[src]
                    stop_id_2 = self.list_node_id[access_node]
                    self.backward_access_node_dist[src][access_node], _, _ = self.shortest_path_by_CH(stop_id_2, stop_id_1, just_dist=True)
                
                access_node_mask = {}
                for ac1, d1 in self.backward_access_node_dist[src].items():
                    for ac2, d2 in self.backward_access_node_dist[src].items():
                        if ac1 == ac2:
                            continue
                        tn1 = self.get_idx_tn[ac1]
                        tn2 = self.get_idx_tn[ac2]
                        #if d1 + self.tnr_dis[ac1][ac2] <= d2: Stupid mistake I made
                        if d1 + self.transit_path[tn2][tn1][0] <= d2:
                            access_node_mask[ac2] = True

                for ac in access_node_mask.keys():
                    del self.backward_access_node_dist[src][ac]
                
                self.backward_TNR_ed[src] = True
        print(f"        ---> Compute local filter: {(time.time() - start)*1000} ms")

    def shortest_path_TNR_with_CH(self, src, tg):
        id_src = src
        id_tg = tg
        src = self.dict_index_stop_id[src]
        tg = self.dict_index_stop_id[tg]
        if not self.TNRed:
            print("The graph has not calculated transit node routing (TNR)")
            return self.shortest_path_by_CH(id_src, id_tg)
        
        # Check for local search
        if len(self.forward_access_node_dist[src]) == 0 or len(self.backward_access_node_dist[tg]) == 0:
            return self.shortest_path_by_CH(id_src, id_tg)
        
        # Check for local search
        for voronoid_1 in self.forward_search_space[src].keys():
            if voronoid_1 in self.backward_search_space[tg].keys():
                return self.shortest_path_by_CH(id_src, id_tg)
            
        # Distance is far enough to use transit node routing
        self.num_TNR_search += 1
        best_dist = self.INF
        final_stop_path = []
        final_coord_path = []
        best_src_access_node = None
        best_tg_access_node = None
        
        # Look up precomputed distance and find best distance and 2 access nodes
        for ac1, d1 in self.forward_access_node_dist[src].items():
            for ac2, d2 in self.backward_access_node_dist[tg].items():
                tn1 = self.get_idx_tn[ac1]
                tn2 = self.get_idx_tn[ac2]
                if self.transit_path[tn1][tn2][0] == -1:
                    continue
                if best_dist > d1 + self.transit_path[tn1][tn2][0] + d2:
                    best_dist = d1 + self.transit_path[tn1][tn2][0] + d2
                    best_src_access_node = ac1
                    best_tg_access_node = ac2
        
        if best_dist == self.INF:
            return self.shortest_path_by_CH(id_src, id_tg)
        
        # Trace back to get the local path
        forward_dist =  [self.INF] * self.num_node
        backward_dist = [self.INF] * self.num_node
        forward_dist[src] = 0
        backward_dist[tg] = 0
        forward_search_heap = [(0, src)]
        backward_search_heap = [(0, tg)]
        forward_backtrace = {}
        backward_backtrace = {}

        forward_backtrace[src] = -1
        backward_backtrace[tg] = -1
        # Get forward path
        while forward_search_heap:
            query_node = heapq.heappop(forward_search_heap)[1]
            self.search_space += 1
            if forward_dist[query_node] <= self.INF:
                if query_node == best_src_access_node:
                    break

            for og_edge in self.adj[0][query_node]:
                if forward_dist[og_edge[1]] > forward_dist[query_node] + og_edge[0]:
                    forward_dist[og_edge[1]] = forward_dist[query_node] + og_edge[0]
                    heapq.heappush(forward_search_heap, (forward_dist[og_edge[1]], og_edge[1]))
                    forward_backtrace[og_edge[1]] = og_edge[2]

        # Get backward path         
        while backward_search_heap:
            query_node = heapq.heappop(backward_search_heap)[1]
            self.search_space += 1
            if backward_dist[query_node] <= self.INF:
                if query_node == best_tg_access_node:
                    break

            for in_edge in self.adj[1][query_node]:
                #if self.contracted_order[query_node] < self.contracted_order[in_edge[1]]:
                if backward_dist[in_edge[1]] > backward_dist[query_node] + in_edge[0]:
                    backward_dist[in_edge[1]] = backward_dist[query_node] + in_edge[0]
                    heapq.heappush(backward_search_heap, (backward_dist[in_edge[1]], in_edge[1]))
                    backward_backtrace[in_edge[1]] = in_edge[2]
        
        # Merge forward path + transit node path + backward path
        forward_stop_path, forward_coord_path = self.get_forward_path_local_TNR(forward_backtrace, best_src_access_node)
        backward_stop_path, backward_coord_path = self.get_backward_path_local_TNR(backward_backtrace, best_tg_access_node)
        final_stop_path = forward_stop_path + self.transit_path[self.get_idx_tn[best_src_access_node]][self.get_idx_tn[best_tg_access_node]][1] + backward_stop_path
        final_coord_path = forward_coord_path + self.transit_path[self.get_idx_tn[best_src_access_node]][self.get_idx_tn[best_tg_access_node]][2] + backward_coord_path
        
        return best_dist, final_stop_path, final_coord_path

    def remove_redundant_edge_access(self):        
        start_r = time.time()
        for i in range(self.num_node):
            # When call in or out edges -> we just get the edge connect to the higher order node in the graph
            for j in range(len(self.adj[0][i]) - 1, -1, -1):
                if self.contracted_order[i] > self.contracted_order[self.adj[0][i][j][1]]:
                    self.adj[0][i].pop(j) 
            for j in range(len(self.adj[1][i]) - 1, -1, -1):
                if self.contracted_order[i] > self.contracted_order[self.adj[1][i][j][1]]:
                    self.adj[1][i].pop(j)
        print(f"        ---> Remove redundant edge access in adj list: {(time.time() - start_r)*1000} ms")

    def save_CH_graph_to_disk(self):
        data_to_save = {
                'adj' : self.adj,
                'contracted_order' : self.contracted_order,
        }   
        with open('storage/CH_graph.bin', 'wb') as f:
            pickle.dump(data_to_save, f)
        print(Fore.GREEN + " ~ Save CH graph to disk successfully")
    
    def save_TNR_graph_to_disk(self):
        data_to_save = {
            'num_transit_node' : self.num_transit_node,
            'ls_transit_node' : self.ls_transit_node,
            'get_idx_tn' : self.get_idx_tn,
            'voronoi_region_id' : self.voronoi_region_id,
            'transit_path' : self.transit_path,
            
            'forward_search_space' : self.forward_search_space,
            'forward_access_node_dist' : self.forward_access_node_dist,

            'backward_search_space' : self.backward_search_space,
            'backward_access_node_dist' : self.backward_access_node_dist,
        }
        with open('storage/TNR_graph.bin', 'wb') as f:
            pickle.dump(data_to_save, f)
        print(Fore.GREEN + " ~ Save TNR graph to disk successfully")

    def load_CH_graph_from_disk(self):
        if self.contracted:
            print(Fore.RED + " ~ The graph has already contracted")
            return
        with open('storage/CH_graph.bin', 'rb') as f:
            data = pickle.load(f)
            self.adj = data['adj']
            self.contracted_order = data['contracted_order']
        self.contracted = True
        print(Fore.GREEN + " ~ Load CH graph from disk successfully")

    def load_TNR_graph_from_disk(self):
        self.remove_redundant_edge_access()
        if self.TNRed:
            print(Fore.RED + " ~ The graph has already calculated transit node routing (TNR)")
            return
        with open('storage/TNR_graph.bin', 'rb') as f:
            data = pickle.load(f)
            self.num_transit_node = data['num_transit_node']
            self.ls_transit_node = data['ls_transit_node']
            self.get_idx_tn = data['get_idx_tn']
            self.voronoi_region_id = data['voronoi_region_id']
            self.transit_path = data['transit_path']
            self.forward_search_space = data['forward_search_space']
            self.forward_access_node_dist = data['forward_access_node_dist']
            self.backward_search_space = data['backward_search_space']
            self.backward_access_node_dist = data['backward_access_node_dist']
        self.TNRed = True
        print(Fore.GREEN + " ~ Load TNR graph from disk successfully")
    
