import random
from fitness import Fitness

class GA:
    def __init__(self, population, population_size, elite_size, mutation_rate, generations):
        self.initial_pop = self.generate_initial_pop(population_size, population)
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def create_random_route(self, city_list):
        route = random.sample(city_list, len(city_list))
        return route

    def generate_initial_pop(self, size, pop):
        population = []
        for i in range(0, size):
            population.append(self.create_random_route(pop))
        return population

    def rank_routes(self, population):
        fitness_results = {}
        for i in range(0, len(population)):
            fitness_results[i] = Fitness(population[i]).route_fitness()
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)

    def selection(self, pop_ranked):
        selection_results = []

        for i in range(0, self.elite_size):
            selection_results.append(pop_ranked[i][0])

        probabilities = [i[1] for i in pop_ranked]
        probabilities = [i / sum(probabilities) for i in probabilities]

        temp_selection = random.choices(pop_ranked, weights=probabilities, k=len(pop_ranked) - self.elite_size)
        temp_selection = [i[0] for i in temp_selection]
        selection_results = selection_results + temp_selection
        return selection_results

    def mating_pool(self, population, selection_results):
        matingpool = []
        for i in range(0, len(selection_results)):
            index = selection_results[i]
            matingpool.append(population[index])
        return matingpool

    def breed(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        start_gene = min(geneA, geneB)
        end_gene = max(geneA, geneB)

        for i in range(start_gene, end_gene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]

        child = childP1 + childP2
        return child

    def breed_population(self, mating_pool):
        children = []
        length = len(mating_pool) - self.elite_size
        pool = random.sample(mating_pool, len(mating_pool))

        for i in range(0, self.elite_size):
            children.append(mating_pool[i])

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(mating_pool) - i - 1])
            children.append(child)
        return children

    def mutate(self, individual):
        for swapped in range(len(individual)):
            if random.random() < self.mutation_rate:
                swap_with = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swap_with]

                individual[swapped] = city2
                individual[swap_with] = city1
        return individual

    def mutate_population(self, population):
        mutated_pop = []

        for ind in range(0, len(population)):
            mutated_ind = self.mutate(population[ind])
            mutated_pop.append(mutated_ind)
        return mutated_pop

    def next_generation(self, current_gen):
        pop_ranked = self.rank_routes(current_gen)
        selection_results = self.selection(pop_ranked)
        mating_pool_ = self.mating_pool(current_gen, selection_results)
        children = self.breed_population(mating_pool_)
        next_generation = self.mutate_population(children)
        return next_generation

    def run(self):
        pop = self.initial_pop
        print("Initial random distance: " + str(1 / self.rank_routes(pop)[0][1]))

        for i in range(0, self.generations):
            pop = self.next_generation(pop)

        print("Final optimized distance: " + str(1 / self.rank_routes(pop)[0][1]))
        best_route_index = self.rank_routes(pop)[0][0]
        best_route = pop[best_route_index]
        return best_route


