import sys

class GraphFromFile:
    def __init__(self, filename):
        self._number_of_vertex = -1
        self._graph = []
        self.read_from_file(filename)

    def __repr__(self):
        return 'TSP problem with {} vertexes'.format(self._number_of_vertex)

    @property
    def number_of_vertex(self):
        return self._number_of_vertex

    @property
    def graph(self):
        return self._graph

    def read_from_file(self, filename):
        try:
            file = open(filename, mode = 'rt', encoding = 'utf-8')
            row = []
            number_of_lines = 0
            for line in file:
                if number_of_lines == 0:
                    self._number_of_vertex = int(line)
                else:
                    row = line.split(' ')
                    while '' in row:    # check if row list have empty string cells. This part of code is needed coz file with cost for TSP are not standardized 
                        row.remove('')
                    while '\n' in row:
                        row.remove('\n')

                    row = list(map(int, row))  # change list of str to list of int  
                    self._graph.append(row)
                number_of_lines += 1
                if self._number_of_vertex + 1 == number_of_lines:
                    break

            file.close()
        except FileNotFoundError:
            print("Do not find file as {}".format(filename))
            sys.exit(-1)
        except Exception as e:
            print("Error while reading graph from file.\n", e)
            sys.exit(-1)
        return self._graph           
