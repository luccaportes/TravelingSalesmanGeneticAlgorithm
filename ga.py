import random
from fitness import Fitness

class GA:
    def __init__(self, population, population_size, elite_size, mutation_rate, generations):
        self.initial_pop = self.generate_initial_pop(population_size, population)
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def create_random_route(self, city_list):
        # Gera uma rota randomica, é usada apenas para criar a população inicial
        route = random.sample(city_list, len(city_list))
        return route

    def generate_initial_pop(self, size, pop):
        # Apenas um for que vai criando um monte de rotas randomicas e pondo numa lista
        population = []
        for i in range(0, size):
            population.append(self.create_random_route(pop))
        return population

    def rank_routes(self, population):
        # Calcula o custo de cada rota e ranqueia do melhor(menor) pro pior(maior)
        fitness_results = {}
        for i in range(0, len(population)):
            fitness_results[i] = Fitness(population[i]).route_fitness()
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)

    def selection(self, pop_ranked):
        # Faz a seleção dos elementos que serão selecionados para a próxima geração
        selection_results = []

        # Seleciona os melhores(elite) para integrar a próxima geração
        for i in range(0, self.elite_size):
            selection_results.append(pop_ranked[i][0])

        # Depois que a elite já esta garantida, os próximos serão escolhidas quase aleatoriamente
        # quanto melhor(menor custo) o elemento for, maior a chance de ele ser escolhido
        probabilities = [i[1] for i in pop_ranked]
        probabilities = [i / sum(probabilities) for i in probabilities]

        temp_selection = random.choices(pop_ranked, weights=probabilities, k=len(pop_ranked) - self.elite_size)
        temp_selection = [i[0] for i in temp_selection]
        selection_results = selection_results + temp_selection
        return selection_results

    def mating_pool(self, population, selection_results):
        # seleciona da população atual, os selecionados para que possa ser feito o cruzamento
        matingpool = []
        for i in range(0, len(selection_results)):
            index = selection_results[i]
            matingpool.append(population[index])
        return matingpool

    def breed(self, parent1, parent2):
        # Cria um filho a partir de dois individuos
        child = []
        child_1 = []
        child_2 = []

        # pega aleatoriamente um indice pra fazer o cruzamento
        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        # o menor desses dois numeros gerados aleatoriamente vai ser o começo da troca e maior o fim
        start_gene = min(geneA, geneB)
        end_gene = max(geneA, geneB)

        # cria parte do filho com um dos pais
        for i in range(start_gene, end_gene):
            child_1.append(parent1[i])

        # cria a outra parte do filho com o resto do outro pai
        child_2 = [item for item in parent2 if item not in child_1]

        # junta os dois
        child = child_1 + child_2
        return child

    def breed_population(self, mating_pool):
        # apenas seleciona a elite e chama a função de cruzamento no resto
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
        # faz a mutação ou não em todos os individuos (aleatoriamente)
        for swapped in range(len(individual)):
            if random.random() < self.mutation_rate:
                swap_with = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swap_with]

                individual[swapped] = city2
                individual[swap_with] = city1
        return individual

    def mutate_population(self, population):
        # apenas chama a funcao de mutacao em todo mundo
        mutated_pop = []

        for ind in range(0, len(population)):
            mutated_ind = self.mutate(population[ind])
            mutated_pop.append(mutated_ind)
        return mutated_pop

    def next_generation(self, current_gen):
        # chama todas as outras funcoes pra pegar a proxima geraçao
        pop_ranked = self.rank_routes(current_gen)
        selection_results = self.selection(pop_ranked)
        mating_pool_ = self.mating_pool(current_gen, selection_results)
        children = self.breed_population(mating_pool_)
        next_generation = self.mutate_population(children)
        return next_generation

    def run(self):
        pop = self.initial_pop
        print("Initial randomized distance: " + str(1 / self.rank_routes(pop)[0][1]))

        for i in range(0, self.generations):
            pop = self.next_generation(pop)

        print("Final distance optimized: " + str(1 / self.rank_routes(pop)[0][1]))
        best_route_index = self.rank_routes(pop)[0][0]
        best_route = pop[best_route_index]
        return best_route


