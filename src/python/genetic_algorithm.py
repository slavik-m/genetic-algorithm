__author__ = 'ViS'

import random
import math
import itertools

M = 10


class Individual:
    def __init__(self, num, val, fitness):
        self.num = num
        self.val = val
        self.fitness = M - fitness


class Population:
    def __init__(self):
        self.individuals = []
        self.fitness_avg = 0

    def calculate_fitness_avg(self):
        sum = 0
        for i in self.individuals:
            sum += i.fitness
            self.fitness_avg = sum / len(self.individuals)


def calculate(fitness_fn, opt):
    opt['t'] = int(opt['min'] + opt['max'] / opt['step'])

    global gen_max_val, gen_count, M
    gen_max_val = 0

    def calculate_optimal():
        global gen_max_val, gen_count
        for i in range(1, 20):
            num = 2 ** i
            if (num - 1) >= opt['t']:
                gen_count = len(bin(num - 1)[2:])
                gen_max_val = num - 1
                break

    calculate_optimal()

    def generate_start_population(gen_max_val):
        population = Population()
        for i in range(0, opt['population_count']):
            val = random.randint(0, gen_max_val)
            x = val * opt['step']
            fitness = eval(fitness_fn)
            population.individuals.append(Individual(i, val, fitness))

        population.calculate_fitness_avg()
        return population

    def selection(population):
        individuals_offsprings = []
        if opt['selection_type'] == 'TOURNEY':
            for i in range(0, opt['population_count']):
                source_idx = random.randint(0, opt['population_count'] - 1)
                target_idx = random.randint(0, opt['population_count'] - 1)

                source = population.individuals[source_idx].fitness
                target = population.individuals[target_idx].fitness

                if source > target:
                    individuals_offsprings.insert(i, population.individuals[source_idx])
                else:
                    individuals_offsprings.insert(i, population.individuals[target_idx])

            return individuals_offsprings

    def pair_cross(individ_s, individ_t, cross_point):
        children = []

        first_part_source = bin(individ_s.val)[2:].zfill(gen_count)[0:cross_point]
        first_part_target = bin(individ_t.val)[2:].zfill(gen_count)[0:cross_point]

        second_part_source = bin(individ_s.val)[2:].zfill(gen_count)[cross_point:]
        second_part_target = bin(individ_t.val)[2:].zfill(gen_count)[cross_point:]

        val1 = first_part_source + second_part_target
        val2 = first_part_target + second_part_source

        x = int(val1, 2) * opt['step']
        fitness1 = eval(fitness_fn)

        x = int(val2, 2) * opt['step']
        fitness2 = eval(fitness_fn)

        child1 = Individual(0, int(val1, 2), fitness1)
        child2 = Individual(0, int(val2, 2), fitness2)

        children.append(child1)
        children.append(child2)

        return children

    def cross(individuals_offsprings, gen_count):
        new_population = Population()
        pair = []
        pair_count = int(opt['population_count'] / 2)
        next_idx = 0
        pc = 0.7  # Chance of crossing

        while pair_count > 0:
            for i in range(0, opt['population_count']):
                if random.random() < pc:
                    pair.append(individuals_offsprings[i])
                    next_idx = i + 1
                    break

            for i in range(next_idx, opt['population_count']):
                if random.random() < pc:
                    if len(pair) > 1:
                        if (pair[1]) == individuals_offsprings[i]:
                            pair.insert(1, individuals_offsprings[i])
                        else:
                            i = 0
                        break
                    else:
                        pair.insert(1, individuals_offsprings[i])

            children = pair_cross(pair[0], pair[1], int(math.floor(random.random() * (gen_count - 1) + 1)))
            new_population.individuals.append(children)

            pair_count -= 1

        new_population.individuals = list(itertools.chain.from_iterable(new_population.individuals))
        for i in range(0, opt['population_count']):
            new_population.individuals[i].num = i

        new_population.calculate_fitness_avg()

        return new_population

    def mutation_gen(undividual, mutagen):
        if undividual[mutagen] == '1':
            undividualSrt = undividual[0:mutagen-1] + '0' + undividual[mutagen+1:]
        else:
            undividualSrt = undividual[0:mutagen-1] + '1' + undividual[mutagen+1:]

        return undividualSrt

    def mutation(population):
        Pm = 0.3  # Chance of mutation
        new_population = Population()

        for i in range(0, opt['population_count']):
            if random.random() < Pm:
                mutagen = int(math.floor(random.random() * (gen_count - 1)))
                val = int(mutation_gen(bin(population.individuals[i].val)[2:].zfill(gen_count), mutagen), 2)

                x = val * opt['step']
                fitness = eval(fitness_fn)

                new_population.individuals.insert(i, Individual(i, val, fitness))
            else:
                new_population.individuals.insert(i, population.individuals[i])

        new_population.calculate_fitness_avg()
        return new_population

    def start():
        population = generate_start_population(gen_max_val)
        start_population = population
        selection_population = Population()
        cross_population = Population()
        mutation_population = Population()

        coefZ = 4

        population_chache = []
        stop = False

        for t in range(0, opt['t'] * 2):
            selection_population = selection(population)
            cross_population = cross(selection_population, gen_count)

            population_chache.insert(t % coefZ, cross_population.fitness_avg)

            if len(population_chache) > 3:
                if population_chache[0] == population_chache[1] and population_chache[1] == population_chache[2] and \
                                population_chache[2] == population_chache[3]:
                    stop = True

            if stop:
                population = cross_population
                break

            if t != (opt['t'] * 2 - 1):
                mutation_population = mutation(cross_population)
                population = mutation_population

            else:
                population = cross_population
                population_chache[t % coefZ or 0] = population.fitness_avg

        for i in range(1, opt['population_count']):
            result = population.individuals[0].val
            temp = population.individuals[0].fitness

            if temp < population.individuals[i].fitness:
                temp = population.individuals[i].fitness
                result = population.individuals[i].val

        return {
            "start_population": start_population,
            "population": population,
            "x": result * opt['step']
        }

    return start()
