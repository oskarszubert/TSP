class DynamicTsp:
    def __init__(self):
        self.best_cost = -1
        self.best_path = []
        self.graph = []
        self.number_of_vertices = 0
        self.npow = 0
        self.g = []
        self.p = []

    def __repr__(self):
        if self.best_cost == -1:
            return "BrutForce object. Not used yet."
        return "BrutForce object. Minimal cost path: {}. Best path: {}".format(self.best_cost, self.best_path)

    def dynamic(self, graph):

        self.graph = graph
        self.number_of_vertices = len(graph[0])
        self.npow = 1 << self.number_of_vertices

        # create ancillary graphs for storing:  
        # q- cost of partial tour
        # p- visited nodes, backtracing when getting path
        # -1 in evry cell in this graphs(matrices) coz we do not visited any of verrtacity ye

        # both ancillary graphs has to be [2**n][n] coz we have n- vertices and 2**n subset of this vertices 
        self.g=[[-1 for city in range(self.npow)] for y in range(self.number_of_vertices) ]
        self.p=[[-1 for city in range(self.npow)] for y in range(self.number_of_vertices) ]

        # initzialize first [row][0] = graph[row][0] coz we know that possible first conetion is from first element(in this case 0) to the rest of vetrices
        # and we know this cost from just reading from graph

        for i in range(self.number_of_vertices):
            self.g[i][0] = self.graph[i][0]

        self.best_cost = self.compute_dynamic(0, self.npow - 2) # start from 0 and gonna compute 2**n -2 coz we have to check all of subset excluding 0 and last ex. {empty}{1}{2}{3}{1,2}{1,3}{2,3}{1,2,3} 
        
        self.best_path.append(0)
        self.get_path(0, self.npow - 2) # same as self.best_cost

        return self.best_cost

    def print(self):
        if len(self.best_path) == 0:
            print('Do not found best path yet')
        else: 
            print('Minimal cost path: {}. \nBest path with Dynamic Programming for TSP: '.format(self.best_cost))
            print("\tPath: ",end = '')
            for vertecity in self.best_path:
                print('{} \u2192 '.format(vertecity), end='')
            print(self.best_path[0])


# bitmask represent all visited cities
# so bitmask is for ecityample of 4city4 tsp is 1111b = 2**4 - 1= (1 << 4) - 1 represents all visited nodes
# bitmask 0001 visit only fist/beginning node (0 node in ths ecitymaple)  and so one 0101 means tour =  0 - 2

    def compute_dynamic(self, position, set_of_visited_nodes):
        result = -1
        if self.g[position][set_of_visited_nodes] != -1: # when this value is not equal -1 that means we already compute this subproblem
            return self.g[position][set_of_visited_nodes]

        for city in range(self.number_of_vertices):
            # self.npow - 1 is equal to set of n number of '1' in binary n=4 = 1111 | 1 << city - creates next 2**city
            # if we substrack this two value we get all subset of 1110(for n-4 example) so it will be 1110 1101 1011 0111
            # 1 in element of this subset represent posiible node to chosed 
            mask = self.npow - 1 - (1 << city) 
            # now if we have posible way we have to chose a proper one
            # in this case we hae to do a 'AND' bit operator in this two binary number
            # we will unvisited node represent by 0
            # variable masked will be our new tour in future calculation
            masked = set_of_visited_nodes & mask

            if masked != set_of_visited_nodes:
                temp = self.graph[position][city] + self.compute_dynamic(city, masked) # recursive call of function with new expanded set_of_visited_nodes as masked
                
                # looking for min value of computed in this rute
                if result == -1 or result > temp:
                    result = temp
                    self.p[position][set_of_visited_nodes] = city # put number of visited city in to the ancillary graph p[] to get tour in other method 
        self.g[position][set_of_visited_nodes] = result # put cost in to the ancillary graph g[] 
        return result 

    def get_path(self, position, set_of_visited_nodes):
        if self.p[position][set_of_visited_nodes] == -1:  # no connetion over 
            return
        # backtrace of nodes in ancillary graph p[] we use the same 'bit magic' as in the upper method
        city = self.p[position][set_of_visited_nodes]
        mask = self.npow - 1 - (1 << city)  
        masked = set_of_visited_nodes & mask

        self.best_path.append(city)
        self.get_path(city, masked) # recursive call of fuction

# all of this operation we can find here: https://www.youtube.com/watch?v=JE0JE8ce1V0 
