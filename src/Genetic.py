from random import randrange as rand
class Genetic():

    def __init__(self):
        self.number_of_iteration = 100
        self.population_size = 10
        self.number_of_vertices = 10
        self.population = []
        self.generate_population()

        self.graph = []


    def swap(self, tab, first_index, second_index):
        tab[first_index], tab[second_index] = tab[second_index], tab[first_index]


    def get_random_path(self):
        tab = [x for x in range(1, self.number_of_vertices)]
        
        for i in range(self.number_of_vertices ): # randomize by swaping n-times
            a, b = rand(0, self.number_of_vertices - 2), rand(0, self.number_of_vertices - 2)
            self.swap(tab,a,b)

        tab.insert(0,0)
        tab.append(0)
        return tab

    def generate_population(self):
        for i in range(self.population_size):
            self.population.append(self.get_random_path())


    def get_path_cost(self, path):
        path_cost = 0

        for i in range( len(path) - 1 ):
            path_cost += self.graph[ path[i] ][ path[i + 1] ]

        return path_cost

    def tournament_selection(self, number_of_winners):
        winners = []

        for i in range(number_of_winners):
            pass


        return winners


    def mutation(self, tab):
        a, b = rand( 0, self.number_of_vertices - 2 ), rand( 0, self.number_of_vertices - 2 )
        self.swap(tab,a,b)
        

    def pmx(self, first, second ): # Partially Matched Crossover
        first_parent = first[1:-1]
        second_parent = second[1:-1]
        random_range = len(first_parent)

        # choose two points randomly point_1 < point_2. point_1 != last element in the list.
        point_1 = rand(0, random_range -2 )
        point_2 = rand(point_1 + 1, random_range - 1)

        # point_1 = 2
        # point_2 = 6

        pmx_map_1 = []
        pmx_map_2 = []
        for i in range(point_1, point_2): # create 'map' for pmx as two dimensional list, additionally change crossingover part of path
            tmp = []
            tmp_2 = []

            tmp.append( second_parent[i] )
            tmp.append( first_parent[i] )

            tmp_2.append( first_parent[i] )
            tmp_2.append( second_parent[i] )

            pmx_map_1.append(tmp)
            pmx_map_2.append(tmp_2)

 
        self.reconstruct_pmx(first_parent, second_parent, pmx_map_1, point_1, point_2)     
        self.reconstruct_pmx(second_parent, first_parent, pmx_map_2, point_1, point_2)     
    


    def reconstruct_pmx(self,first_parent, second_parent, pmx_map, point_1, point_2):
        part_1 = first_parent[:point_1] + first_parent[point_2:] # part not taking part in replecment
        part_2 = second_parent[point_1:point_2] # part from crossingover


        # (almost) old C style :)
        for n in range( len(part_2) ):
            for i in range( len(part_1) ): # for every element in part_1 check if its already in part_2
                    if part_1[i] in part_2:
                        for k in range(len(part_2)): # if it is change with pmx_map
                            if part_1[i] == pmx_map[k][0]:
                                part_1[i] = pmx_map[k][1]

        parent = part_1[:point_1] + part_2 + part_1[point_1:]

        return parent