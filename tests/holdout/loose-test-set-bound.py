import scipy.stats as st
import math
import statsmodels.api
import statsmodels as sm
import numpy as np

from components.tests_addons import min_max, min_max_conf

# Loose test set bound (Langford)


def loose_langford(n, acc, conf):
    '''
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.
    '''
    
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


def loose_langford_reverse(diff, conf):
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.
    '''
    n = math.log(2/(1-conf))/(2*(diff/100)**2)
    return int(round(n))


def loose_langford_conf(diff, n):
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and number of samples (n).
    Returns confidence rounded to two decimal places.
    '''
    pr = diff/100
    pr2 = (diff/100)**2
    expnt = math.exp(2*n*pr2)
    conf = 1 - 2/expnt
    return min_max_conf(round(conf, 2))