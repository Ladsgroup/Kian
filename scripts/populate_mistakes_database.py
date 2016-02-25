import argparse
import pywikibot
import sys
import codecs
import os

try:
    basestring
except NameError:
    import pymysql as MySQLdb
else:
    import MySQLdb

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import kian.fitness
from kian import TrainedModel
from kian import Kian

site = pywikibot.Site('wikidata', fam='wikidata')
repo = site.data_repository()


def store(name, res, wiki, p_number, value):
    item = pywikibot.ItemPage(repo, name)
    try:
        item.get()
    except pywikibot.NoPage:
        return False
    if wiki not in item.sitelinks:
        return False
    insert_statement = (
        "INSERT INTO kian_mistakes "
        "(qid, property, value, wiki_name, name_wiki, status, prob, wd_value) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    db = MySQLdb.connect(host="tools-db", db="s52709__kian_p",
                         read_default_file="~/replica.my.cnf", charset='utf-8')
    cursor = db.cursor()
    name = int(name.lower().replace('q', ''))
    wd_value = 1 if res < 0.5 else 0
    cursor.execute(insert_statement, (name, p_number, value, wiki,
                                      item.sitelinks[wiki], 0, res, wd_value))
    db.commit()
    cursor.close()
    db.close()
    print('Stored')
    return True


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
    second_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.125)[0]
    print('Finding possible mistakes')
    print(second_thrashhold)
    name = None
    a = []
    p_number = int(model.property_name.lower().replace('p', ''))
    q_number = int(model.value.lower().replace('q', ''))
    with model.wiki_data_file as f:
        for line in f:
            line = line.replace('\n', '')
            if u'\t' not in line:
                continue
            if name and name != line.split('\t')[0]:
                features = model.label_case(a)
                res = Kian.kian(model.theta, features)[0]
                if name in model.wikidata_data_w and \
                        res < (1 - second_thrashhold):
                    store(name, res, model.wiki, p_number, q_number)
                elif name in model.wikidata_data_wo and \
                        res > second_thrashhold:
                    store(name, res, model.wiki, p_number, q_number)
                a = []
            name = line.split('\t')[0]
            a.append(line.split('\t')[1])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
