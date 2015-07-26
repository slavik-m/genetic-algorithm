__author__ = 'ViS'

import genetic_algorithm
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument("-fn", "--fn", dest="fitness_fn", help="Fitness function")
parser.add_argument("-min", "--min", dest="min", default=0, help="Minimum value", type=int)
parser.add_argument("-max", "--max", dest="max", default=10, help="Maximum value", type=int)
parser.add_argument("-s", "--step", dest="step", default=0.1, help="Step", type=float)
parser.add_argument("-p", "--population", dest="population_count", default=20, help="Population count", type=int)
parser.add_argument("-st", "--seltype", dest="selection_type", default="TOURNEY", help="Selection type")

args = parser.parse_args()

# fitness_fn = '1/4*(x**4)-8/3*(x**3)+19/2*(x**2)-12*x+10'
fitness_fn = args.fitness_fn

OPTIONS = {
    'min': args.min,
    'max': args.max,
    'step': args.step,
    'population_count': args.population_count,
    'selection_type': args.selection_type
}

result = genetic_algorithm.calculate(fitness_fn, OPTIONS)

print(json.dumps(result, default=lambda o: o.__dict__))