from random import randrange as rand

class Genetic():

    def __init__(self):
        # self.graph = []

        self.graph = [
        [0, 10, 15, 20],
        [5, 0, 9, 10],
        [6, 13, 0, 12],
        [8, 8, 9, 0]]

        self.number_of_iteration = 100
        self.population_size = 10

        self.arena_size = 2 # how many paths is getting part in tournament

        self.mutation_ratio =  1 # percet  
        self.crossover_ratio = 90 # percet 

        self.number_of_vertices = len(self.graph[0]) # len(graph[0])
        self.population = []
        self.generate_population()



    def genetic(self):

        while self.number_of_iteration:
            self.number_of_iteration -= 1

        # evaluate all paths , remeber global_best_path/ global_best_cost
        # from tournament choose two paths and PMX // how many another param?

        #try do mutation on every path in population

        #add stop criterion, like- if do not found new best path for n-iteration stop(?)



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

        population = list(self.population)
        for i in range(number_of_winners):
            arena = []

            for k in range(self.arena_size): # choose self.arena_size paths to tournament
                random_index = rand(0, len(population) )
                arena.append( population[random_index] )
                del population[random_index]

            # choose best path:
            result = []
            for path in arena:
                tmp = []
                cost = self.get_path_cost(path)
                tmp.append(cost)
                tmp.append(path)
                result.append(tmp)

            result.sort()

            winners.append(result[0][1])


            population = list(self.population) # restore population but without prevoius winner 
            population.remove( winners[-1] )

        return winners


    def mutation_swap(self, path):
        rand_numer = rand(0,100001) / 1000 # in percent

        if rand_numer <= self.mutation_ratio:
            path = path[1:-1]
            a, b = rand( 0, len( path ) - 2 ), rand( 0, len( path ) - 2 )
            self.swap(path,a,b)
            path.insert(0,0)
            path.append(0)

    def mutation_invertion(self, path):
        rand_numer = rand(0,100001) / 1000 # in percent

        if rand_numer <= self.mutation_ratio:
            path = path[1:-1]
            random_range = len(path)

            # choose random subpath bounded by two random points || point_1 < point_2. point_1 != last element
            point_1 = rand(0, random_range -2 )
            point_2 = rand(point_1 + 1, random_range - 1)

            subpath = path[point_1:point_2]
            path = path[0:point_1] + path[point_2:]

            point_3 = rand(0,len(path)) # put our subpath in random place in the rest of path
            path = path[0:point_3] + subpath + path[point_3:]
            path.insert(0,0)
            path.append(0) 
            

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

        parent = [0] + part_1[:point_1] + part_2 + part_1[point_1:] + [0]

        return parent
