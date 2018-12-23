from Genetic import *
from GraphFromFile import *

filename = 'tsp.txt'
file = GraphFromFile(filename)
graph = file.graph
sd = Genetic(graph)

sd.genetic()
sd.print()
