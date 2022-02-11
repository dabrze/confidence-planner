import scipy.stats as st
import math
import statsmodels.api
import statsmodels as sm
import numpy as np

from components.tests_addons import min_max, min_max_conf

# T-test


def ttest_pr(n, acc, conf):
    '''
    This test works for smaller number of samples (<30), uses t-distribution.
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.
    '''
    
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


def reverse_ttest_pr(diff, conf):
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.
    '''
    pass
    
def reverse_ttest_pr_conf(diff, n):
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and number of samples (n).
    Returns confidence rounded to two decimal places.
    '''
    pr = diff/100
    t = pr/math.sqrt(0.25/n)
    return min_max_conf(round(2*st.t.cdf(t, n-1)-1, 2))
