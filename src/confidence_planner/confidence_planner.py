import scipy.stats as st
import math
import statsmodels.api
import statsmodels as sm
import numpy as np


def min_max(tup:tuple) -> tuple:
    '''
    Function takes tuple with lists with the accuracy confidence interval
    and guarantees that the lower bound will be at least 0 and the upper bound will be at most 100.
    '''
    for i in range(len(tup)):
        tup[i][0] = max(0, tup[i][0])
        tup[i][1] = min(tup[i][1], 100)
    print('Confidence intervals around given accuracy for your confidence and 90%, 95%, 98%, 99%.')
    return tup

def min_max_conf(conf:float) -> float:
    '''
    Function takes confidence and guarantees that it will be in the range 0-1
    '''
    if conf < 0:
        conf = 0
    if conf > 1:
        conf = 1
    return conf

def clopper_pearson(n:int, acc:float, conf:float) -> tuple:
    '''
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    n : int
        Number of samples used in a test set, greater than 0.
    acc : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''
    
    # Scalling accuracy by *100 as functions were prepared for percentage scale (0-100)
    acc = acc * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if acc < 0 or acc > 100:
        raise Exception(f'Accuracy should by between <0, 1>, not \"{acc/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')

    low90, high90 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.90, method = "beta")
    int90 = [acc-(0.5-low90)*100, acc+(high90-0.5)*100]
    
    low95, high95 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.95, method = "beta")
    int95 = [acc-(0.5-low95)*100, acc+(high95-0.5)*100]
    
    low98, high98 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.98, method = "beta")
    int98 = [acc-(0.5-low98)*100, acc+(high98-0.5)*100]
    
    low99, high99 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.99, method = "beta")
    int99 = [acc-(0.5-low99)*100, acc+(high99-0.5)*100]
    
    
    low, high = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-conf, method = "beta")
    int_conf = [acc-(0.5-low)*100, acc+(high-0.5)*100]
    return min_max((int_conf, int90, int95, int98, int99))


def cv_interval(n:int, k:int, acc:float, conf:float) -> tuple:
    '''
    Function takes number of samples (n), number of folds(k), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    n : int
        Number of all samples used from the dataset, greater than 0.
    k : int
        Number of folds used in cross validation, greater than 0.
    acc : float or int
        Obtained accuracy - final accuracy, e.g. average of all accuracies from each fold.
        Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''
    
    # Scalling accuracy by *100 as functions were prepared for percentage scale (0-100)
    acc = acc * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if k <= 0:
        raise Exception(f'Number of folds must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 

    if acc < 0 or acc > 100:
        raise Exception(f'Accuracy should by between <0, 1>, not \"{acc/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')
    
    x90 = math.log((1-0.9)/2)*k/2/n
    t90 = math.sqrt(-x90)
    lower_bound90 = acc-t90*100
    upper_bound90 = acc+t90*100
    int90 = [lower_bound90, upper_bound90]
    
    x95 = math.log((1-0.95)/2)*k/2/n
    t95 = math.sqrt(-x95)
    lower_bound95 = acc-t95*100
    upper_bound95 = acc+t95*100
    int95 = [lower_bound95, upper_bound95]
    
    x98 = math.log((1-0.98)/2)*k/2/n
    t98 = math.sqrt(-x98)
    lower_bound98 = acc-t98*100
    upper_bound98 = acc+t98*100
    int98 = [lower_bound98, upper_bound98]
    
    x99 = math.log((1-0.99)/2)*k/2/n
    t99 = math.sqrt(-x99)
    lower_bound99 = acc-t99*100
    upper_bound99 = acc+t99*100
    int99 = [lower_bound99, upper_bound99]
    
    
    x = math.log((1-conf)/2)*k/2/n
    t = math.sqrt(-x)
    lower_bound = acc-t*100
    upper_bound = acc+t*100
    int_conf = [lower_bound, upper_bound]
    
    return min_max((int_conf, int90, int95, int98, int99))


def loose_langford_conf(diff:float, n:int) -> float:
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and number of samples (n).
    Returns confidence rounded to two decimal places.

    Parameters
    ----------
    diff : float or int
        Difference from accuracy to lower/upper bound of a confidence interval,
        e.g. if accuracy is 0.9 and interval is [0.85, 0.95], then diff=0.05.
        Should be between 0 and 1 -> <0, 1>.
    n : int
        Number of samples used in a test set greater than 0.
    '''

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not \"{diff/100}\"')

    pr = diff/100
    pr2 = (diff/100)**2
    expnt = math.exp(2*n*pr2)
    conf = 1 - 2/expnt
    return min_max_conf(round(conf, 2))


def loose_langford_reverse(diff:float, conf:float) -> int:
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.

    Parameters
    ----------
    diff : float or int
        Difference from accuracy to lower/upper bound of a confidence interval,
        e.g. if accuracy is 0.9 and interval is [0.85, 0.95], then diff=0.5.
        Should be between 0 and 1 -> <0, 1>.
    conf : float
        Confidence. Should be between 0 and 1 -> (0, 1).
    '''

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not \"{diff/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')

    n = math.log(2/(1-conf))/(2*(diff/100)**2)
    return int(round(n))


def loose_langford(n:int, acc:float, conf:float) -> tuple:
    '''
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    n : int
        Number of samples used in a test set, greater than 0.
    acc : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''
    
    # Scalling accuracy by *100 as functions were prepared for percentage scale (0-100)
    acc = acc * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if acc < 0 or acc > 100:
        raise Exception(f'Accuracy should by between <0, 1>, not \"{acc/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')

    
    pr90 = math.sqrt(math.log(2/(1-0.90))/(n*2))
    upper_bound90 = acc + pr90*100
    lower_bound90 = acc - pr90*100
    int90 = [lower_bound90, upper_bound90]
    
    pr95 = math.sqrt(math.log(2/(1-0.95))/(n*2))
    upper_bound95 = acc + pr95*100
    lower_bound95 = acc - pr95*100
    int95 = [lower_bound95, upper_bound95]
    
    pr98 = math.sqrt(math.log(2/(1-0.98))/(n*2))
    upper_bound98 = acc + pr98*100
    lower_bound98 = acc - pr98*100
    int98 = [lower_bound98, upper_bound98]
    
    pr99 = math.sqrt(math.log(2/(1-0.99))/(n*2))
    upper_bound99 = acc + pr99*100
    lower_bound99 = acc - pr99*100
    int99 = [lower_bound99, upper_bound99]
    
    
    pr = math.sqrt(math.log(2/(1-conf))/(n*2))
    upper_bound = acc + pr*100
    lower_bound = acc - pr*100
    int_conf = [lower_bound, upper_bound]
    return min_max((int_conf, int90, int95, int98, int99))


def percentile_BM(accs:list, conf:float) -> tuple:
    '''
    Function takes list of resamples accuracies obtained from bootstrap method(accs) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    accs : list
        List of resamples accuracies from each bootstrapping.
        Accuracies should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''

    # Scalling accuracies by *100 as functions were prepared for percentage scale (0-100)
    accs = list(accs).sort()
    accs = np.array(accs) * 100

    # Checking correctness of user input
    if any(accs < 0) or any(accs > 100):
        raise Exception(f'Each accuracy should by between <0, 1>, some is outside these boundaries')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')

    
    lower_bound90 = np.percentile(accs, 100*((1-0.9)/2))
    upper_bound90 = np.percentile(accs, 100*(0.9 + (1-0.9)/2))
    int90 = [lower_bound90, upper_bound90]
    
    lower_bound95 = np.percentile(accs, 100*((1-0.95)/2))
    upper_bound95 = np.percentile(accs, 100*(0.95 + (1-0.95)/2))
    int95 = [lower_bound95, upper_bound95]
    
    lower_bound98 = np.percentile(accs, 100*((1-0.98)/2))
    upper_bound98 = np.percentile(accs, 100*(0.98 + (1-0.98)/2))
    int98 = [lower_bound98, upper_bound98]
    
    lower_bound99 = np.percentile(accs, 100*((1-0.99)/2))
    upper_bound99 = np.percentile(accs, 100*(0.99 + (1-0.99)/2))
    int99 = [lower_bound99, upper_bound99]
    
    
    lower_bound = np.percentile(accs, 100*((1-conf)/2))
    upper_bound = np.percentile(accs, 100*(conf + (1-conf)/2))
    int_conf = [lower_bound, upper_bound]
    return min_max((int_conf, int90, int95, int98, int99))


def prog_val(s:int, acc:float, conf:float) -> tuple:
    '''
    Function takes number of samples from a test set (s), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    s : int
        Number of samples from a test set, greater than 0.
    acc : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''

    # Scalling accuracy by *100 as functions were prepared for percentage scale (0-100)
    acc = acc * 100

    # Checking correctness of user input
    if s <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{s}\"') 
    
    if acc < 0 or acc > 100:
        raise Exception(f'Accuracy should by between <0, 1>, not \"{acc/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')
    
    x90 = math.log((1-0.9)/2)/2/s
    t90 = math.sqrt(-x90)
    lower_bound90 = acc-t90*100
    upper_bound90 = acc+t90*100
    int90 = [lower_bound90, upper_bound90]
    
    x95 = math.log((1-0.95)/2)/2/s
    t95 = math.sqrt(-x95)
    lower_bound95 = acc-t95*100
    upper_bound95 = acc+t95*100
    int95 = [lower_bound95, upper_bound95]
    
    x98 = math.log((1-0.98)/2)/2/s
    t98 = math.sqrt(-x98)
    lower_bound98 = acc-t98*100
    upper_bound98 = acc+t98*100
    int98 = [lower_bound98, upper_bound98]
    
    x99 = math.log((1-0.99)/2)/2/s
    t99 = math.sqrt(-x99)
    lower_bound99 = acc-t99*100
    upper_bound99 = acc+t99*100
    int99 = [lower_bound99, upper_bound99]
    
    
    x = math.log((1-conf)/2)/2/s
    t = math.sqrt(-x)
    lower_bound = acc-t*100
    upper_bound = acc+t*100
    int_conf = [lower_bound, upper_bound]
    
    return min_max((int_conf, int90, int95, int98, int99))


def reverse_ttest_pr_conf(diff:float, n:int) -> float:
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and number of samples (n).
    Returns confidence rounded to two decimal places.

    Parameters
    ----------
    diff : float or int
        Difference from accuracy to lower/upper bound of a confidence interval,
        e.g. if accuracy is 0.9 and interval is [0.85, 0.95], then diff=0.05.
        Should be between 0 and 1 -> <0, 1>.
    n : int
        Number of samples from a test set greater than 0.
    '''

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not \"{diff/100}\"')

    pr = diff/100
    t = pr/math.sqrt(0.25/n)
    return min_max_conf(round(2*st.t.cdf(t, n-1)-1, 2))


def reverse_ztest_pr_conf(diff:float, n:int) -> float:
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and number of samples (n).
    Returns confidence rounded to two decimal places.

    Parameters
    ----------
    diff : float or int
        Difference from accuracy to lower/upper bound of a confidence interval,
        e.g. if accuracy is 0.9 and interval is [0.85, 0.95], then diff=0.05.
        Should be between 0 and 1 -> <0, 1>.
    n : int
        Number of samples from a test set greater than 0.
    '''

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not \"{diff/100}\"')

    z = (math.sqrt(n)*diff)/50
    return min_max_conf(round(2*st.norm.cdf(z)-1, 2))


def reverse_ztest_pr(diff:float, conf:float) -> int:
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.

    Parameters
    ----------
    diff : float
        Difference from accuracy to lower/upper bound of a confidence interval,
        e.g. if accuracy is 0.9 and interval is [0.85, 0.95], then diff=0.05.
        Should be between 0 and 1 -> <0, 1>.
    conf : float
        Confidence level. Should be between 0 and 1 -> (0, 1).
    '''

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not \"{diff/100}\"')
    
    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')


    z = st.norm.ppf(1-(1-conf)/2)
    n = (z*math.sqrt(0.25)/(diff/100))**2
    return int(round(n))


def ttest_pr(n:int, acc:float, conf:float) -> tuple:
    '''
    This test works for smaller number of samples (<30), uses t-distribution.
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    n : int
        Number of samples used in a test set, greater than 0.
    acc : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''
    
    # Scalling accuracy by *100 as functions were prepared for percentage scale (0-100)
    acc = acc * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if acc < 0 or acc > 100:
        raise Exception(f'Accuracy should by between <0, 1>, not \"{acc/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')
    

    t90 = st.t.ppf(1-(1-0.9)/2, n-1)
    pr90 = t90*math.sqrt(0.25/n)
    upper_bound90 = acc + 100*pr90
    lower_bound90 = acc - 100*pr90
    int90 = [lower_bound90, upper_bound90]
    
    t95 = st.t.ppf(1-(1-0.95)/2, n-1)
    pr95 = t95*math.sqrt(0.25/n)
    upper_bound95 = acc + 100*pr95
    lower_bound95 = acc - 100*pr95
    int95 = [lower_bound95, upper_bound95]
    
    t98 = st.t.ppf(1-(1-0.98)/2, n-1)
    pr98 = t98*math.sqrt(0.25/n)
    upper_bound98 = acc + 100*pr98
    lower_bound98 = acc - 100*pr98
    int98 = [lower_bound98, upper_bound98]
    
    t99 = st.t.ppf(1-(1-0.99)/2, n-1)
    pr99 = t99*math.sqrt(0.25/n)
    upper_bound99 = acc + 100*pr99
    lower_bound99 = acc - 100*pr99
    int99 = [lower_bound99, upper_bound99]
    
    
    t = st.t.ppf(1-(1-conf)/2, n-1)
    pr = t*math.sqrt(0.25/n)
    upper_bound = acc + 100*pr
    lower_bound = acc - 100*pr
    int_conf = [lower_bound, upper_bound]
    
    return min_max((int_conf, int90, int95, int98, int99))


def wilson(n:int, acc:float, conf:float) -> tuple:
    '''
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    n : int
        Number of samples used in a test set, greater than 0.
    acc : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''

    # Scalling accuracy by *100 as functions were prepared for percentage scale (0-100)
    acc = acc * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if acc < 0 or acc > 100:
        raise Exception(f'Accuracy should by between <0, 1>, not \"{acc/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')
    
    
    low90, high90 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.90, method = "wilson")
    int90 = [acc-(0.5-low90)*100, acc+(high90-0.5)*100]
    
    low95, high95 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.95, method = "wilson")
    int95 = [acc-(0.5-low95)*100, acc+(high95-0.5)*100]
    
    low98, high98 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.98, method = "wilson")
    int98 = [acc-(0.5-low98)*100, acc+(high98-0.5)*100]
    
    low99, high99 = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-0.99, method = "wilson")
    int99 = [acc-(0.5-low99)*100, acc+(high99-0.5)*100]
    
    
    low, high = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-conf, method = "wilson")
    int_conf = [acc-(0.5-low)*100, acc+(high-0.5)*100]
    return min_max((int_conf, int90, int95, int98, int99))


def ztest_pr(n:int, acc:float, conf:float) -> tuple:
    '''
    This test assumes that data is normally distributed and works well for bigger number of samples (>30).
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    n : int
        Number of samples used in a test set, greater than 0.
    acc : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''

    # Scalling accuracy by *100 as functions were prepared for percentage scale (0-100)
    acc = acc * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"') 
    
    if acc < 0 or acc > 100:
        raise Exception(f'Accuracy should by between <0, 1>, not \"{acc/100}\"')

    if conf <= 0 or conf >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{conf}\"')
    
    
    z90 = st.norm.ppf(1-(1-0.9)/2)
    pr = z90*math.sqrt(0.25/n)
    upper_bound90 = acc + 100*pr
    lower_bound90 = acc - 100*pr
    int90 = [lower_bound90, upper_bound90]
    
    z95 = st.norm.ppf(1-(1-0.95)/2)
    pr = z95*math.sqrt(0.25/n)
    upper_bound95 = acc + 100*pr
    lower_bound95 = acc - 100*pr
    int95 = [lower_bound95, upper_bound95]
    
    z98 = st.norm.ppf(1-(1-0.98)/2)
    pr = z98*math.sqrt(0.25/n)
    upper_bound98 = acc + 100*pr
    lower_bound98 = acc - 100*pr
    int98 = [lower_bound98, upper_bound98]
    
    z99 = st.norm.ppf(1-(1-0.99)/2)
    pr = z99*math.sqrt(0.25/n)
    upper_bound99 = acc + 100*pr
    lower_bound99 = acc - 100*pr
    int99 = [lower_bound99, upper_bound99]    
    
    
    z = st.norm.ppf(1-(1-conf)/2)
    pr = z*math.sqrt(0.25/n)
    upper_bound = acc + 100*pr
    lower_bound = acc - 100*pr
    int_conf = [lower_bound, upper_bound]
    
    return min_max((int_conf, int90, int95, int98, int99))