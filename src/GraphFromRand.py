from random import randint as rand

class GraphFromRand:
    def __init__(self, number_of_vertex, max_value):
        self._number_of_vertex = number_of_vertex
        self._graph = []
        self.create_graph(max_value)


    def __repr__(self):
        return 'Random graph for TSP problem with {} vertexes'.format(self._number_of_vertex)

    @property
    def number_of_vertex(self):
        return self._number_of_vertex

    @property
    def graph(self):
        return self._graph

    def create_graph(self, max_value):
            for i in range(self._number_of_vertex):
                tmp_list = []
                for k in range(self._number_of_vertex):
                    if k == i:
                        tmp_list.append(-1)
                    else:
                        tmp_list.append(rand(0,max_value))
                self._graph.append(tmp_list)
