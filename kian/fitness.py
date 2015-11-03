

def _ratio(test_set, thrashhold):
    false_positives = 0
    for case in test_set[0]:
        if case > thrashhold:
            false_positives += 1
    true_positives = 0
    for case in test_set[1]:
        if case > thrashhold:
            true_positives += 1
    return (false_positives / float(len(test_set[0])),
            true_positives / float(len(test_set[1])))


def AUC(test_set, step=0.01):
    thrashhold = 0
    auc = 0
    x_before = 1
    while thrashhold < 1:
        x, y = _ratio(test_set, thrashhold)
        auc += (x_before - x) * y
        x_before = x
        thrashhold += step
    return auc


def precision(a, b):
    true_positives = 0
    positives = 0
    for case in a[0]:
        if case > b:
            positives += 1
    for case in a[1]:
        if case > b:
            positives += 1
            true_positives += 1
    if positives == 0:
        return
    return float(true_positives) / float(positives)


def recall(a, b):
    true_positives = 0
    positives = 0
    for case in a[1]:
        if case > b:
            true_positives += 1
        positives += 1
    if positives == 0:
        return
    return float(true_positives) / float(positives)


def optimum_thrashhold(test_set, beta=0.5):
    thrashhold = 0
    res = {}
    x = []
    y = []
    while thrashhold < 1:
        pre = precision(test_set, thrashhold)
        rec = recall(test_set, thrashhold)
        if pre is None or rec is None:
            thrashhold += 0.001
            continue
        res[thrashhold] = (pre, rec)
        x.append(thrashhold)
        y.append((2 + (beta**2)) * (pre * rec) / ((pre * beta * beta) + rec))
        thrashhold += 0.001
    the_thrashhold = max(y)
    index = y.index(the_thrashhold)
    return x[index], res[x[index]]
