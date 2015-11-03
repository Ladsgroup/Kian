import argparse
import pywikibot
import sys
import codecs
import os
from pywikibot import pagegenerators
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import kian.fitness
from kian import TrainedModel
from kian import Kian


def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Parse and add statements '
                                     'based on trained model')
    parser.add_argument('--name', '-n', nargs='?', required=True,
                        help='name of the model to train')
    parsed_args = parser.parse_known_args(args)[0]

    model = TrainedModel.from_file(parsed_args.name)
    model.load()
    file_path = os.path.join(model.data_directory, 'res2.dat')

    if not os.path.isfile(file_path):
        raise ValueError('You should train the model first')
    with codecs.open(file_path, 'r', 'utf-8') as f:
        cv_set = eval(f.read())
    first_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 1)[0]
    second_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.5)[0]
    second_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.25)[0]
    pywikibot.output('1st, 2nd, and 3rd thrashholds are: %s, %s, %s' %
                     (first_thrashhold, second_thrashhold, second_thrashhold))
    local_args = pywikibot.handle_args(args)
    genFactory = pagegenerators.GeneratorFactory()
    for arg in local_args:
        genFactory.handleArg(arg)
    generator = genFactory.getCombinedGenerator()
    for page in generator:
        cats = [cat.title(underscore=True, withNamespace=False)
                for cat in page.categories()]
        features = model.label_case(cats)
        res = Kian.kian(model.theta, features)[0]
        pywikibot.output(page.title(), res)


if __name__ == "__main__":
    main()
