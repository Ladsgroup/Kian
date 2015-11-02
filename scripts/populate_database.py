import argparse
import sys
import codecs
import os
import MySQLdb

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
    print('Loading the model')
    model.load_data()
    model.load()
    file_path = os.path.join(model.data_directory, 'res2.dat')

    if not os.path.isfile(file_path):
        raise ValueError('You should train the model first')
    with codecs.open(file_path, 'r', 'utf-8') as f:
        cv_set = eval(f.read())
    first_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 1)[0]
    second_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.125)[0]
    print('Finding possible adds to human review')
    print(first_thrashhold, second_thrashhold)
    pros = model.wikidata_data_w | model.wikidata_data_wo
    print(len(pros))
    name = None
    a = []
    db = MySQLdb.connect(host="tools-db", db="s52709__kian_p",
                         read_default_file="~/replica.my.cnf")
    cursor = db.cursor()
    insert_statement = (
        "INSERT INTO kian "
        "(qid, model_name, wiki_name, property, value, status, prob) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    with model.wiki_data_file as f:
        for line in f:
            line = line.replace('\n', '')
            if u'\t' not in line:
                continue
            if name and name != line.split('\t')[0]:
                if name in pros:
                    a = []
                    name = line.split('\t')[0]
                    continue
                features = model.label_case(a)
                res = Kian.kian(model.theta, features)[0]
                if res > first_thrashhold and res < second_thrashhold:
                    cursor.execute(insert_statement,
                                   (name, model.name, model.wiki,
                                    model.property_name, model.value, 0,
                                    str(res)[:7]))
                a = []
            name = line.split('\t')[0]
            a.append(line.split('\t')[1])
    db.commit()
    cursor.close()
    db.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
