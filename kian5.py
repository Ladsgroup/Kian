import codecs
base_dir = '/data/project/dexbot/pywikipedia-git/'
f = codecs.open('%scats2.txt' % base_dir, 'r', 'utf-8')
a = f.read()
f.close()
a = a.replace('[', '(').replace(']', ')')
a = eval(u'[%s]' % a[2:])
dict_a = {}
dst = []
for i in a:
    if not i[:-1] in dict_a:
        dict_a[i[:-1]] = i[-1]
    else:
        dst.append(i[:-1])
        print dict_a[i[:-1]], i[-1], i[:-1]

a = []
for i in dict_a:
    if i in dst:
        continue
    a.append(list(i) + [dict_a[i]])
f = codecs.open('%skian5.txt' % base_dir, 'w', 'utf-8')
f.write(str(a))
f.close()
