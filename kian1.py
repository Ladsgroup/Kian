import codecs
base_dir = '/data/project/dexbot/pywikipedia-git/'
a = []
name = None
cats = {}
f = codecs.open('%sen_kian2.txt' % base_dir, 'r', 'utf-8')
aa2 = f.read().split('\n')
f.close()
for line in aa2:
    try:
        if int(line.split('\t')[1]) == 0:
            continue
    except:
        continue
    cats[line.split('\t')[0]] = [int(line.split('\t')[1]), 0, None]
f = codecs.open('%sHuman.txt' % base_dir, 'r', 'utf-8')
humans = set(f.read().split('\n'))
f.close()
c = 0


def check(name, list_of_ctas):
    global c
    if name in humans:
        c += 1
        for cat in list_of_ctas:
            if cat in cats:
                cats[cat][1] += 1
            else:
                print list_of_ctas
    f.close()
with codecs.open('%sen_kian.txt' % base_dir, 'r', 'utf-8') as najme:
    for line in najme:
        line = line.replace('\n', '')
        try:
            line.split("\t")[1]
        except:
            continue
        if name and name != line.split("\t")[0]:
            check(name, a)
            a = []
        name = line.split("\t")[0]
        a.append(line.split("\t")[1])
vals = []
vals2 = []
for cat in cats:
    cats[cat][2] = cats[cat][1] * 100.0 / cats[cat][0]
    vals.append(cats[cat][2])
    if int(cats[cat][2]) not in [100, 0]:
        vals2.append(cats[cat][2])
vals.sort()
vals2.sort()
f = codecs.open('%skian1_1.txt' % base_dir, 'w', 'utf-8')
f.write(str(cats))
f.close()
f = codecs.open('%skian1_2.txt' % base_dir, 'w', 'utf-8')
f.write(str(vals))
f.close()
f = codecs.open('%skian1_3.txt' % base_dir, 'w', 'utf-8')
f.write(str(vals2))
f.close()
