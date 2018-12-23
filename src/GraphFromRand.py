from random import randint as rand

class GraphFromRand():

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
            # if self._number_of_vertex > 20:
            #     print('To much number of vertexes change your number in to 20')
            #     self._number_of_vertex = 20

            for i in range(self._number_of_vertex):
                tmp_list = []
                for k in range(self._number_of_vertex):
                    if k == i:
                        tmp_list.append(-1)
                    else:
                        tmp_list.append(rand(0,max_value))
                self._graph.append(tmp_list)

    def print(self):
        print("Number of vertexes: {}".format(self._number_of_vertex))
        print('    ', end='')
        for i in range(self._number_of_vertex ):
            print('{0:5d}'.format(i),end='')
        print('\n    ', end='')
        for i in range(self._number_of_vertex ):
            print(5*'-',end='')
        print()            

        i = 0
        for row in self._graph: 
            print('{0:2d} |'.format(i), end='')
            i += 1
            for cell in row:
                print('{0:5d}'.format(cell), end='')
            print('')
