import scipy.stats as st
import math
import statsmodels.api
import statsmodels as sm
import numpy as np

from components.tests_addons import min_max, min_max_conf

# Interval for Cross Validation


def cv_interval(n, k, acc, conf):
    '''
    Function takes number of samples (n), number of folds(k), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.
    '''
    
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