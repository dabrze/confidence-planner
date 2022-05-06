import scipy.stats as st
import math
import statsmodels.api
import statsmodels as sm
import numpy as np


def min_max(interval: tuple) -> tuple:
    '''
    Function takes tuple with lists with the accuracy confidence interval
    and guarantees that the lower bound will be at least 0 and the upper bound will be at most 100.
    '''
    interval[0] = max(0.0, interval[0])
    interval[1] = min(interval[1], 1.0)
    return interval


def min_max_tuple(tup: tuple) -> tuple:
    '''
    Function takes tuple with lists with the accuracy confidence interval
    and guarantees that the lower bound will be at least 0 and the upper bound will be at most 100.
    '''
    for i in range(len(tup)):
        tup[i][0] = max(0, tup[i][0])
        tup[i][1] = min(tup[i][1], 100)
    return tup


def min_max_conf(conf: float) -> float:
    '''
    Function takes confidence and guarantees that it will be in the range 0-1
    '''
    if conf < 0:
        conf = 0
    if conf > 1:
        conf = 1
    return conf


def _check_n_acc_conf(n: int, acc: float, conf: float):
    if n <= 0:
        raise Exception(
            f'Number of samples must be a natural number -> whole, positive and greater than 0, not \"{n}\"')

    if acc < 0.0 or acc > 1.0:
        raise Exception(f'Accuracy should by between <0, 1>, not {acc}')

    if conf <= 0.0 or conf >= 1.0:
        raise Exception(f'Confidence level should be between (0, 1), not {conf}')


def clopper_pearson(sample_size: int, accuracy: float, confidence_level: float) -> tuple:
    """
    Returns confidence interval for the given confidence level according to the Clopper-Pearson method, based on
    the number of holdout test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set, greater than 0.
    accuracy : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1 -> (0, 1).
    """

    # Checking correctness of user input
    _check_n_acc_conf(sample_size, accuracy, confidence_level)
    
    low, high = sm.stats.proportion.proportion_confint(sample_size / 2, sample_size, alpha=1 - confidence_level, method ="beta")
    int_conf = [accuracy - (0.5 - low), accuracy + (high - 0.5)]
    return min_max(int_conf)


def cv_interval(n: int, n_splits:  int, accuracy:float, confidence_level: float) -> tuple:
    '''
    Returns confidence interval for the given confidence level for mean CV results, based on
    the number of samples in the CV, number of splits, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    n : int
        Number of all samples used from the dataset, greater than 0.
    n_splits : int
        Number of folds used in cross validation, greater than 0.
    accuracy : float or int
        Obtained accuracy - final accuracy, e.g. average of all accuracies from each fold.
        Should be between 0 and 1 -> <0, 1>.
    confidence_level : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''

    # Checking correctness of user input
    _check_n_acc_conf(n, accuracy, confidence_level)
    if n_splits <= 0:
        raise Exception(f'Number of folds must be a natural number -> whole, positive and greater than 0, not \"{n}\"')
    
    x = math.log((1 - confidence_level) / 2) * n_splits / 2 / n
    t = math.sqrt(-x)
    lower_bound = accuracy - t
    upper_bound = accuracy + t
    int_conf = [lower_bound, upper_bound]
    
    return min_max(int_conf)


def langford_conf(diff: float, n:int) -> float:
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


def langford_reverse(diff: float, conf: float) -> int:
    '''
    Function takes difference from accuracy to lower/upper bound which is upper_bound-acc 
    or acc-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.

    Parameters
    ----------
    diff : float or int
        Difference from accuracy to lower/upper bound of a confidence interval,
        e.g. if accuracy is 0.9 and interval is [0.85, 0.95], then diff=0.05.
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


def langford(sample_size: int, accuracy: float, confidence_level: float) -> tuple:
    '''
    Returns confidence interval for the given confidence level according to the Clopper-Pearson method, based on
    the number of holdout test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set, greater than 0.
    accuracy : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    confidence_level : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''

    # Checking correctness of user input
    _check_n_acc_conf(sample_size, accuracy, confidence_level)
    
    pr = math.sqrt(math.log(2 / (1 - confidence_level)) / (sample_size * 2))
    upper_bound = accuracy + pr
    lower_bound = accuracy - pr
    int_conf = [lower_bound, upper_bound]
    return min_max(int_conf)


def percentile_BM(accuracies:list, confidence_level:float) -> tuple:
    '''
    Function takes list of resamples accuracies obtained from bootstrap method(accs) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    accuracies : list
        List of resamples accuracies from each bootstrapping.
        Accuracies should be between 0 and 1 -> <0, 1>.
    confidence_level : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''
    accuracies = np.array(sorted(list(accuracies)))

    # Checking correctness of user input
    if np.any(accuracies < 0) or np.any(accuracies > 1):
        raise Exception(f'Each accuracy should by between <0, 1>, some is outside these boundaries')

    if confidence_level <= 0 or confidence_level >= 1:
        raise Exception(f'Confidence level should be between (0, 1), not \"{confidence_level}\"')

    lower_bound = np.percentile(accuracies, ((1 - confidence_level) / 2))
    upper_bound = np.percentile(accuracies, (confidence_level + (1 - confidence_level) / 2))
    int_conf = [lower_bound, upper_bound]
    return min_max(int_conf)


def prog_val(n:int, acc:float, conf:float) -> tuple:
    '''
    Function takes number of samples from a test set (s), obtained accuracy (acc) and confidence (conf).
    Returns confidence interval for the given confidence as well as confidence intervals 
    for 90%, 95%, 98% and 99% confidences.

    Parameters
    ----------
    n : int
        Number of samples from a test set, greater than 0.
    acc : float or int
        Obtained accuracy. Should be between 0 and 1 -> <0, 1>.
    conf : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    '''
    _check_n_acc_conf(n, acc, conf)
    
    x = math.log((1-conf)/2) / 2 / n
    t = math.sqrt(-x)
    lower_bound = acc-t
    upper_bound = acc+t
    int_conf = [lower_bound, upper_bound]
    
    return min_max(int_conf)


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
    _check_n_acc_conf(n, acc, conf)
    
    t = st.t.ppf(1-(1-conf)/2, n-1)
    pr = t*math.sqrt(0.25/n)
    upper_bound = acc + pr
    lower_bound = acc - pr
    int_conf = [lower_bound, upper_bound]
    
    return min_max(int_conf)


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
    _check_n_acc_conf(n, acc, conf)
    
    low, high = sm.stats.proportion.proportion_confint(n/2, n, alpha=1-conf, method = "wilson")
    int_conf = [acc-(0.5-low), acc+(high-0.5)]
    return min_max(int_conf)


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
    _check_n_acc_conf(n, acc, conf)
    
    z = st.norm.ppf(1-(1-conf)/2)
    pr = z*math.sqrt(0.25/n)
    upper_bound = acc + pr
    lower_bound = acc - pr
    int_conf = [lower_bound, upper_bound]
    
    return min_max(int_conf)


def estimate_confidence_interval(sample_size, accuracy, confidence_level, n_splits=None, method="holdout_wilson"):
    if method == "holdout_wilson":
        return wilson(sample_size, accuracy, confidence_level)
    elif method == "holdout_langford":
        return langford(sample_size, accuracy, confidence_level)
    elif method == "holdout_clopper_pearson":
        return clopper_pearson(sample_size, accuracy, confidence_level)
    elif method == "holdout_z_test":
        return ztest_pr(sample_size, accuracy, confidence_level)
    elif method == "holdout_t_test":
        return ttest_pr(sample_size, accuracy, confidence_level)
    elif method == "bootstrap":
        return percentile_BM(accuracy, confidence_level)
    elif method == "cv":
        return cv_interval(sample_size, n_splits, accuracy, confidence_level)
    elif method == "progressive":
        return prog_val(sample_size, accuracy, confidence_level)
    else:
        raise Exception("Unknown CI estimation method. Should be one of: 'holdout_wilson', 'holdout_langford', "
                        "'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test', 'bootstrap', "
                        "'cv', 'progressive'")


def estimate_sample_size(accuracy_radius, confidence_level, method="z_test"):
    if method == "z_test":
        return reverse_ztest_pr(accuracy_radius, confidence_level)
    elif method == "langford":
        return langford_reverse(accuracy_radius, confidence_level)
    else:
        raise Exception("Unknown sample size estimation method. Should be one of: 'z_test', 'langford'")


def estimate_confidence_level(accuracy_radius, sample_size, method="z_test"):
    if method == "z_test":
        return reverse_ztest_pr_conf(accuracy_radius, sample_size)
    if method == "t_test":
        return reverse_ttest_pr_conf(accuracy_radius, sample_size)
    elif method == "langford":
        return langford_conf(accuracy_radius, sample_size)
    else:
        raise Exception("Unknown sample size estimation method. Should be one of: 'z_test', 't_test', 'langford'")
