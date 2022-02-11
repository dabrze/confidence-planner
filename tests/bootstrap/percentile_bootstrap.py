import scipy.stats as st
import math
import statsmodels.api
import statsmodels as sm
import numpy as np

from components.tests_addons import min_max, min_max_conf

# Percentile bootstrap method


def percentile_BM(accs, conf):
    '''
    Function takes list of resamples accuracies obtained from bootstrap method(accs) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.
    '''
    accs.sort()
    accs = np.array(accs)
    
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