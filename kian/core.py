import math
import random
import codecs
import os


class Kian(object):
    """Train the model"""
    def __init__(self, model=None, lambda_para=0.0005, no_iter=250,
                 alpha=0.1, epi=0.2, training_set=None, slow=False):
        if not model and not training_set:
            raise ValueError('You must define a model or training set')
        self.model = model
        self.lambda_para = lambda_para
        self.no_iter = no_iter
        self.alpha = alpha
        self.epi = epi
        self.J_cv_history = []
        self.lambda_history = []
        self.theta_history = []
        self.J_history = []
        self.delta = []
        self.slow = slow
        if not training_set:
            tr_path = os.path.join(self.model.data_directory,
                                   'training_set.dat')
            with codecs.open(tr_path, 'r', 'utf-8') as f:
                training_set_temp = eval(f.read())
        else:
            training_set_temp = training_set
        self.training_set = []
        for case in training_set_temp:
            self.training_set.append(list(case))
        if isinstance(self.training_set[0][-1], int):
            y_k = 1
        else:
            y_k = len(self.training_set[0][-1])
        self.arch = [len(self.training_set[0]), y_k]
        self.arch2 = [len(self.training_set[0]), len(self.training_set[0])]
        self.cv_set = random.sample(
            self.training_set, len(self.training_set) / 5)
        training_set2 = [x for x in self.training_set if x not in self.cv_set]
        self.training_set = training_set2[:]
        if len(self.training_set) > 30000 and not slow:
            self.training_set = random.sample(self.training_set, 30000)
        self.size = len(self.training_set)

    @staticmethod
    def forward(a, theta):
        sum_i = []
        for i in range(len(theta)):
            sum_i_2 = 0
            for j in range(len(a)):
                sum_i_2 += a[j] * theta[i][j]
            sum_i.append(sum_i_2)
        return sum_i

    @staticmethod
    def backward(delta, theta, a):
        res = []
        for i in range(len(theta[0])):
            sum_i = 0.0
            for j in range(len(theta)):
                sum_i += theta[j][i] * delta[j] * a[i] * (1 - a[i])
            res.append(sum_i)
        return res

    @staticmethod
    def sigmoid(a):
        return 1.0 / (1 + math.exp(-1 * a))

    @staticmethod
    def kian(theta, case):
        z = [[]] * 3
        a = [[]] * 3
        a[0] = [1] + case
        z[1] = Kian.forward(a[0], theta[0])
        a[1] = [1] + [Kian.sigmoid(i) for i in z[1]][1:]
        z[2] = Kian.forward(a[1], theta[1])
        a[2] = [Kian.sigmoid(i) for i in z[2]]
        return a[2]

    @staticmethod
    def cost_function(theta, training_set, reg=True, lambda_para=1):
        sum_cos = 0
        m = len(training_set)
        for case in training_set:
            y = Kian.kian(theta, case[:-1])
            if isinstance(case[-1], int):
                case[-1] = [case[-1]]
            for i in range(len(y)):
                sum_cos -= case[-1][i] * math.log(y[i]) + \
                    (1 - case[-1][i]) * math.log(1 - y[i])
        sum_cos = sum_cos / m
        if reg:
            for i in range(2):
                for j in range(len(theta[i])):
                    for k in range(len(theta[i][j])):
                        if not k or not j:
                            sum_cos += (lambda_para * theta[i][j][k] *
                                        theta[i][j][k]) / (2 * m)
        return sum_cos

    def train(self):
        print "Working on a training set size of %d" % self.size

        while True:
            if len(self.J_cv_history) > 1 and self.J_cv_history[-1] > \
                    self.J_cv_history[-2]:
                break
            self.lambda_para *= 1.62
            print self.lambda_para
            theta = [[]] * 2
            self.J_history = []
            for i in range(2):
                theta[i] = [[]] * self.arch[i]
                for j in range(len(theta[i])):
                    theta[i][j] = [[]] * self.arch2[i]
                    for k in range(len(theta[i][j])):
                        theta[i][j][k] = (random.random() * self.epi * 2) \
                            - self.epi
            for i in range(self.no_iter):
                J = self.cost_function(theta, self.training_set,
                                       lambda_para=self.lambda_para)
                self.J_history.append(J)
                Delta = [[]] * 2
                for ii in range(2):
                    Delta[ii] = [[]] * self.arch[ii]
                    for j in range(len(Delta[ii])):
                        Delta[ii][j] = [[]] * self.arch2[ii]
                        for k in range(len(Delta[ii][j])):
                            Delta[ii][j][k] = 0
                D = Delta[:]
                for case in self.training_set:
                    z = [[]] * 3
                    a = [[]] * 3
                    delta = [[]] * 3
                    a[0] = [1] + case[:-1]
                    z[1] = self.forward(a[0], theta[0])
                    a[1] = [1] + [self.sigmoid(ii) for ii in z[1]][1:]
                    z[2] = self.forward(a[1], theta[1])
                    a[2] = [self.sigmoid(ii) for ii in z[2]]
                    delta[2] = [a[2][ii] - case[-1][ii] for ii
                                in range(len(case[-1]))]
                    delta[1] = self.backward(delta[2], theta[1], a[1])
                    for ii in range(2):
                        for j in range(len(Delta[ii])):
                            for k in range(len(Delta[ii][j])):
                                Delta[ii][j][k] += delta[ii + 1][j] * a[ii][k]
                for ii in range(2):
                    for j in range(len(Delta[ii])):
                        for k in range(len(Delta[ii][j])):
                            D[ii][j][k] = (1.0 / self.size) * Delta[ii][j][k]
                            if not j or not k:
                                D[ii][j][k] += self.lambda_para * \
                                    theta[ii][j][k]
                for ii in range(2):
                    for j in range(len(Delta[ii])):
                        for k in range(len(Delta[ii][j])):
                            theta[ii][j][k] -= self.alpha * D[ii][j][k]
            self.J_cv_history.append(
                self.cost_function(theta, self.cv_set, False))
            self.lambda_history.append(self.lambda_para)
            self.theta_history.append(theta)
        self.theta = theta
        self.D = D

    def finalize(self):
        d_theta = 0.00001
        theta_1 = self.theta[:]
        theta_2 = self.theta[:]
        theta_1[0][1][1] += d_theta
        dl1 = self.cost_function(theta_1, self.training_set)
        theta_2[0][1][1] -= 2 * d_theta
        dl2 = self.cost_function(theta_2, self.training_set)
        print "difference between results..."
        print self.D[0][1][1], (dl1 - dl2) / (2 * d_theta)
        res_the = {0: [], 1: []}
        for case in self.training_set:
            res_the[case[-1][0]].append(self.kian(self.theta, case[:-1])[0])
        res_the2 = {0: [], 1: []}
        for case in self.cv_set:
            res_the2[case[-1][0]].append(self.kian(self.theta, case[:-1])[0])
        print "Cost function convergence"
        print self.J_history[:10], self.J_history[-10:]
        d_path = self.model.data_directory
        with codecs.open(os.path.join(d_path, 'res1.dat'), 'w', 'utf-8') as f:
            f.write(str(res_the))
        with codecs.open(os.path.join(d_path, 'res2.dat'), 'w', 'utf-8') as f:
            f.write(str(res_the2))
        with codecs.open(os.path.join(d_path, 'theta.dat'), 'w', 'utf-8') as f:
            f.write(str(self.theta))

    def run(self):
        self.train()
        self.finalize()
