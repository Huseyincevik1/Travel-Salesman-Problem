import random

# Şehir koordinatlarını oku
with open('tsp_124_1.txt') as f:
    lines = f.readlines()
    city_locations = []
    for line in lines[1:]:  # ilk satırı atlayarak diğerlerini okuyoruz
        parts = line.strip().split(' ')
        city_locations.append((float(parts[0]), float(parts[1])))


# Sabitler
POPULATION_SIZE = 50
ELITISM_RATIO = 0.1
MUTATION_PROBABILITY = 0.1
NUM_GENERATIONS = 1000

# Yardımcı fonksiyonlar
def calculate_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def calculate_fitness(individual):
    total_distance = 0
    for i in range(len(individual)):
        total_distance += calculate_distance(city_locations[individual[i - 1]], city_locations[individual[i]])
    return 1 / total_distance

def create_individual(num_cities):
    individual = list(range(num_cities))
    random.shuffle(individual)
    return individual

def create_population(population_size, num_cities):
    population = []
    for i in range(population_size):
        individual = create_individual(num_cities)
        population.append(individual)
    return population

def select_parents(population):
    sorted_population = sorted(population, key=calculate_fitness, reverse=True)
    num_parents = int(len(sorted_population) * ELITISM_RATIO)
    parents = sorted_population[:num_parents]
    for individual in sorted_population[num_parents:]:
        if random.random() < 0.5:
            parents.append(individual)
    return parents

def crossover(parent1, parent2):
    start = random.randint(0, len(parent1) - 1)
    end = random.randint(start, len(parent1) - 1)
    child = [-1] * len(parent1)
    for i in range(start, end + 1):
        child[i] = parent1[i]
    j = 0
    for i in range(len(parent2)):
        if not parent2[i] in child:
            while child[j] != -1:
                j += 1
            child[j] = parent2[i]
    return child

def mutate(individual):
    if random.random() < MUTATION_PROBABILITY:
        i = random.randint(0, len(individual) - 1)
        j = random.randint(0, len(individual) - 1)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def evolve_population(population):
    parents = select_parents(population)
    num_children = len(population) - len(parents)
    children = []
    while len(children) < num_children:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = crossover(parent1, parent2)
        child = mutate(child)
        children.append(child)
    parents.extend(children)
    return parents

# Başlangıç populasyonunu oluştur
num_cities = len(city_locations)
population = create_population(POPULATION_SIZE, num_cities)

# Genetik algoritma döngüsü
for i in range(NUM_GENERATIONS):
    population = evolve_population(population)
    best_individual = max(population, key=calculate_fitness)


best_individual = max(population, key=calculate_fitness)
best_distance = 1 / calculate_fitness(best_individual)
best_route = [city_locations[i] for i in best_individual]
print('Best distance:', best_distance)
print('Best route:', best_route)

