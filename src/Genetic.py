import sys
from random import randint as rand

class Genetic:
    def __init__(self, graph):
        self.graph = graph
        
        self.number_of_iteration = 100
        self.number_of_vertices = len(self.graph[0]) # len(graph[0])

        self.population_size = 10 * self.number_of_vertices

        self.arena_size = int(0.3 * self.population_size) # how many paths is getting part in tournament

        self.mutation_ratio =  5 # percet  
        self.crossover_ratio = 90 # percet 

        self.parent_population = []
        self.child_population = []

        self.global_best_path = []
        self.global_best_cost = sys.maxsize

        self.elitism_ratio = 0.1
        self.elitism_number = int(self.elitism_ratio * self.population_size)

    def  __str__(self):
        return "Genetic TSP object. Minimal cost path: {}. Best path: {}".format(self.global_best_cost, self.global_best_path)

    def __repr__(self):
        return str(self.global_best_cost)  

    def set_number_of_iteration(self, number):
        self.number_of_iteration = number
    
    def set_population_size(self, size):
        self.population_size = size

    def set_arena_size(self, size):
        self.arena_size = size

    def set_mutation_ratio(self, ratio):
        self.mutation_ratio = ratio

    def set_crossover_ratio(self, ratio):
        self.crossover_ratio = ratio

    def set_genetic_properties(self, iters, pop, arena, mutate, cross ):
        self.set_number_of_iteration(iters)
        self.set_population_size(pop)
        self.set_arena_size(arena)
        self.set_mutation_ratio(mutate)
        self.set_crossover_ratio(cross)

    def genetic(self): # flow of genetic algorithm
        self.generate_population()

        while self.number_of_iteration:
            self.number_of_iteration -= 1
            
            self.choose_best_path()
            self.elitism()

            while self.parent_population :

                if len(self.parent_population) == 1 : # for odd size of population just copy last path to child without changing it 
                    self.child_population.append( self.parent_population[0] )
                    self.parent_population = []
                    continue

                selected_parents = self.tournament_selection()
                child = self.chance_of_crossover(selected_parents[0], selected_parents[1])
                for path in child:
                    self.child_population.append(path) # add paths to child 


            for path in self.child_population: # try mutate every path in child population 
                self.chance_of_mutation(path)

            self.parent_population = list(self.child_population) # exchange of generations :) child become parents
            self.child_population = [] # wiped childer population

    def choose_best_path(self):
        self.parent_population.sort()
        potencial_best = self.parent_population[0] # python zen
        if potencial_best[0] < self.global_best_cost:
            self.global_best_cost = potencial_best[0]
            self.global_best_path = potencial_best[1]

    def elitism(self):
        self.parent_population.sort()
        for path in self.parent_population[:self.elitism_number]:
            self.child_population.append(path)
            self.parent_population.remove(path)

        for path in self.parent_population[-self.elitism_number:]:
            self.child_population.append(path)
            self.parent_population.remove(path)
            
    def print(self):
        if len(self.global_best_path) == 0:
            print('Do not found best path yet')
        else: 
            print('Minimal cost path: {}. \nBest path with Genetic Algorithm for TSP: '.format(self.global_best_cost))
            print("\tPath: ",end = '')
            for vertex in self.global_best_path[:-1]:
                print('{} \u2192 '.format(vertex), end='')
            print(self.global_best_path[0])

    @staticmethod        
    def swap( tab, first_index, second_index):
        tab[first_index], tab[second_index] = tab[second_index], tab[first_index]


    def get_random_path(self):
        tab = [x for x in range(1, self.number_of_vertices)]
        
        for i in range(self.number_of_vertices ): # randomize by swaping n-times
            a, b = rand(0, self.number_of_vertices - 2), rand(0, self.number_of_vertices - 2) # random points to swap
            self.swap(tab,a,b)

        tab.insert(0,0)
        tab.append(0)

        return tab

    def generate_population(self): # each 'individual' will be represent with [cost, [path]]
        for i in range(self.population_size):
            tmp = []       
            path = self.get_random_path()    
            tmp.append( self.get_path_cost(path) )
            tmp.append(path)
            self.parent_population.append(tmp)


    def get_path_cost(self, path):
        path_cost = 0

        for i in range( len(path) - 1 ):
            path_cost += self.graph[ path[i] ][ path[i + 1] ]

        return path_cost


    def tournament_selection(self):
        winners = []
        number_of_winners = 2 # in this case we just need two paths for crossover

        if len(self.parent_population) == number_of_winners: 
            winners = list(self.parent_population)
            self.parent_population = []
            return winners

        population = list(self.parent_population) # copy global parent population

        for i in range(number_of_winners):
            arena = []

            if len(self.parent_population) < self.arena_size: # what if size of population is lower than arena :)
                arena = list( population ) 

            else:
                for k in range(self.arena_size):  #choose self.arena_size paths to tournament
                    random_index = rand(0, len(population) -1)

                    arena.append( population[random_index] )
                    del population[random_index]

            arena.sort()  
            winners.append(arena[0])
            self.parent_population.remove( winners[-1] ) # remove latest winner from global parent_population
            population = list(self.parent_population) # restore population

        return winners

    def chance_of_mutation(self, individual): # works on invidual [cost, [path] ]
        rand_numer = rand(0,100001) / 1000 # in percent

        if rand_numer <= self.mutation_ratio:
            path = individual[1]
            individual = []
            path = self.mutation_insertion(path)
            # path = self.mutation_swap(path)
            individual.append(self.get_path_cost( path ))
            individual.append( path )

        return individual

    def mutation_swap(self, path):
        path = path[1:-1]
        a, b = rand( 0, len( path ) - 2 ), rand( 0, len( path ) - 2 )
        self.swap(path, a, b)
        path.insert(0,0)
        path.append(0)

        return path

    @staticmethod
    def mutation_insertion(path):
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

        return path
        
    def chance_of_crossover(self, parent_1, parent_2): # in param tooks [cost, [path]]
        rand_numer = rand(0,100001) / 1000 # in percent
        childs = []
        if rand_numer <= self.crossover_ratio: 
            childs = self.pmx(parent_1[1], parent_2[1])
        else:  # if not crossover parents will became child with no changes
            childs.append(parent_1)
            childs.append(parent_2)

        return childs


    def pmx(self, first, second ): # Partially Matched Crossover in param tooks [path]
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

        childs = [] # result as list

        childs.append( self.reconstruct_pmx(first_parent, second_parent, pmx_map_1, point_1, point_2) )     
        childs.append( self.reconstruct_pmx(second_parent, first_parent, pmx_map_2, point_1, point_2) )

        return childs 

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

        child = []
        path = [0] + part_1[:point_1] + part_2 + part_1[point_1:] + [0]
        child.append( self.get_path_cost( path ) )
        child.append( path )

        return child
