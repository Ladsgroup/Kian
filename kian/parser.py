from .model import Model

try:
    basestring
except NameError:
    import urllib.request as urllib2
    import pymysql as MySQLdb
else:
    import urllib2
    import MySQLdb

import codecs
import os
import json


class ModelWithData(Model):
    """docstring for ModelWithData"""
    def __init__(self, *args, **kwargs):
        super(ModelWithData, self).__init__(*args, **kwargs)

    def retrieve_statements_w(self):
        url = "http://tools.wmflabs.org/autolist/index.php?wdq=claim[" \
            "{statemnt}:{value}]_and_link[{wiki}]&run=Run&download=1"
        res = urllib2.urlopen(
            url.format(statemnt=self.property_name[1:],
                       value=self.value[1:],
                       wiki=self.wiki)).read().decode('utf-8')
        return set(res.split('\n'))

    def retrieve_statements_wo(self):
        url = "http://tools.wmflabs.org/autolist/index.php?wdq=claim[" \
            "{statemnt}]_and_noclaim[{statemnt}:{value}]_and_link[{wiki}]" \
            "&run=Run&download=1"
        res = urllib2.urlopen(
            url.format(statemnt=self.property_name[1:],
                       value=self.value[1:],
                       wiki=self.wiki)).read().decode('utf-8')
        res_set = set(res.split('\n'))
        if hasattr(self, 'bias_unit'):
            url = "http://tools.wmflabs.org/autolist/index.php?wdq={bias}" \
                  "_and_noclaim[{statemnt}:{value}]_and_link[{wiki}]" \
                  "&run=Run&download=1"
            res = urllib2.urlopen(
                url.format(statemnt=self.property_name[1:],
                           value=self.value[1:], bias=self.bias_unit,
                           wiki=self.wiki)).read().decode('utf-8')
        return set(res.split('\n')) | res_set

    def sql_query(self, cnf_file='~/replica.my.cnf', host='labsdb'):
        query = "SELECT pp_value, cl_to FROM page_props JOIN categorylinks " \
            "ON pp_page = cl_from JOIN page ON cl_from = page_id WHERE " \
            "pp_propname = 'wikibase_item' AND page_namespace=0 AND " \
            "page_is_redirect=0;"
        conn = MySQLdb.connect('%s.%s' % (self.wiki, host),
                               db='%s_p' % self.wiki,
                               read_default_file=cnf_file,
                               charset='utf8',
                               use_unicode=True)
        cursor = conn.cursor()
        print('Executing the query')
        cursor.execute(query)
        return cursor.fetchall()

    def sql_query2(self, cnf_file='~/replica.my.cnf', host='labsdb'):
        query = "SELECT cl_to, count(*) FROM categorylinks GROUP BY cl_to;"
        conn = MySQLdb.connect('%s.%s' % (self.wiki, host),
                               db='%s_p' % self.wiki,
                               read_default_file=cnf_file,
                               charset='utf8',
                               use_unicode=True)
        cursor = conn.cursor()
        print('Executing the query')
        cursor.execute(query)
        return cursor.fetchall()

    def load_cats(self, wiki_path):
        self.categories = {}
        if os.path.isfile(wiki_path):
            with codecs.open(wiki_path, 'r', 'utf-8') as f:
                for line in f:
                    line = line.replace('\n', '').split('\t')
                    if len(line) != 2:
                        continue
                    self.categories[line[0]] = [int(line[1]), 0, 0]

    def load_data(self, reload_wiki=False, reload_wikidata=False,
                  load_cats=True):
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)
        wiki_data_dir = os.path.join(self.data_directory, os.pardir,
                                     '.wiki_data')
        if not os.path.isdir(wiki_data_dir):
            os.makedirs(wiki_data_dir)
        wiki_path = os.path.join(wiki_data_dir, self.wiki + '.dat')
        if os.path.isfile(wiki_path) and not reload_wiki:
            self.wiki_data_file = codecs.open(wiki_path, 'r', 'utf-8')
        wiki_path = os.path.join(wiki_data_dir, self.wiki + '2.dat')
        if load_cats and not reload_wiki:
            self.load_cats(wiki_path)
        file_path = os.path.join(self.data_directory, 'with_statemnts.dat')
        if os.path.isfile(file_path) and not reload_wikidata:
            with codecs.open(file_path, 'r', 'utf-8') as f:
                self.wikidata_data_w = set(f.read().split('\n'))
        file_path = os.path.join(self.data_directory, 'without_statemnts.dat')
        if os.path.isfile(file_path) and not reload_wikidata:
            with codecs.open(file_path, 'r', 'utf-8') as f:
                self.wikidata_data_wo = set(f.read().split('\n'))

    def retrieve_data(self, reload_wiki=False, reload_wikidata=False):
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)
        if reload_wiki or not hasattr(self, 'wiki_data'):
            wiki_data_dir = os.path.join(self.data_directory, os.pardir,
                                         '.wiki_data')
            wiki_path = os.path.join(wiki_data_dir, self.wiki + '.dat')
            if not os.path.isfile(wiki_path):
                with codecs.open(wiki_path, 'w', 'utf-8') as f:
                    res = u''
                    for case in self.sql_query():
                        res += u'\t'.join([i.decode('utf-8') for i in case]) \
                            + '\n'
                    f.write(res)
            wiki_path = os.path.join(wiki_data_dir, self.wiki + '2.dat')
            if not os.path.isfile(wiki_path):
                with codecs.open(wiki_path, 'w', 'utf-8') as f:
                    res = u''
                    for case in self.sql_query2():
                        sql_row_res = [str(i).decode('utf-8') for i in case]
                        res += u'\t'.join(sql_row_res) + '\n'
                    f.write(res)
            self.categories = {}
            with codecs.open(wiki_path, 'r', 'utf-8') as f:
                for line in f:
                    line = line.replace('\n', '').split('\t')
                    if len(line) != 2:
                        continue
                    self.categories[line[0]] = [int(line[1]), 0, 0]

        if reload_wikidata or not hasattr(self, 'wikidata_data_w'):
            file_path = os.path.join(
                self.data_directory, 'with_statemnts.dat')
            self.wikidata_data_w = self.retrieve_statements_w()
            with codecs.open(file_path, 'w', 'utf-8') as f:
                f.write(u'\n'.join(self.wikidata_data_w))
            self.wikidata_data_w = set(self.wikidata_data_w)
            file_path = os.path.join(
                self.data_directory, 'without_statemnts.dat')
            self.wikidata_data_wo = self.retrieve_statements_wo()
            with codecs.open(file_path, 'w', 'utf-8') as f:
                f.write(u'\n'.join(self.wikidata_data_wo))
            self.wikidata_data_wo = set(self.wikidata_data_wo)

    def _check(self, name, list_of_cats):
        if name in self.wikidata_data_w:
            for cat in list_of_cats:
                if cat not in self.categories:
                    continue
                self.categories[cat][1] += 1
        elif name in self.wikidata_data_wo:
            for cat in list_of_cats:
                if cat not in self.categories:
                    continue
                self.categories[cat][2] += 1

    def label_case(self, list_of_cats):
        percents = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        x1 = [0] * len(percents)
        x2 = [0] * len(percents)
        for cat in list_of_cats:
            if cat not in self.categories:
                continue
            for i in range(len(percents)):
                percent1 = self.categories[cat][1] * 100.0 \
                    / self.categories[cat][0]
                percent2 = self.categories[cat][2] * 100.0 \
                    / self.categories[cat][0]
                upper = percents[i]
                lower = percents[i - 1]
                if i == 0:
                    if percent1 >= lower:
                        x1[i] += 1
                    if percent2 >= lower:
                        x2[i] += 1
                if percent1 >= lower and percent1 < upper:
                    x1[i] += 1
                if percent2 >= lower and percent2 < upper:
                    x2[i] += 1
        return x1 + x2

    def build_training_set(self, name, list_of_cats):
        y = None
        if len(self.training_set) > 30000:
            return
        if name in self.wikidata_data_w:
            y = [1]
        elif name in self.wikidata_data_wo:
            y = [0]
        else:
            return
        x = self.label_case(list_of_cats)
        self.training_set.add(tuple(x + y))

    def label_categories(self):
        if not (hasattr(self, 'wiki_data_file') and
                hasattr(self, 'wikidata_data_w') and
                hasattr(self, 'wikidata_data_wo') and
                hasattr(self, 'categories')):
            raise ValueError('You need to define enough data to label')

        name = None
        a = []
        with self.wiki_data_file as f:
            for line in f:
                line = line.replace('\n', '')
                if u'\t' not in line:
                    continue
                if name and name != line.split('\t')[0]:
                    self._check(name, a)
                    a = []
                name = line.split('\t')[0]
                a.append(line.split('\t')[1])
        self.training_set = set()
        t_f = self.wiki_data_file
        self.wiki_data_file = codecs.open(t_f.name, t_f.mode, 'utf-8')
        with self.wiki_data_file as f:
            for line in f:
                line = line.replace('\n', '')
                if u'\t' not in line:
                    continue
                if name and name != line.split('\t')[0]:
                    self.build_training_set(name, a)
                    a = []
                name = line.split('\t')[0]
                a.append(line.split('\t')[1])
        file_path = os.path.join(
            self.data_directory, 'categories.json')
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(json.dumps(self.categories))
        file_path = os.path.join(
            self.data_directory, 'training_set.dat')
        with codecs.open(file_path, 'w', 'utf-8') as f:
            f.write(str(self.training_set))
