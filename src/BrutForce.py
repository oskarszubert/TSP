import itertools

class BrutForce():

    def __init__(self):
        self.best_cost = -1
        self.best_paths = []
        self.matrix_of_perumtation = []

    def __repr__(self):
        if self.best_cost == -1:
            return "BrutForce object. Not used yet."
        else:
            return "BrutForce object. Minimal cost path: {}. Best path: {}".format(self.best_cost, self.best_paths)
       
    def brutforce(self, graph):
        number_of_vertexes = len(graph[0])
        nums = list(range(1, number_of_vertexes))
        self.compute_brutforce_and_permute(graph, nums, 0, number_of_vertexes-2 )
        
        return self.best_cost

    def print(self):
        if len(self.best_paths) == 0:
            print('Do not found best path yet')
        else: 
            print('Minimal cost path: {}. \nBest path with Brutforce for TSP: '.format(self.best_cost))
            for path in self.best_paths:
                print('\tPath: ', end='')
                for vertex in path:
                    print('{} \u2192 '.format(vertex), end='')
                print('{}'.format(path[0]))

    def compute_brutforce_and_permute(self, graph, nums, start, end_index):
        if start==end_index: 
            path_tmp = []
            for i in range(len(nums)):
                path_tmp.append(nums[i])
            path_tmp.insert(0, 0)

            path_cost = 0
            for i in range( len(path_tmp) -1 ):
                path_cost += graph[ path_tmp[i] ][ path_tmp[i + 1] ]
            path_cost += graph[path_tmp[-1]][path_tmp[0]]

            if self.best_cost == -1:
                self.best_cost = path_cost
                self.best_paths.append(path_tmp)

            if path_cost < self.best_cost:
                self.best_cost = path_cost
                self.best_paths.clear()
                self.best_paths.append(path_tmp)

            return self.best_cost

        else: 
            for i in range(start,end_index+1): 
                nums[start], nums[i] = nums[i], nums[start] 
                self.compute_brutforce_and_permute(graph, nums, start+1, end_index) 
                nums[start], nums[i] = nums[i], nums[start] # backtrack 
