from database import DataBase
from fitness import Fitness
from city import City
from ga import GA
import itertools


# def create_route(city_list):
#     route = random.sample(city_list, len(city_list))
#     return route
#
#
# def initial_population(pop_size, city_list):
#     population = []
#
#     for i in range(0, pop_size):
#         population.append(create_route(city_list))
#     return population
#
# def rank_routes(population):
#     fitness_results = {}
#     for i in range(0, len(population)):
#         fitness_results[i] = Fitness(population[i]).route_fitness()
#     return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)
#
#
# def selection(pop_ranked, elite_size):
#     selection_results = []
#
#     for i in range(0, elite_size):
#         selection_results.append(pop_ranked[i][0])
#
#     probabilities = [i[1] for i in pop_ranked]
#     probabilities = [i/sum(probabilities) for i in probabilities]
#
#     temp_selection = random.choices(pop_ranked, weights=probabilities, k=len(pop_ranked) - elite_size)
#     temp_selection = [i[0] for i in temp_selection]
#     selection_results = selection_results + temp_selection
#     return selection_results
#
# def mating_pool(population, selection_results):
#     matingpool = []
#     for i in range(0, len(selection_results)):
#         index = selection_results[i]
#         matingpool.append(population[index])
#     return matingpool
#
#
# def breed(parent1, parent2):
#     child = []
#     childP1 = []
#     childP2 = []
#
#     geneA = int(random.random() * len(parent1))
#     geneB = int(random.random() * len(parent1))
#
#     start_gene = min(geneA, geneB)
#     end_gene = max(geneA, geneB)
#
#     for i in range(start_gene, end_gene):
#         childP1.append(parent1[i])
#
#     childP2 = [item for item in parent2 if item not in childP1]
#
#     child = childP1 + childP2
#     return child
#
#
# def breed_population(mating_pool, elite_size):
#     children = []
#     length = len(mating_pool) - elite_size
#     pool = random.sample(mating_pool, len(mating_pool))
#
#     for i in range(0, elite_size):
#         children.append(mating_pool[i])
#
#     for i in range(0, length):
#         child = breed(pool[i], pool[len(mating_pool) - i - 1])
#         children.append(child)
#     return children
#
#
# def mutate(individual, mutation_rate):
#     for swapped in range(len(individual)):
#         if (random.random() < mutation_rate):
#             swap_with = int(random.random() * len(individual))
#
#             city1 = individual[swapped]
#             city2 = individual[swap_with]
#
#             individual[swapped] = city2
#             individual[swap_with] = city1
#     return individual
#
#
# def mutate_population(population, mutation_rate):
#     mutated_pop = []
#
#     for ind in range(0, len(population)):
#         mutated_ind = mutate(population[ind], mutation_rate)
#         mutated_pop.append(mutated_ind)
#     return mutated_pop
#
# def next_generation(current_gen, elite_size, mutation_rate):
#     pop_ranked = rank_routes(current_gen)
#     selection_results = selection(pop_ranked, elite_size)
#     mating_pool_ = mating_pool(current_gen, selection_results)
#     children = breed_population(mating_pool_, elite_size)
#     next_generation = mutate_population(children, mutation_rate)
#     return next_generation
#
#
# def genetic_algorithm(population, pop_size, elite_size, mutation_rate, generations):
#     pop = initial_population(pop_size, population)
#     print("Initial distance: " + str(1 / rank_routes(pop)[0][1]))
#
#     for i in range(0, generations):
#         pop = next_generation(pop, elite_size, mutation_rate)
#
#     print("Final distance: " + str(1 / rank_routes(pop)[0][1]))
#     best_route_index = rank_routes(pop)[0][0]
#     best_route = pop[best_route_index]
#     return best_route

def brute_force(cities):
    a = itertools.permutations(cities)
    list_values = []
    for route in a:
        list_values.append(Fitness(route).route_distance())
    return min(list_values)


if __name__ == "__main__":
    db = DataBase("randomized_1.txt")
    cities_list = db.get_cities()
    cities = []
    for index, label in cities_list:
        cities.append(City(index, label, db))

    ga = GA(cities, 50, 5, 0.01, 1000)
    ga.run()

    # print(genetic_algorithm(population=cities, pop_size=200, elite_size=10, mutation_rate=0.01, generations=1000))
    # print(brute_force(cities))



