import numpy
import random

class Population:
    def __init__(self, machines, processes, pop_size, chromosome_rate, mutation_rate):
        self.pop_size = pop_size
        self.machines = machines
        self.processes = processes
        self.m = len(machines)
        self.n = len(processes)
        population = []
        for i in range(pop_size):
            chrome = [random.randint(0, self.m-1) for i in range(self.n)]
            population.append(chrome)

        print(population)
        self.population = population
        self.chromosome_rate = chromosome_rate
        self.mutation_rate = mutation_rate
    
    def mutate(self, individu: list):
        new_ind = individu.copy()
        pos = random.randint(0, self.n-1)
        changed = random.randint(0, self.m-1)
        while (changed == new_ind[pos]):
            changed = random.randint(0, self.m-1)
        new_ind[pos] = changed
        return new_ind

    def mutation(self):
        new_ind = []
        for individu in self.population:
            if (random.random() <= self.chromosome_rate):
                new_ind.append(self.mutate(individu))
        self.population.extend(new_ind)
    
    def crossover(self, ind1, ind2):

        split_point = random.randint(0, self.n-1)
        left_ind1 = ind1[:split_point]
        right_ind1 = ind1[split_point:]
        left_ind2 = ind2[:split_point]
        right_ind2 = ind2[split_point:]

        child1 = left_ind1 + right_ind2
        child2 = left_ind2 + right_ind1
        return [child1, child2]
    def reproduce(self):
        new_ind =[]
        for individu in self.population:
            if (random.random() <=self.mutation_rate):
                new_ind.append(individu)
        
        random.shuffle(new_ind)
        child = []
        for i in range(len(new_ind)):
            for j in range(len(new_ind)):
                child.extend(self.crossover(new_ind[i], new_ind[j]))
        self.population.extend(child)

    def fitness(self, individu):
        length = [0] * self.m
        for task, gen in enumerate(individu):
            p = self.processes[task]
            m_ = self.machines[gen]
            ex_time = p['processLength']/m_['speed']
            length[gen] += ex_time
        return max(length)

    def selection(self):
        fitn = []
        for ind in self.population:
            fitn.append((self.fitness(ind), ind))
        
        fitn.sort()
        fitn = fitn[:self.pop_size]
        self.population = [ind for _, ind in fitn]

    def formatted(self):
        return {
            'machines': self.machines,
            'processes': self.processes,
            'population': self.population,
            'fitness' : [self.fitness(x) for x in self.population]
        }

    def generate(self, max_iter):
        for i in range(max_iter):
            self.reproduce()
            self.mutation()
            self.selection()
        return self.formatted()