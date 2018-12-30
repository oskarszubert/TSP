import os
import sys

from GraphFromFile import *
from GraphFromRand import *
from Time import *

from BrutForce import *
from Dynamic import *
from TabuSearch import *
from Genetic import *

class UserInterface:
    def __init__(self, n_number):
        self.n_tests = n_number
        self.hue()

    @staticmethod
    def prepare_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
        print('------------ Traveling Salesman Problem | O.Szubert ------------')

    def hue(self):
        self.prepare_screen()
        batch = self.input_method()
        result_filename = self.save_result_as()
        algo_trigger = self.choose_algorithm(result_filename, batch)


    def input_method(self):
            self.prepare_screen()
            try:
                 input_method = int(input('------------Choose input method: \
                \n\t[ 1 ] From single file \
                \n\t[ 2 ] From all file in specific dir \
                \n\t[ 3 ] Generate random graph \
                \n\t ------------------------------- \
                \n\t[ 0 ] Exit \
                \nYour choice: '))

            except Exception:
                print('*** Something went wrong! ***')
                sys.exit(-1)         

            while not (input_method >= 0 and input_method <= 3 ):
                input_method = int(input('Wrong choice try again: '))

            if input_method == 0:
                sys.exit()
            if input_method == 1:
                batch = self.single_file()
            if input_method == 2:
                batch = self.multiple_file()
            if input_method == 3:
                batch = self.generate_graph()

            return batch

    def choose_algorithm(self, result_filename, batch):
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            algo_trigger = int(input('------------Choose method to solve TSP problem: \
                \n\t [ 1 ] Brutforce \
                \n\t [ 2 ] Dynamic programming \
                \n\t [ 3 ] Tabu Search \
                \n\t [ 4 ] Genetic Algorithm \
                \n\t ------------------------------- \
                \n\t [ 0 ] Exit \
                \nYour choice: '))
        except Exception:
            print('*** Something went wrong! ***')
            sys.exit(-1)  

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
            
            time_as_str = '{0:7f}'.format(time.result)
            self.save_as_csv(result_filename, time_as_str, bf.best_cost, bf.best_paths)

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
            self.save_as_csv(result_filename, time_as_str, dp.best_cost, dp.best_path)
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
        print('***Note: if you want to test more than value of parameter type them and seperate with spacebar\n\
            like: 10 20 30 . And press Enter to accept.\n Type \'-1\' to use default value of parameter.***\n')
        try:
            iteration = input('Type number of iteration: ')
            cadency = input('Type length of TABU LIST  greater than 0: ')
            diversification_number = input('To ACTIVATE diversification type number greater than 0: ')
            aspiration_ratio = input('To ACTIVATE aspiratio type a decimal fraction in the range of [0-1]: ')
        except Exception:
            print('*** Something went wrong! ***')
            sys.exit(-1)  

        iteration = self.create_int_list(iteration)
        cadency = self.create_int_list(cadency)
        diversification_number = self.create_int_list(diversification_number)
        aspiration_ratio = self.create_float_list(aspiration_ratio)

        time = Time()
        
        self.csv_title(result_filename, 'Iteration', 'Cadency', 'Diversification', 'Aspiratio', 'Type')
        for graph in batch:
            self.print_graph(graph)
            
            for iters in iteration:
                for cad in cadency:
                    for diver in  diversification_number:
                        for asp in aspiration_ratio:
                            
                            result_tabu = []
                            time_tabu = []
                            time_avg = 0
                            cost_avg = 0
                            for test in range(self.n_tests):
                                tmp_tab = []
                                tabu = TabuSearch(graph)
                                if iters == -1:
                                    iters = tabu.number_of_iteration
                                if cad == -1:
                                    cad = tabu.cadency
                                if diver == -1:
                                    diver = tabu.diversification_number
                                if asp == -1:
                                    asp = tabu.aspiration_ratio
                                tabu.set_tabu_properties(iters, cad, diver, asp)
                                time.start()
                                tabu.tabu()
                                time.stop()
                                
                                time_avg += time.result
                                cost_avg += tabu.global_best_cost

                                tmp_tab.append(tabu)
                                tmp_tab.append(time.result)
                                result_tabu.append(tmp_tab) # in this list signle elements is: [tabu, time]
                                del time.result

                            tabu = result_tabu[0][0]
                            global_time = result_tabu[0][1]
                            global_cost = tabu.global_best_cost 
                            for tabu_solution in result_tabu:
                                tmp_cost = int(repr( tabu_solution[0] ))
                                if tmp_cost < global_cost:
                                    tabu = tabu_solution[0]
                                    global_cost = tmp_cost
                                    global_time = tabu_solution[1]
                            
                            time_avg /= self.n_tests
                            cost_avg /= self.n_tests
                            print('\n-----------------------------------------------------------')
                            tabu.print()
                            print('Time = {0:7f} [sec]'.format( global_time))
                            print('Iteration: {}. Cadency: {}. Diversification: {}. Aspiratio: {}'.format(iters, cad, diver, asp ))
                            time_as_str =  '{0:7f}'.format(global_time)
                            time_as_str_avg =  '{0:7f}'.format(time_avg)
                            self.save_as_csv(result_filename,
                                            len(graph[0]),
                                            time_as_str, 
                                            tabu.global_best_cost,
                                            tabu.global_best_path,
                                            iters,
                                            cad,
                                            diver,
                                            asp,
                                            'best found')
                            if self.n_tests > 1:
                                self.save_as_csv(result_filename,
                                                len(graph[0]),
                                                time_as_str_avg, 
                                                cost_avg,
                                                '-',
                                                iters,
                                                cad,
                                                diver,
                                                asp,
                                                'avg')

    def genetic_algo(self, batch, result_filename):
        print('***NOTE: if you want to test more than value of parameter type them and seperate with spacebar\n\
            like: 10 20 30 . And press Enter to accept.\n Type \'-1\' to use default value of parameter.***\n')

        iteration = input('Type number of iteration: ')
        population_size = input('Type population size greater than 0: ')
        arena_size = input('Type arena size greater than 0: ')
        muatation_ratio = input('To ACTIVATE mutation type percent [0-100]  ')  
        crossover_ratio = input('To ACTIVATE crossover type percent [0-100]  ')

        try:
            iteration = self.create_int_list(iteration)
            population_size = self.create_int_list(population_size)
            arena_size = self.create_int_list(arena_size)
            muatation_ratio = self.create_float_list(muatation_ratio)
            crossover_ratio = self.create_float_list(crossover_ratio)

        except Exception:
            print('*** Something went wrong! ***')
            sys.exit(-1)  

        time = Time()

        self.csv_title(result_filename, 'Iteration', 'Population size', 'Arena size', 'Muatation', 'Crossover', 'Type')
        for graph in batch:
            self.print_graph(graph) 
            for iters in iteration:
                for pop in population_size:
                    for arena in  arena_size:
                        for mut in muatation_ratio:
                            for cros in crossover_ratio:
                                result_genetic = []
                                time_tabu = []
                                time_avg = 0
                                cost_avg = 0
                                for test in range(self.n_tests):
                                    tmp_tab = []
                                    genetic = Genetic(graph)
                                    if iters == -1:
                                        iters = genetic.number_of_iteration
                                    if pop == -1:
                                        pop = genetic.population_size
                                    if arena == -1:
                                        arena = int(pop * 0.3)
                                    if mut == -1:
                                        mut = genetic.mutation_ratio
                                    if cros == -1:
                                        cros = genetic.crossover_ratio

                                    genetic.set_genetic_properties(iters, pop, arena, mut, cros)

                                    time.start()
                                    genetic.genetic()
                                    time.stop()
                                    
                                    time_avg += time.result
                                    cost_avg += genetic.global_best_cost
                                    
                                    tmp_tab.append(genetic)
                                    tmp_tab.append(time.result)
                                    result_genetic.append(tmp_tab) # in this list signle elements is: [tabu, time]

                                    del time.result

                                genetic = result_genetic[0][0]
                                global_time = result_genetic[0][1]
                                global_cost = genetic.global_best_cost 
                                for genetic_solution in result_genetic:
                                    tmp_cost = int(repr( genetic_solution[0] ))
                                    if tmp_cost < global_cost:
                                        genetic = genetic_solution[0]
                                        global_cost = tmp_cost
                                        global_time = genetic_solution[1]
                                time_avg /= self.n_tests
                                cost_avg /= self.n_tests
                                print('\n-----------------------------------------------------------')
                                genetic.print()

                                print('Time = {0:7f} [sec]'.format( global_time))
                                print('Iteration: {}. Population size: {}. Arena size: {}. Mutation: {}.  Crossover: {} '.format(iters, pop, arena, mut, cros ))
                                time_as_str =  '{0:7f}'.format(global_time)
                                time_as_str_avg =  '{0:7f}'.format(time_avg)
                                self.save_as_csv(result_filename,
                                                len(graph[0]),
                                                time_as_str, 
                                                genetic.global_best_cost,
                                                genetic.global_best_path,
                                                iters, 
                                                pop, 
                                                arena, 
                                                mut, 
                                                cros,
                                                'best found')
                                if self.n_tests > 1:
                                    self.save_as_csv(result_filename,
                                                    len(graph[0]),
                                                    time_as_str_avg, 
                                                    cost_avg,
                                                    '-',
                                                    iters,
                                                    pop, 
                                                    arena, 
                                                    mut, 
                                                    cros,
                                                    'avg')

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
        try:
            filename = input('Enter filename in your local dir: ')
        except Exception:
            print('*** Something went wrong! ***')
            sys.exit(-1)

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
        try:
            dir_name =input("Enter dir name: ") + '/'
        except Exception:
            print('*** Something went wrong! ***')
            sys.exit(-1)  

        for filename in os.listdir(dir_name):
            file = GraphFromFile(dir_name + filename)
            graph = file.graph
            batch.append(graph)

        return batch

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
        try:
            dir_name = input('Input directory name where do you want to save your graph(s): ')
            number_of_vertex = int(input('Input NUMBER OF VERTEXES in graph: '))
            max_value = int(input('Input NUMBER OF MAX VALUE of one connection between two vertexes: '))
            print('Input HOW MANY GRAPHS that you want to generate: \n***Note: if INPUT >= 2 program will generate graphs with {}, {} ... number of vertexes***'.format(number_of_vertex, number_of_vertex +1))
            num_of_graphs = int(input('Number of graphs: '))
        except Exception:
            print('*** Something went wrong! ***')
            sys.exit(-1)  

        if num_of_graphs > 1:
            print('Gererating graphs with number of vertex: {} to {}'.format(number_of_vertex, number_of_vertex + num_of_graphs - 1))
            for i in range(num_of_graphs):
                graph = GraphFromRand(number_of_vertex + i, max_value)
                batch.append(graph.graph)
        else:
            graph = GraphFromRand(number_of_vertex, max_value)
            batch.append(graph.graph)

        self.save_graph_to_file(dir_name, batch)

        return batch

    @staticmethod
    def save_graph_to_file(dir_name, batch):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        for graph in batch:
            graph_filename = dir_name + '/tsp_' + str(len(graph)) + '.txt'
            file = open(graph_filename, 'w')

            file.write(str(len(graph[0])) + '\n')

            for row in graph:
                for cell in row:
                    file.write(str(cell) + ' ')
                file.write('\n')

            file.close()

    @staticmethod
    def print_graph(graph):
        number_of_vertex = len(graph[0])
        if number_of_vertex > 20:
            return

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
