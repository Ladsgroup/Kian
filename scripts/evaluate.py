import argparse
import codecs
import os

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import kian.fitness
from kian import TrainedModel

parser = argparse.ArgumentParser(description='Evaluate a trained model')
parser.add_argument('--name', '-n', nargs='?', required=True,
                    help='name of the model to train')
args = parser.parse_args()

model = TrainedModel.from_file(args.name)
file_path = os.path.join(model.data_directory, 'res2.dat')

if not os.path.isfile(file_path):
    raise ValueError('You should train the model first')
with codecs.open(file_path, 'r', 'utf-8') as f:
    cv_set = eval(f.read())
AUC = kian.fitness.AUC(cv_set)

first_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 1)
second_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.5)
third_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.25)

print('AUC of the classifier: {0:.4}'.format(AUC))
print('First thrashhold (recall and precision): %s (%s, %s)' %
      (first_thrashhold[0], first_thrashhold[1][0], first_thrashhold[1][1]))
print('Second thrashhold (recall and precision): %s (%s, %s)' %
      (second_thrashhold[0], second_thrashhold[1][0],
       second_thrashhold[1][1]))
print('Third thrashhold (recall and precision): %s (%s, %s)' %
      (third_thrashhold[0], third_thrashhold[1][0], third_thrashhold[1][1]))
