import codecs
a = []
name = None
base_dir = '/data/project/dexbot/pywikipedia-git/'
f = codecs.open('%skian1_1.txt' % base_dir, 'r')
cats = eval(f.read())
f.close()
f = codecs.open('%scats2.txt' % base_dir, 'w', 'utf-8')
f.write('')
f.close()
f = codecs.open('%sHuman.txt' % base_dir, 'r', 'utf-8')
humans = set(f.read().split('\n'))
f.close()
f = codecs.open('%sNotHuman.txt' % base_dir, 'r', 'utf-8')
n_humans = set(f.read().split('\n'))
f.close()
li = set()


def check(name, list_of_ctas):
    words = [u'fictional', u'duos', 'trios', 'bands',
             'deities', 'men', 'women', 'people', 'births', 'deaths']
    set_of = ([0] * 11) + ([0] * len(words)) + [0]
    if name in n_humans:
        pass
    else:
        if name in humans:
            set_of[-1] = 1
        else:
            return
    for cat in list_of_ctas:
        n_cat = '_' + cat.lower().replace('category:', '') + '_'
        if cat in cats:
            a = cats[cat][2]
            if not a:
                set_of[0] += 1
            elif a <= 10.0:
                set_of[1] += 1
            elif a <= 20.0:
                set_of[2] += 1
            elif a <= 30.0:
                set_of[3] += 1
            elif a <= 40.0:
                set_of[4] += 1
            elif a <= 50.0:
                set_of[5] += 1
            elif a <= 60.0:
                set_of[6] += 1
            elif a <= 70.0:
                set_of[7] += 1
            elif a <= 80.0:
                set_of[8] += 1
            elif a <= 90.0:
                set_of[9] += 1
            else:
                set_of[10] += 1
            for i, word in enumerate(words):
                if u'_%s_' % word in n_cat:
                    set_of[11 + i] += 1

    if not tuple(set_of) in li:
        li.add(tuple(set_of))
        f = codecs.open('%scats2.txt' % base_dir, 'a', 'utf-8')
        f.write(',\n%s' % str(set_of))
        f.close()
print 'Starting'
name = None
with codecs.open('%sen_kian.txt' % base_dir, 'r', 'utf-8') as najme:
    for line in najme:
        line = line.replace('\n', '')
        try:
            line.split('\t')[1]
        except:
            continue
        if name and name != line.split("\t")[0]:
            check(name, a)
            a = []
        name = line.split("\t")[0]
        a.append(line.split("\t")[1])
