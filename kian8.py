import codecs
import math
a = []
name = None
base_dir = '/data/project/dexbot/pywikipedia-git/'
f = codecs.open('%skian1_1.txt' % base_dir, 'r')
cats = eval(f.read())
f.close()
f = codecs.open('%spossible_mistakes.txt' % base_dir, 'w', 'utf-8')
f.write('')
f.close()
f = codecs.open('%sHuman.txt' % base_dir, 'r', 'utf-8')
humans = set(f.read().split('\n'))
f.close()
f = codecs.open('%sNotHuman.txt' % base_dir, 'r', 'utf-8')
n_humans = set(f.read().split('\n'))
f.close()
li = set()
theta = [[[-0.14330406290649209, 0.14160289488513547, 0.10058465151666317, 0.013335273369270819, 0.1622403666235688, -0.16420186888474528], [-0.2819467181519574, 0.6238360117119567, 0.014600272440078091, -0.0029178560269299486, -0.0751639593458717, -0.9419896081058511], [-0.06976938013653712, -0.281727417715928, -0.15070441686443145, 0.005347539499836222, 0.19852155407957514, 0.31748967583133586], [0.12212473323565698, -0.5003518179890775, -0.05909623012431725, 0.0138022520262144, 0.10154188503788891, 0.7875359404041361], [-0.06505917181680726, 0.6444301485203436, -0.021566046187735347, -0.014983647822043863, -0.13407276535934626, -0.8423034287174258], [0.19255055619423225, -0.45258433744364746, -0.12459293318750417, 0.0031583190104828678, 0.16378971782062612, 0.6742306720512257]], [[-0.42194750722903673, 2.124094005484356, -0.6687475205436897, -1.710919311901155, 1.98488304230357, -1.440489332552221]]]  # noqa


def forward(a, theta):
    sum_i = []
    for i in range(len(theta)):
        sum_i_2 = 0
        for j in range(len(a)):
            sum_i_2 += a[j]*theta[i][j]
        sum_i.append(sum_i_2)
    return sum_i


def sigmoid(a):
    return 1.0/(1 + math.exp(-1*a))


def kian(theta, case):
    z = [[]]*3
    a = [[]]*3
    a[0] = [1] + case
    z[1] = forward(a[0], theta[0])
    a[1] = [1] + [sigmoid(i) for i in z[1]][1:]
    z[2] = forward(a[1], theta[1])
    a[2] = [sigmoid(i) for i in z[2]]
    return a[2]


def check(name, list_of_ctas):
    set_of = [0, 0, 0, 0, 0, 0]
    if name in n_humans:
        pass
    else:
        if name in humans:
            set_of[-1] = 1
        else:
            return
    for cat in list_of_ctas:
        if cat in cats:
            a = cats[cat][2]
            if not a:
                set_of[-2] += 1
            elif a < 20.0:
                set_of[-3] += 1
            elif a <= 50.0:
                set_of[-4] += 1
            elif a <= 80.0:
                set_of[-5] += 1
            else:
                set_of[-6] += 1
    res = kian(theta, set_of[:-1])[0]
    if res > 0.36 and res < 0.90:
        return
    res2 = math.floor(res + 0.5)
    if res2 != set_of[-1]:
        f = codecs.open('%spossible_mistakes.txt' % base_dir, 'a', 'utf-8')
        f.write(
            '\n%s: %s (d), %s (w) %s' % (name, set_of[-1], res, set_of[:-1]))
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
