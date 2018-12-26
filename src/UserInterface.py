import os
import sys

from GraphFromFile import *
from GraphFromRand import *
from Time import *

from BrutForce import *
from Dynamic import *
from TabuSearch import *
from Genetic import *

class UserInterface(object):

    def __init__(self):

        # x = input("put table here")
        # x = x.split(" ")
        # while '' in x:
        #     x.remove('')
        # print(x)
        self.hue()


    @staticmethod
    def prepare_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('------------ Traveling Salesman Problem | O.Szubert ------------')

    def hue(self):
        self.prepare_screen()
        x = int(input('Choose what you want to do: \
            \n\t[ 1 ] Solve TSP with specified algorithm \
            \n\t[ 2 ] Generate random graph \
            \n\t------------------------------- \
            \n\t[ 0 ] Exit \
            \nYour choice: '))

        if x == 0:
            sys.exit()
        if x == 1:
            batch = self.input_method()
            result_filename = self.save_result_as()
            algo_trigger = self.choose_algorithm(result_filename, batch)

        if x == 2:
            pass 

    def input_method(self):
            self.prepare_screen()
            input_method = int(input('------------Choose input method: \
            \n\t[ 1 ] From single file \
            \n\t[ 2 ] From all file in specific dir \
            \nYour choice: '))
            # \n\t[ 3 ] Generate random graph \

            while not (input_method >= 1 and input_method <= 2 ):
                input_method = int(input('Wrong choice try again: '))
            
            if input_method == 1:
                batch = self.single_file()
            if input_method == 2:
                batch = self.multiple_file()
            # if input_method == 3:
                # batch = self.generate_graph()

            return batch

    def choose_algorithm(self, result_filename, batch):
        os.system('cls' if os.name == 'nt' else 'clear')
        algo_trigger = int(input('------------Choose method to solve TSP problem: \
            \n\t [ 1 ] Brutforce \
            \n\t [ 2 ] Dynamic programming \
            \n\t [ 3 ] Tabu Search \
            \n\t [ 4 ] Genetic Algorithm \
            \n\t ------------------------------- \
            \n\t [ 0 ] Exit \
            \nYour choice: '))

        while not (algo_trigger >= 0 and algo_trigger <= 4):
            algo_trigger = int(input('Wrong choice try again: '))

        if algo_trigger == 0:
            sys.exit()
        if algo_trigger == 1:
            self.brutforce_algo(batch, result_filename)
        if algo_trigger == 2:
            self.dynamic_algo(batch, result_filename)
        if algo_trigger == 3:
            self.tabu_algo(batch, result_filename)
        if algo_trigger == 4:
            self.genetic_algo(batch, result_filename)

    def save_result_as(self):
        self.prepare_screen()

        if not os.path.exists('results'):
            os.makedirs('results')

        result_filename = input('Save your solutions as: ')
        result_filename = 'results/' + result_filename + '.csv'
        result_file = open(result_filename, 'w')
        result_file.close()
        return result_filename

    def brutforce_algo(self, batch, result_filename):
        time = Time()

        self.csv_title(result_filename)
        for graph in batch:
            bf = BrutForce()
            time.start()

            bf.brutforce(graph)
            time.stop()

            print('\n-----------------------------------------------------------')
            self.print_graph(graph)
            bf.print()
            print('Time = {0:8f} [sec] '.format( time.result))
            
            time_as_str =  '{0:7f}'.format(time.result)
            self.save_as_csv(result_filename, time.result, bf.best_cost, bf.best_paths)

            del time.result

    def dynamic_algo(self, batch, result_filename):
        time = Time()

        self.csv_title(result_filename)
        for graph in batch:
            dp = DynamicTsp()
            time.start()

            dp.dynamic(graph)
            time.stop()

            print('\n-----------------------------------------------------------')
            self.print_graph(graph)
            dp.print()
            print('Time = {0:7f} [sec] '.format( time.result))

            time_as_str =  '{0:7f}'.format(time.result)
            self.save_as_csv(result_filename, time.result, dp.best_cost, dp.best_path)
            del time.result

    @staticmethod
    def create_int_list(tab):
        tab = tab.split(' ')
        while '' in tab:
            tab.remove('')
        for i in range(len(tab)):
            tab[i] = int(tab[i])

        return tab

    @staticmethod
    def create_float_list(tab):
        tab = tab.split(' ')
        while '' in tab:
            tab.remove('')
        for i in range(len(tab)):
            tab[i] = float(tab[i])

        return tab

    def tabu_algo(self, batch, result_filename):
        print('***NOTE: if you want to test more than value of parameter type them and seperate with spacebar\n\
            like: 10 20 30 . And press Enter to accept.***\n')
        iteration = input('Type number of iteration: ')
        cadency = input('Type length of TABU LIST  greater than 0: ')
        diversification_number = input('To ACTIVATE diversification type number greater than 0: ')
        aspiration_ratio = input('To ACTIVATE aspiratio type a decimal fraction in the range of [0-1]: ')


        iteration = self.create_int_list(iteration)
        cadency = self.create_int_list(cadency)
        diversification_number = self.create_int_list(diversification_number)
        aspiration_ratio = self.create_float_list(aspiration_ratio)

        time = Time()

        self.csv_title(result_filename, 'Iteration', 'Cadency', 'Diversification', 'Aspiratio' )
        for graph in batch:
            print('\n-----------------------------------------------------------')
            self.print_graph(graph)
            
            for iters in iteration:
                for cad in cadency:
                    for diver in  diversification_number:
                        for asp in aspiration_ratio:
                            tabu = TabuSearch(graph)
                            tabu.set_tabu_properties(iters, cad, diver, asp)
                            time.start()
                            tabu.tabu()
                            time.stop()
                            
                            print('\n-----------------------------------------------------------')
                            tabu.print()

                            print('Time = {0:8f} [sec]'.format( time.result))
                            print('Iteration: {}. Cadency: {}. Diversification: {}. Aspiratio: {}'.format(iters, cad, diver, asp ))
                            time_as_str =  '{0:7f}'.format(time.result)
                            self.save_as_csv(result_filename,
                                            len(graph[0]),
                                            time_as_str, 
                                            tabu.global_best_cost,
                                            tabu.global_best_path,
                                            iters,
                                            cad,
                                            diver,
                                            asp)

                            del time.result

    def genetic_algo(self, batch, result_filename):
        print('***NOTE: if you want to test more than value of parameter type them and seperate with spacebar\n\
            like: 10 20 30 . And press Enter to accept.***\n')

        iteration = input('Type number of iteration: ')
        population_size = input('Type population size greater than 0: ')
        arena_size = input('Type arena size greater than 0: ')
        muatation_ratio = input('To ACTIVATE muatation type percent [0-100]  ')  
        crossover_ratio = input('To ACTIVATE crossover type percent [0-100]  ')

        iteration = self.create_int_list(iteration)
        population_size = self.create_int_list(population_size)
        arena_size = self.create_int_list(arena_size)
        muatation_ratio = self.create_float_list(muatation_ratio)
        crossover_ratio = self.create_float_list(crossover_ratio)

        time = Time()

        self.csv_title(result_filename, 'Iteration', 'Population size', 'Arena size', 'Muatation', 'Crossover')
        for graph in batch:
            self.print_graph(graph) 
            for iters in iteration:
                for pop in population_size:
                    for arena in  arena_size:
                        for mut in muatation_ratio:
                            for cros in crossover_ratio:
                                genetic = Genetic(graph)
                                genetic.set_genetic_properties(iters, pop, arena, mut, cros)
                                time.start()
                                genetic.genetic()
                                time.stop()
                                
                                print('\n-----------------------------------------------------------')
                                genetic.print()

                                print('Time = {0:8f} [sec]'.format( time.result))
                                print('Iteration: {}. Population size: {}. Arena size: {}. Muatation: {}.  Crossover: {} '.format(iters, pop, arena, mut, cros ))
                                time_as_str =  '{0:7f}'.format(time.result)
                                self.save_as_csv(result_filename,
                                                len(graph[0]),
                                                time_as_str, 
                                                genetic.global_best_cost,
                                                genetic.global_best_path,
                                                iters, 
                                                pop, 
                                                arena, 
                                                mut, 
                                                cros)

                                del time.result

    @staticmethod
    def csv_title(*args): # asume that args[0] is filename
        result_filename = args[0]        
        result_file = open(result_filename, 'a')
        result_file.write('number of vertexes;time[sec];cost;path;')

        for i in args[1:]:
            result_file.write(str(i) + ';')

        result_file.write('\n')
        result_file.close()

    @staticmethod
    def save_as_csv(*args): # asume that args[0] is filename
        result_filename = args[0]
        result_file = open(result_filename, 'a')
        for i in args[1:]:
            result_file.write(str(i) + ';')
        result_file.write('\n')
        result_file.close()

    @staticmethod    
    def single_file():
        batch = []
        filename = input('Enter filename in your local dir: ')
        file = GraphFromFile(filename)
        batch.append(file.graph)
        return batch

    @staticmethod
    def single_file_remote(filename):
        batch = []
        file = GraphFromFile(filename)
        batch.append(file.graph)
        return batch

    @staticmethod
    def multiple_file():
        batch = []
        dir_name =input("Enter dir name: ") + '/'

        for filename in os.listdir(dir_name):
            file = GraphFromFile(dir_name + filename)
            graph = file.graph
            batch.append(graph)

    @staticmethod
    def multiple_file_remote(dir_name):
        batch = []

        for filename in os.listdir(dir_name):
            file = GraphFromFile(dir_name + filename)
            graph = file.graph
            batch.append(graph)

        return batch

    def generate_graph(self):
        batch = []
        number_of_vertex = int(input('Input NUMBER OF VERTEXES in graph: '))
        max_value = int(input('Input NUMBER OF MAX VALUE of one connection between two vertexes: '))
        print('Input HOW MANY GRAPHS that you want to generate: \n***Note: if INPUT >= 2 program will generate graphs with {}, {} ... number of vertexes***'.format(number_of_vertex, number_of_vertex +1))
        num_of_graphs = int(input('Numver of graphs: '))


        if num_of_graphs > 1:
            print('Gererating graphs with number of vertex: {} to {}'.format(number_of_vertex, number_of_vertex + num_of_graphs - 1))
            for i in range(num_of_graphs):
                graph = GraphFromRand(number_of_vertex + i, max_value)
                batch.append(graph.graph)
        else:
            graph = GraphFromRand(number_of_vertex, max_value)
            batch.append(graph.graph)

        return batch 

    @staticmethod
    def print_graph(graph):
        number_of_vertex = len(graph[0])
        # if number_of_vertex < 20:
        #     return

        print("Number of vertexes: {}".format(number_of_vertex))
        print('    ', end='')
        for i in range(number_of_vertex ):
            print('{0:5d}'.format(i),end='')
        print('\n    ', end='')
        for i in range(number_of_vertex ):
            print(5*'-',end='')
        print()            

        i = 0
        for row in graph: 
            print('{0:2d} |'.format(i), end='')
            i += 1
            for cell in row:
                print('{0:5d}'.format(cell), end='')
            print('')
