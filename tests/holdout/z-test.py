import scipy.stats as st
import math

from components.tests_addons import min_max, min_max_conf

# Z-Test


def ztest_pr(n, acc, conf):
    '''
    This test assumes that data is normally distributed and works well for bigger number of samples (>30).
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.
    '''
    
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


def reverse_ztest_pr(diff, conf):
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.
    '''
    z = st.norm.ppf(1-(1-conf)/2)
    n = (z*math.sqrt(0.25)/(diff/100))**2
    return int(round(n))


def reverse_ztest_pr_conf(diff, n):
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and number of samples (n).
    Returns confidence rounded to two decimal places.
    '''
    z = (math.sqrt(n)*diff)/50
    return min_max_conf(round(2*st.norm.cdf(z)-1, 2))