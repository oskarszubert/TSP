import sys
from random import shuffle

class TabuSearch(object):

    def __init__(self, graph):
        self.graph = graph
        self.number_of_vertices = len(self.graph[0])
        self.tabu_list = [[0 for city in range(self.number_of_vertices)] for y in range(self.number_of_vertices) ]
        
        self.global_best_path = self.lenny_random_path(self.number_of_vertices)
        self.global_best_cost = self.get_path_cost(self.global_best_path)
        
        self.number_of_iteration = 300
        self.cadency = 5

        self.active_diversification = False
        self.diversification_number = 30 # default number, change by method set_diversification_number()
        self.diversification_counter = 0

        self.active_aspiration = False
        self.aspiration_ratio = 0.9 # default ratio in percent,by method change by set_aspiration_ratio()

    def __repr__(self):
        return "BrutTabuSearchForce object. Minimal cost path: {}. Best path: {}".format(self.global_best_cost, self.global_best_path)

    def print(self):
        print(" Minimal cost path: {}. Best path: {}".format(self.global_best_cost, self.global_best_path) )

    def set_of_iteration(self, number):
        if number <= 0:
            return
        self.number_of_iteration = number

    def set_cadency(self, cadency):
        if cadency <= 0:
            return
        self.cadency = cadency

    #if user set any number greater than 0 means that he want to use diversification
    def set_diversification_number(self, number):
        if number <= 0:
            return
        if number != 0:
            self.diversification_number = number
            self.active_diversification = True

    #if user set any ratio greater than 0 means that he want to use diversification
    def set_aspiration_ratio(self, ratio):
        if ratio >= 1 and ratio <=0:
            return # ratio cannot be grater than 100% and less than 0%
        if ratio != 0:
            self.aspiration_ratio = ratio
            self.active_aspiration = True

    def set_tabu_properties(self,itera,cadency, number, ratio):
        self.set_of_iteration(itera)
        self.set_cadency(cadency)
        self.set_diversification_number(number)
        self.set_aspiration_ratio(ratio)
        
    def lenny_random_path(self, number_of_vertices): # ( ͡° ͜ʖ ͡°) this is a 'random' path 
        path = [x for x in range(number_of_vertices)]
        path.append(0)

        return path

    def real_random_path(self, path): # real random path with 0 node as first element(and last)
        path = path[1:-1]
        shuffle(path)
        path.insert(0,0)
        path.append(0)
        
        return path

    def swap(self, tab, first_index, second_index):
        tab[first_index], tab[second_index] = tab[second_index], tab[first_index]

    def get_path_cost(self, path):
        path_cost = 0

        for i in range( len(path) - 1 ):
            path_cost += self.graph[ path[i] ][ path[i + 1] ]

        return path_cost

    def decrement_cadency(self):
        for i in range(self.number_of_vertices):
            for k in range(self.number_of_vertices):
                if self.tabu_list[i][k] != 0:
                    self.tabu_list[i][k] -= 1

    def clear_tabu_list(self):
        self.tabu_list = [[0 for city in range(self.number_of_vertices)] for y in range(self.number_of_vertices) ]

    def increase_diversification(self):
        self.diversification_number += self.diversification_number * 0.3
        if self.diversification_number > self.number_of_iteration:
            self.diversification_number = self.number_of_iteration * 0.3

    def diversification(self, path):
        # self.increase_diversification()
        self.clear_tabu_list()

        return self.real_random_path(path)

    def tabu(self):
        move_1, move_2 = 0, 0
        local_best_path = list(self.global_best_path)

        plot_twist = 0
        while self.number_of_iteration: # main loop
            self.number_of_iteration -= 1 
            plot_twist += 1
            current_path = list(local_best_path)
            local_best_cost = sys.maxsize

            #search for best neighbour                
            for i in range(1, self.number_of_vertices):
                for k in range(i + 1, self.number_of_vertices):

                    if self.active_aspiration:
                        self.swap(current_path, i, k) # create next neighbour
                        current_cost = self.get_path_cost(current_path)

                        if self.tabu_list[i][k] != 0:
                            if current_cost < (self.aspiration_ratio * local_best_cost): # check aspiration cond
                                local_best_path = list(current_path)
                                local_best_cost = current_cost
                                move_1, move_2 = i, k
                            else:
                                self.swap(current_path, i, k) # restore path
                                continue
                        else:
                        #IGNORE move in tabu_list
                            if current_cost < local_best_cost:
                                local_best_path = list(current_path)
                                local_best_cost = current_cost
                                move_1, move_2 = i, k

                    # aspiration not active:
                    else: 
                        #IGNORE move in tabu_list
                        if self.tabu_list[i][k] != 0:
                            continue
                        
                        self.swap(current_path, i, k) # create next neighbour
                        current_cost = self.get_path_cost(current_path)

                        if current_cost < local_best_cost:
                            local_best_path = list(current_path)
                            local_best_cost = current_cost
                            move_1, move_2 = i, k
      
                    self.swap(current_path, i, k) # restore path

            # print('(',plot_twist,',',local_best_cost,')') 
            # decrement all value in tabu_list  
            self.decrement_cadency()

            # add move_1 and move_2 to tabu_list    
            self.tabu_list[move_1][move_2] = self.cadency
            self.tabu_list[move_2][move_1] = self.cadency # just for sure


            if local_best_cost < self.global_best_cost:
                self.global_best_cost = local_best_cost
                self.global_best_path = list(local_best_path)
            else:
                if self.active_diversification:
                    self.diversification_counter += 1
                    if self.diversification_counter == self.diversification_number:
                        self.diversification_counter = 0
                        local_best_path = self.diversification(local_best_path) 