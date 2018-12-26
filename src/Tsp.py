class Tsp(object):

    def __init__(self):
        self.global_best_path = []
        self.global_best_cost = sys.maxsize

    def get_path_cost(self, path):
        path_cost = 0

        for i in range( len(path) - 1 ):
            path_cost += self.graph[ path[i] ][ path[i + 1] ]

        return path_cost