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


def recent_changes_gen(site, client, max_pages=100000):
    c = 0
    rccontinue = None
    while c < max_pages:
        c += 500
        print(c)
        params = {
            'action': 'query',
            'list': 'recentchanges',
            'rclimit': 500,
            'rctype': 'new',
            'rcprop': 'title',
            'rcnamespace': '0',
        }
        if rccontinue:
            params['rccontinue'] = rccontinue
        res = pywikibot.data.api.Request(site=site, **params).submit()
        rccontinue = res['query-continue']['recentchanges']['rccontinue']
        ids = [case['title'] for case in res['query']['recentchanges']]
        params = {
            'action': 'wbgetentities',
            'ids': '|'.join(ids),
            'props': 'sitelinks',
            'sitefilter': client
        }
        res = pywikibot.data.api.Request(site=site, **params).submit()
        for case in res["entities"]:
            if client not in res["entities"][case].get("sitelinks", []):
                continue
            yield res["entities"][case]["sitelinks"][client]["title"]

sources = {
    'enwiki': 'Q328',
    'svwiki': 'Q169514',
    'dewiki': 'Q48183',
    'itwiki': 'Q11920',
    'nowiki': 'Q191769',
    'fawiki': 'Q48952',
    'eswiki': 'Q8449',
    'plwiki': 'Q1551807',
    'cawiki': 'Q199693',
    'frwiki': 'Q8447',
    'nlwiki': 'Q10000',
    'ptwiki': 'Q11921',
    'ruwiki': 'Q206855',
    'viwiki': 'Q200180',
    'bewiki': 'Q877583',
    'ukwiki': 'Q199698',
    'trwiki': 'Q58255',
    'cswiki': 'Q191168',
    'shwiki': 'Q58679',
    'jawiki': 'Q177837',
    'kowiki': 'Q17985',
    'fiwiki': 'Q175482',
    'huwiki': 'Q53464',
    'rowiki': 'Q199864',
    'zhwiki': 'Q30239',
    'ltwiki': 'Q202472',
    'srwiki': 'Q200386',
    'arwiki': 'Q199700',
    'skwiki': 'Q192582',
    'elwiki': 'Q11918',
    'hrwiki': 'Q203488',
    'mswiki': 'Q845993',
    'glwiki': 'Q841208',
    'euwiki': 'Q207260'}


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
    second_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.5)[0]

    site = pywikibot.site.APISite.fromDBName(model.wiki)
    repo = site.data_repository()
    repo.login()
    gen = recent_changes_gen(repo, model.wiki)
    for case in gen:
        page = pywikibot.Page(site, case)
        if page.namespace().id != 0:
            continue
        print(page)
        cats = [cat.title(underscore=True, withNamespace=False)
                for cat in page.categories()]
        features = model.label_case(cats)
        res = Kian.kian(model.theta, features)[0]
        if res > second_thrashhold:
            try:
                item = pywikibot.ItemPage.fromPage(page)
            except pywikibot.NoPage:
                continue
            if model.property_name in item.claims:
                continue
            claim = pywikibot.Claim(repo, model.property_name)
            claim.setTarget(pywikibot.ItemPage(repo, model.value))
            item.addClaim(claim, summary='Bot: Adding %s:%s from %s '
                          '([[User:Ladsgroup/Kian|Powered by Kian]])' %
                          (model.property_name, model.value, model.wiki))
            source = pywikibot.Claim(repo, 'P143')
            source.setTarget(pywikibot.ItemPage(repo, sources[model.wiki]))
            claim.addSource(source)

if __name__ == "__main__":
    main()
