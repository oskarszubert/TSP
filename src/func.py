import os

from GraphFromFile import *
from GraphFromRand import *
from Time import *

from Genetic import *


def main():
    print('-----------------PEA proj3: TSP TABU Search - Oskar Szubert: -----------------')

    input_method = int(input('------------Choose input method: \n\t[ 1 ] From single file\n\t[ 2 ] From all file in specific dir\n\t[ 3 ] Generate random graph\nYour choice: '))

    while input_method != 1 and input_method != 2 and input_method != 3:
        input_method = int(input('Wrong choice try again: '))

    if not os.path.exists('results'):
        os.makedirs('results')

    result_filename = input('Save result as: ')
    result_filename = 'results/' + result_filename + '.csv'
    result_file = open(result_filename, 'w')

    time = Time()

    if input_method == 1:
        batch = single_file()
    if input_method == 2:
        batch = multiple_file()
    if input_method == 3:
        batch = generate_graph()
        
    iteration = int(input('Type number of iteration: '))
    population_size = int(input('Type population size greater than 0: '))
    arena_size = int(input('Type aerna size greater than 0: '))
    muatation_ratio = int(input('To ACTIVATE muatation type percent [0-100]  '))   
    crossover_ratio = int(input('To ACTIVATE crossover type percent [0-100]  '))   

    for graph in batch:
        genetic = Genetic(graph)
        genetic.set_genetic_properties(iteration, population_size, arena_size, muatation_ratio, crossover_ratio)
        time.start()

        genetic.genetic()

        time.stop()

        print('\n-----------------------------------------------------------')

        print_graph(graph)
        genetic.print()
        print('Time = {0:8f} [sec] '.format( time.result))
                

        time_as_str =  '{0:7f}'.format(time.result)
        result_file.write('(')
        result_file.write(str(len(graph[0])) +',')
        result_file.write(time_as_str)
        result_file.write(') -- ')
        result_file.write(str(genetic.global_best_cost) + '\n')

        del time.result

           
    result_file.close()


def single_file():
    batch = []
    filename = input('Enter filename in your local dir: ')
    file = GraphFromFile(filename)
    batch.append(file.graph)
    return batch

def single_file_remote(filename):
    batch = []
    file = GraphFromFile(filename)
    batch.append(file.graph)
    return batch

def multiple_file():
    batch = []
    dir_name =input("Enter dir name: ") + '/'

    for filename in os.listdir(dir_name):
        file = GraphFromFile(dir_name + filename)
        graph = file.graph
        batch.append(graph)

def multiple_file_remote(dir_name):
    batch = []

    for filename in os.listdir(dir_name):
        file = GraphFromFile(dir_name + filename)
        graph = file.graph
        batch.append(graph)

    return batch

def generate_graph():
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

def print_graph(graph):
    number_of_vertex = len(graph[0])
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

def automatic_test():
    filename = 'tsp.txt'
    batch = single_file_remote(filename)

    for graph in batch:
        genetic = Genetic(graph)
        genetic.set_genetic_properties(10000 ,70, 10, 1, 80)
        genetic.genetic()
        genetic.print()
    
def automatic_test_2():
    iteration_tab = [100,500,1000]
    cadency_tab = [50, 100]
    diversification_tab = [0,100]
    aspiration_ratio = [0, 0.9]

    iteration_tab = [100,300]
    cadency_tab = [5,20]
    diversification_tab = [0, 30]
    aspiration_ratio = [0, 0.9]


    batch = multiple_file_remote('examp/ATSP/')


    if not os.path.exists('results/ATSP/'):
        os.makedirs('results/ATSP/')
    time = Time()

    for iters in iteration_tab:
        for cad in cadency_tab:
            for div in diversification_tab:
                for ratio in aspiration_ratio:

                    result_filename = 'results/ATSP/' + str(iters) + '_' + str(cad) + '_'  + str(div) + '_'  + str(ratio) + '.csv'
                    result_file = open(result_filename, 'w')
                    for graph in batch:
                        tabu = TabuSearch(graph)
                        tabu.set_tabu_properties(iters ,cad, div, ratio)
                        time.start()
                        tabu.tabu()
                        time.stop()


                        time_as_str =  '{0:7f}'.format(time.result)

                        result_file.write(str(len(graph[0])) +',')
                        result_file.write(' && ')
                        result_file.write(time_as_str)
                        result_file.write(' && ')
                        result_file.write(str(tabu.global_best_cost) )
                        result_file.write(' && ')

                        result_file.write(str(iters))
                        result_file.write(' && ')
                        result_file.write(str(cad))
                        result_file.write(' && ')
                        result_file.write(str(div))
                        result_file.write(' && ')
                        result_file.write(str(ratio))
                        result_file.write(' && \\\\ \n')

                        del time.result
                    result_file.close()
