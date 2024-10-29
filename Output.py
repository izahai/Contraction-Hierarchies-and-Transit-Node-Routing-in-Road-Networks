from build.Graph import Graph
from colorama import Fore, Back, Style, init
import time

init(autoreset=True)

class Output:
    def __init__(self, file_test : str, graph : Graph):
        self.graph = graph
        self.num_test = None
        self.test_case = None

        with open("test.txt", 'r') as f:
            self.num_test = f.readline()
            self.num_test = int(self.num_test)
            self.test_case = [(0,0) for _ in range(self.num_test)]
            i = 0
            for line in f:
                self.test_case[i] = tuple(map(int, line.split()))
                i += 1
        
        self.ans_CH = [(0,0,0,[],[]) for _ in range(self.num_test)]
        self.ans_TNR = [(0,0,0,[],[]) for _ in range(self.num_test)]
        self.ans_dijkstra = [(0,0,0,[],[]) for _ in range(self.num_test)]

    def query_testcase_dijkstra(self):
        print("<--------------------------------------------------------->")
        print("Query using Dijkstra...")
        start = time.time()
        self.graph.search_space = 0 # Reset search space
        for i in range(self.num_test):
            d, path_stop, path_coord = self.graph.dijkstra_2_stop(self.test_case[i][0], self.test_case[i][1])
            self.ans_dijkstra[i] = (self.test_case[i][0], self.test_case[i][1], d, path_stop, path_coord)
        total = time.time() - start
        print(Fore.CYAN + f" ~ Total query dijkstra: {total} seconds")
        print(f" ~ Dijkstra second per query: {total*1000/self.num_test} ms")
        print(f" ~ Total dijkstra search space: {self.graph.search_space} vertices")
        print(f" ~ Avg dijkstra search space per query: {self.graph.search_space / self.num_test} vertices")

    def query_testcase_CH(self):
        print("<--------------------------------------------------------->")
        print("Query using contraction hierarchies(CH)...")
        start = time.time()
        self.graph.search_space = 0
        for i in range(self.num_test):
            d, path_stop, path_coord = self.graph.shortest_path_by_CH(self.test_case[i][0], self.test_case[i][1])
            self.ans_CH[i] = (self.test_case[i][0], self.test_case[i][1], d, path_stop, path_coord)
        total = time.time() - start
        print(Fore.CYAN + f" ~ Total query CH: {total} seconds")
        print(f" ~ CH second per query: {total*1000/self.num_test} ms")
        print(f" ~ Total CH search space: {self.graph.search_space} vertices")
        print(f" ~ Avg CH search space per query: {self.graph.search_space / self.num_test} vertices")  
    
    def query_testcase_TNR(self):
        print("<--------------------------------------------------------->")
        print("Query using transit node routing(TNR) with CH...")
        self.graph.search_space = 0
        start = time.time()
        for i in range(self.num_test):
            d, path_stop, path_coord = self.graph.shortest_path_TNR_with_CH(self.test_case[i][0], self.test_case[i][1])
            self.ans_TNR[i] = (self.test_case[i][0], self.test_case[i][1], d, path_stop, path_coord)
        total = time.time() - start
        print(Fore.CYAN + f" ~ Total query TNR+CH: {total} seconds")
        print(f" ~ TNR second per query: {total*1000/self.num_test} ms")
        print(f" ~ Total TNR+CH search space: {self.graph.search_space} vertices")
        print(f" ~ Avg TNR+CH search space per query: {self.graph.search_space / self.num_test} vertices")
        print(Fore.YELLOW + f" ~ Search by TNR: {self.graph.num_TNR_search}/{self.num_test} queries")
        print(f" ~ Search by local search(CH): {self.num_test - self.graph.num_TNR_search}/{self.num_test} queries")

    def write_output(self, file_output : str, ans : list):
        with open(file_output, 'w') as f:
            for i in range(self.num_test):
                f.write(f"{ans[i][0]} {ans[i][1]} {ans[i][2]} {ans[i][3]} {ans[i][4]}\n")

    def compare_all_kind_of_search_algorithm(self):
        self.query_testcase_CH()
        self.query_testcase_TNR()
        self.query_testcase_dijkstra()

        print("<--------------------------------------------------------->")
        num_diff = self.check_ans(self.ans_CH, self.ans_dijkstra)
        if num_diff == 0:
            print(Fore.GREEN + f" ~ :) Dijkstra and CH pass: {self.num_test}/{self.num_test}")
        else:
            print(f" ~ :( Dijkstra and CH pass: {self.num_test - num_diff}/{self.num_test}")
        num_diff = self.check_ans(self.ans_TNR, self.ans_dijkstra)
        if num_diff == 0:
            print(Fore.GREEN + f" ~ :) Dijkstra and TNR pass: {self.num_test}/{self.num_test}")
        else:
            print(f" ~ :( Dijkstra and TNR pass: {self.num_test - num_diff}/{self.num_test}")

        print("\nWriting output to file...")
        self.write_output("output/outputCH.txt", self.ans_CH)
        self.write_output("output/outputCH_TNR.txt", self.ans_TNR)
        self.write_output("output/outputDijkstra.txt", self.ans_dijkstra)
        print(" ~ :) Done")

    def check_ans(self, ans1 : list, ans2 : list):
        num_diff = 0
        for i in range(len(ans1)):
            if ans1[i][0] != ans2[i][0] or ans1[i][1] != ans2[i][1] or ans1[i][2] != ans2[i][2] or ans1[i][3] != ans2[i][3]:
                print(f" ~ :( Test case {i+1} is different")
                num_diff += 1
        return num_diff