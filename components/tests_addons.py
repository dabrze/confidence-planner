# Functions providing additional functionality to conducted tests

def min_max(tup):
    '''
    Function takes tuple with lists with the accuracy confidence interval
    and guarantees that the lower bound will be at least 0 and the upper bound will be at most 100.
    '''
    for i in range(len(tup)):
        tup[i][0] = max(0, tup[i][0])
        tup[i][1] = min(tup[i][1], 100)
    return tup

def min_max_conf(conf):
    '''
    Function takes confidence and guarantees that it will be in the range 0-1
    '''
    if conf < 0:
        conf = 0
    if conf > 1:
        conf = 1
    return conf