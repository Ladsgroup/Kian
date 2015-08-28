import argparse
import pywikibot
import sys
import codecs
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import kian.fitness
from kian import TrainedModel
from kian import Kian

site = pywikibot.Site('wikidata', fam='wikidata')


def main():
    res_text = u"{| class=\"wikitable sortable\"\n!Qid!!Value<br />" \
        u"(Wikidata)!!Value<br />(Wipedia)!!Other boring stuff"
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
                    res_text += ("\n|-\n|[[%s]]||Yes||No (%s)||%s" %
                                 (name, res, features))
                elif name in model.wikidata_data_wo and \
                        res > second_thrashhold:
                    res_text += ("\n|-\n|[[%s]]||No||Yes (%s)||%s" %
                                 (name, res, features))
                a = []
            name = line.split('\t')[0]
            a.append(line.split('\t')[1])
    page_title = "User:Ladsgroup/Kian/Possible mistakes/%s" % model.name
    page = pywikibot.Page(site, page_title)
    page.put(res_text + "\n|}", "Bot: Report")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
