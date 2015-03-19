import math
import random
import codecs
#import scipy, numpy
#I used to use BFGS method but I really don't want dependencies.
no_iter = 500
J_history = []
delta = []
alpha = 0.1
epi = 0.2
base_dir = '/data/project/dexbot/pywikipedia-git/'
f = codecs.open('%skian5.txt' % base_dir, 'r', 'utf-8')
training_set = eval(f.read())
f.close()
y_k = 0
# backward compatability
if isinstance(training_set[0][-1], int):
    y_k = 1
else:
    y_k = len(training_set[0][-1])
arch = [len(training_set[0]), y_k]
arch2 = [len(training_set[0]), len(training_set[0])]
print "Working on a training set size of %d" % len(training_set)
cv_set = random.sample(training_set, len(training_set)/5)
training_set2 = [x for x in training_set if x not in cv_set]
training_set = training_set2[:]


def forward(a, theta):
    sum_i = []
    for i in range(len(theta)):
        sum_i_2 = 0
        for j in range(len(a)):
            sum_i_2 += a[j]*theta[i][j]
        sum_i.append(sum_i_2)
    return sum_i


def backward(delta, theta, a):
    res = []
    for i in range(len(theta[0])):
        sum_i = 0.0
        for j in range(len(theta)):
            sum_i += theta[j][i]*delta[j]*a[i]*(1-a[i])
        res.append(sum_i)
    return res


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
m = len(training_set)


def cost_function(theta, training_set, reg=True, lambda_para=1):
    sum_cos = 0
    m = len(training_set)
    for case in training_set:
        y = kian(theta, case[:-1])
        if isinstance(case[-1], int):
            case[-1] = [case[-1]]
        for i in range(len(y)):
            sum_cos -= case[-1][i]*math.log(y[i]) + \
                (1-case[-1][i])*math.log(1-y[i])
    sum_cos = sum_cos/m
    if reg:
        for i in range(2):
            for j in range(len(theta[i])):
                for k in range(len(theta[i][j])):
                    if not k or not j:
                        sum_cos += (lambda_para*theta[i][j][k]*theta[i][j][k])/(2*m)  # noqa
    return sum_cos
lambda_para = 0.0005
J_cv_history = []
lambda_history = []
theta_history = []
while True:
    if len(J_cv_history) > 1 and J_cv_history[-1] > J_cv_history[-2]:
        break
    lambda_para *= 1.62
    print lambda_para
    theta = [[]]*2
    J_history = []
    for i in range(2):
        theta[i] = [[]]*arch[i]
        for j in range(len(theta[i])):
            theta[i][j] = [[]]*arch2[i]
            for k in range(len(theta[i][j])):
                theta[i][j][k] = (random.random()*epi*2) - epi
    for i in range(no_iter):
        J = cost_function(theta, training_set, lambda_para=lambda_para)
        J_history.append(J)
        Delta = [[]]*2
        for ii in range(2):
            Delta[ii] = [[]]*arch[ii]
            for j in range(len(Delta[ii])):
                Delta[ii][j] = [[]]*arch2[ii]
                for k in range(len(Delta[ii][j])):
                    Delta[ii][j][k] = 0
        D = Delta[:]
        for case in training_set:
            z = [[]]*3
            a = [[]]*3
            delta = [[]]*3
            a[0] = [1] + case[:-1]
            z[1] = forward(a[0], theta[0])
            a[1] = [1] + [sigmoid(ii) for ii in z[1]][1:]
            z[2] = forward(a[1], theta[1])
            a[2] = [sigmoid(ii) for ii in z[2]]
            delta[2] = [a[2][ii] - case[-1][ii] for ii in range(len(case[-1]))]
            delta[1] = backward(delta[2], theta[1], a[1])
            for ii in range(2):
                for j in range(len(Delta[ii])):
                    for k in range(len(Delta[ii][j])):
                        Delta[ii][j][k] += delta[ii+1][j]*a[ii][k]
        for ii in range(2):
            for j in range(len(Delta[ii])):
                for k in range(len(Delta[ii][j])):
                    D[ii][j][k] = (1.0/m)*Delta[ii][j][k]
                    if not j or not k:
                        D[ii][j][k] += lambda_para*theta[ii][j][k]
        for ii in range(2):
            for j in range(len(Delta[ii])):
                for k in range(len(Delta[ii][j])):
                    theta[ii][j][k] -= alpha*D[ii][j][k]
    J_cv_history.append(cost_function(theta, cv_set, False))
    lambda_history.append(lambda_para)
    theta_history.append(theta)
#    print scipy.minimize(
#        cost_function, unrolled_theta, method='BFGS',
#        jac=lambda unrolled_theta: unrolled_D, options={'disp': True}))
d_theta = 0.00001
theta[0][1][1] += d_theta
dl1 = cost_function(theta, training_set)
theta[0][1][1] -= 2*d_theta
dl2 = cost_function(theta, training_set)
print D[0][1][1], (dl1 - dl2)/(2*d_theta)
theta = theta_history[-2]
res_the = {0: [], 1: []}
for case in training_set:
    print kian(theta, case[:-1])[0], case[-1], case[:-1]
    res_the[case[-1][0]].append(kian(theta, case[:-1])[0])
print J_history[:10], J_history[-10:]
print theta
f = codecs.open('%skian_res_lang.txt' % base_dir, 'w', 'utf-8')
f.write(str(res_the))
f.close()
