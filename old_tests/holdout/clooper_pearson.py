import scipy.stats as st
import math
import statsmodels.api
import statsmodels as sm
import numpy as np

from components.tests_addons import min_max, min_max_conf

# Clopper-Pearson


def clopper_pearson(n, acc, conf):
    '''
    Function takes number of samples (n), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.
    '''
    
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