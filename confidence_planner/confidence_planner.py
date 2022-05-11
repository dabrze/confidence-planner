import math
import numpy as np
import functools
import scipy.stats as st
from statsmodels.stats.proportion import proportion_confint


def _min_max(value, low: float = 0.0, high: float = 1.0) -> list:
    """
    Function takes a pair of values (the accuracy confidence interval) and caps it to makes sure that
    the lower bound is at least 0 and the upper bound is at most 1.
    :param value: pair of values
    :param low: min cap
    :param high: max cap
    :return: capped inteval
    """
    if isinstance(value, list):
        assert value[0] <= value[1]
        value[0] = min(max(low, value[0]), high)
        value[1] = min(max(low, value[1]), high)
    else:
        value = max(low, value)
        value = min(value, high)

    return value


def _check_n_acc_conf(n: int, acc: float, conf: float, n_splits: int = 1):
    if n <= 0:
        raise Exception(
            f'Number of samples must be an integer greater than 0, not "{n}"'
        )

    if acc < 0.0 or acc > 1.0:
        raise Exception(f"Accuracy should by between <0, 1>, not {acc}")

    if conf <= 0.0 or conf >= 1.0:
        raise Exception(f"Confidence level should be between (0, 1), not {conf}")

    if n_splits <= 0:
        raise Exception(
            f'Number of folds must be an integer greater tha 0, not "{n_splits}"'
        )


def _check_radius_conf(
    confidence_level: float, interval_radius: float, n_splits: int = 1
):
    if interval_radius < 0 or interval_radius > 0.5:
        raise Exception(
            f'Difference should by between <0, 0.5>, not "{interval_radius}"'
        )
    if confidence_level <= 0 or confidence_level >= 1:
        raise Exception(
            f'Confidence level should be between (0, 1), not "{confidence_level}"'
        )
    if n_splits <= 0:
        raise Exception(
            f'Number of folds must be an integer greater tha 0, not "{n_splits}"'
        )


def cap(low, high):
    def wrapper(f):
        @functools.wraps(f)
        def cap_result(*args, **kwargs):
            value = f(*args, **kwargs)
            return _min_max(value, low, high)

        return cap_result

    return wrapper


@cap(low=0.0, high=1.0)
def wilson_ci(sample_size: int, accuracy: float, confidence_level: float) -> list:
    """
    Returns a confidence interval according to the Wilson approximation, based on the number of holdout
    test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set.
    accuracy : float
        Accuracy obtained on the test set. Should be between 0 and 1.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    """
    _check_n_acc_conf(sample_size, accuracy, confidence_level)

    low, high = proportion_confint(
        accuracy * sample_size, sample_size, alpha=1 - confidence_level, method="wilson"
    )
    int_conf = [low, high]
    return int_conf


@cap(low=0.0, high=1.0)
def clopper_pearson_ci(
    sample_size: int, accuracy: float, confidence_level: float
) -> list:
    """
    Returns a confidence interval according to the Clopper-Pearson approximation, based on the number of holdout
    test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set.
    accuracy : float
        Accuracy obtained on the test set. Should be between 0 and 1.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    """
    _check_n_acc_conf(sample_size, accuracy, confidence_level)

    low, high = proportion_confint(
        accuracy * sample_size, sample_size, alpha=1 - confidence_level, method="beta"
    )
    int_conf = [low, high]
    return int_conf


@cap(low=0.0, high=1.0)
def langford_ci(sample_size: int, accuracy: float, confidence_level: float) -> list:
    """
    Returns a confidence interval according to Langford's approximation, based on the number of holdout
    test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set.
    accuracy : float
        Accuracy obtained on the test set. Should be between 0 and 1.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    """
    _check_n_acc_conf(sample_size, accuracy, confidence_level)

    pr = math.sqrt(math.log(2 / (1 - confidence_level)) / (sample_size * 2))
    upper_bound = accuracy + pr
    lower_bound = accuracy - pr
    int_conf = [lower_bound, upper_bound]

    return int_conf


@cap(low=0.0, high=1.0)
def z_test_ci(sample_size: int, accuracy: float, confidence_level: float) -> list:
    """
    Returns a confidence interval the Z-test (normal distribution) approximation, based on the number of holdout
    test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set.
    accuracy : float
        Accuracy obtained on the test set. Should be between 0 and 1.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    """
    _check_n_acc_conf(sample_size, accuracy, confidence_level)

    z = st.norm.ppf(1 - (1 - confidence_level) / 2)
    pr = z * math.sqrt(0.25 / sample_size)
    upper_bound = accuracy + pr
    lower_bound = accuracy - pr
    int_conf = [lower_bound, upper_bound]

    return int_conf


@cap(low=0.0, high=1.0)
def t_test_ci(sample_size: int, accuracy: float, confidence_level: float) -> list:
    """
    Returns a confidence interval the t-test approximation, based on the number of holdout
    test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set.
    accuracy : float
        Accuracy obtained on the test set. Should be between 0 and 1.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    """
    _check_n_acc_conf(sample_size, accuracy, confidence_level)

    t = st.t.ppf(1 - (1 - confidence_level) / 2, sample_size - 1)
    pr = t * math.sqrt(0.25 / sample_size)
    upper_bound = accuracy + pr
    lower_bound = accuracy - pr
    int_conf = [lower_bound, upper_bound]

    return int_conf


@cap(low=0.0, high=1.0)
def cross_validation_ci(
    sample_size: int, n_splits: int, accuracy: float, confidence_level: float
) -> list:
    """
    Returns confidence interval for the given confidence level for mean CV results, based on
    the number of samples in the CV, number of splits, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of all samples used from the dataset, greater than 0.
    n_splits : int
        Number of folds used in cross validation, greater than 0.
    accuracy : float
        Obtained accuracy - mean of all accuracies from each fold.
        Should be between 0 and 1.
    confidence_level : float
        Desire confidence level. Should be between 0 and 1.
    """
    _check_n_acc_conf(sample_size, accuracy, confidence_level, n_splits=n_splits)

    x = math.log((1 - confidence_level) / 2) * n_splits / 2 / sample_size
    t = math.sqrt(-x)
    lower_bound = accuracy - t
    upper_bound = accuracy + t
    int_conf = [lower_bound, upper_bound]

    return int_conf


@cap(low=0.0, high=1.0)
def percentiles_ci(accuracies: list, confidence_level: float) -> list:
    """
    Returns confidence interval for the given confidence level for a set of bootstrap results, according to percentile
    measurement.

    Parameters
    ----------
    accuracies : list
        List of resamples accuracies from each bootstrapping.
        Accuracies should be between 0 and 1 -> <0, 1>.
    confidence_level : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    """
    accuracies = np.array(sorted(list(accuracies)))

    # Checking correctness of user input
    if np.any(accuracies < 0) or np.any(accuracies > 1):
        raise Exception(
            f"Each accuracy should by between <0, 1>, some is outside these boundaries"
        )

    if confidence_level <= 0 or confidence_level >= 1:
        raise Exception(
            f'Confidence level should be between (0, 1), not "{confidence_level}"'
        )

    lower_bound = np.percentile(accuracies, 100 * ((1 - confidence_level) / 2))
    upper_bound = np.percentile(
        accuracies, 100 * (confidence_level + (1 - confidence_level) / 2)
    )
    int_conf = [lower_bound, upper_bound]
    return int_conf


@cap(low=0.0, high=1.0)
def progressive_validation_ci(
    sample_size: int, accuracy: float, confidence_level: float
) -> list:
    """
    Returns a confidence interval for progressive validation, based on the number of holdout
    test samples, obtained accuracy, and desired confidence level.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set.
    accuracy : float
        Accuracy obtained on the test set. Should be between 0 and 1.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    """
    _check_n_acc_conf(sample_size, accuracy, confidence_level)

    x = math.log((1 - confidence_level) / 2) / 2 / sample_size
    t = math.sqrt(-x)
    lower_bound = accuracy - t
    upper_bound = accuracy + t
    int_conf = [lower_bound, upper_bound]

    return int_conf


def langford_sample_size(interval_radius: float, confidence_level: float) -> int:
    """
    Estimates the number of examples that should be used as holdout to obtain a given confidence interval radius at a
    given confidence level, according to Langford's approximation.

    Parameters
    ----------
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    confidence_level : float
        Confidence level. Should be between 0 and 1.
    """
    _check_radius_conf(confidence_level, interval_radius)

    n = math.log(2 / (1 - confidence_level)) / (2 * interval_radius**2)
    return math.ceil(n)


def z_test_sample_size(interval_radius: float, confidence_level: float) -> int:
    """
    Estimates the number of examples that should be used as holdout to obtain a given confidence interval radius at a
    given confidence level, according to Langford's approximation.

    Parameters
    ----------
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    confidence_level : float
        Confidence level. Should be between 0 and 1.
    """
    _check_radius_conf(confidence_level, interval_radius)

    z = st.norm.ppf(1 - (1 - confidence_level) / 2)
    n = (z * math.sqrt(0.25) / interval_radius) ** 2
    return math.ceil(n)


def cross_validation_sample_size(
    interval_radius: float, confidence_level: float, n_splits: int
) -> int:
    """
    Estimates the number of examples in a dataset taht are needed to obtain a given confidence interval radius at a
    given confidence level, when performing corss-validation with a given number of splits.

    Parameters
    ----------
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    confidence_level : float
        Confidence level. Should be between 0 and 1.
    n_splits: int
        Number of cross-validation splits. Must be greater than 0.
    """
    _check_radius_conf(confidence_level, interval_radius)

    n = -math.log((1 - confidence_level) / 2) * n_splits / 2 / (interval_radius**2)

    return math.ceil(n)


@cap(low=0.0, high=1.0)
def langford_confidence_level(diff: float, n: int) -> float:
    """
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
    """

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(
            f'Number of samples must be a natural number -> whole, positive and greater than 0, not "{n}"'
        )

    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not "{diff / 100}"')

    pr2 = (diff / 100) ** 2
    expnt = math.exp(2 * n * pr2)
    conf = 1 - 2 / expnt

    return conf


@cap(low=0.0, high=1.0)
def t_test_confidence_level(diff: float, n: int) -> float:
    """
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
    """

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(
            f'Number of samples must be a natural number -> whole, positive and greater than 0, not "{n}"'
        )

    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not "{diff / 100}"')

    pr = diff / 100
    t = pr / math.sqrt(0.25 / n)
    conf = 2 * st.t.cdf(t, n - 1) - 1
    return conf


@cap(low=0.0, high=1.0)
def z_test_confidence_level(diff: float, n: int) -> float:
    """
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
    """

    # Scalling difference by *100 as functions were prepared for percentage scale (0-100)
    diff = diff * 100

    # Checking correctness of user input
    if n <= 0:
        raise Exception(
            f'Number of samples must be a natural number -> whole, positive and greater than 0, not "{n}"'
        )

    if diff < 0 or diff > 100:
        raise Exception(f'Difference should by between <0, 1>, not "{diff / 100}"')

    z = (math.sqrt(n) * diff) / 50
    conf = 2 * st.norm.cdf(z) - 1
    return conf


def estimate_confidence_interval(
    sample_size, accuracy, confidence_level, n_splits=None, method="holdout_wilson"
):
    if method == "holdout_wilson":
        return wilson_ci(sample_size, accuracy, confidence_level)
    elif method == "holdout_langford":
        return langford_ci(sample_size, accuracy, confidence_level)
    elif method == "holdout_clopper_pearson":
        return clopper_pearson_ci(sample_size, accuracy, confidence_level)
    elif method == "holdout_z_test":
        return z_test_ci(sample_size, accuracy, confidence_level)
    elif method == "holdout_t_test":
        return t_test_ci(sample_size, accuracy, confidence_level)
    elif method == "bootstrap":
        return percentiles_ci(accuracy, confidence_level)
    elif method == "cv":
        return cross_validation_ci(sample_size, n_splits, accuracy, confidence_level)
    elif method == "progressive":
        return progressive_validation_ci(sample_size, accuracy, confidence_level)
    else:
        raise Exception(
            "Unknown CI estimation method. Should be one of: 'holdout_wilson', 'holdout_langford', "
            "'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test', 'bootstrap', "
            "'cv', 'progressive'"
        )


def estimate_sample_size(accuracy_radius, confidence_level, method="z_test"):
    if method == "holdout_z_test" or method == "bootstrap":
        return z_test_sample_size(accuracy_radius, confidence_level)
    elif method == "holdout_langford":
        return langford_sample_size(accuracy_radius, confidence_level)
    elif method == "cv":
        return cross_validation_sample_size(accuracy_radius, confidence_level)
    else:
        raise Exception(
            "Unknown sample size estimation method. Should be one of: 'holdout_z_test', 'holdout_langford', 'cv',"
            "bootstrap"
        )


def estimate_confidence_level(accuracy_radius, sample_size, method="z_test"):
    if method == "holdout_z_test":
        return z_test_confidence_level(accuracy_radius, sample_size)
    if method == "holdout_t_test":
        return t_test_confidence_level(accuracy_radius, sample_size)
    elif method == "holdout_langford":
        return langford_confidence_level(accuracy_radius, sample_size)
    else:
        raise Exception(
            "Unknown sample size estimation method. Should be one of: 'holdout_z_test', 'holdout_t_test', "
            "'holdout_langford'"
        )
