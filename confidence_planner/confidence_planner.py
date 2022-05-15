import math
import numpy as np
import functools
import scipy.stats as st
from statsmodels.stats.proportion import proportion_confint
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def _min_max(value, low: float = 0.0, high: float = 1.0) -> list:
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


def _check_accuracies_conf_radius(accuracies, confidence_level, interval_radius=0.5):
    if np.any(accuracies < 0) or np.any(accuracies > 1):
        raise Exception(
            f"Each accuracy should by between <0, 1>. Some were found outside of this range."
        )
    if confidence_level <= 0 or confidence_level >= 1:
        raise Exception(
            f'Confidence level should be between 0 and 1, not "{confidence_level}".'
        )
    if interval_radius < 0 or interval_radius > 0.5:
        raise Exception(
            f'Interval radius should be between 0 and 0.5, not "{interval_radius}"'
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


def _check_n_radius(sample_size: float, interval_radius: float, n_splits: int = 1):
    if interval_radius < 0 or interval_radius > 0.5:
        raise Exception(
            f'Interval radius should be between 0 and 0.5, not "{interval_radius}"'
        )
    if sample_size <= 0:
        raise Exception(
            f'Sample size must be an integer greater tha 0, not "{n_splits}"'
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
        Accuracies should be between 0 and 1.
    confidence_level : float
        Desire confidence level. Should be between 0 and 1 -> (0, 1).
    """
    accuracies = np.array(sorted(list(accuracies)))
    _check_accuracies_conf_radius(accuracies, confidence_level)

    lower_bound = np.percentile(accuracies, 100 * ((1 - confidence_level) / 2))
    upper_bound = np.percentile(
        accuracies, 100 * (confidence_level + (1 - confidence_level) / 2)
    )
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
    Estimates the number of examples in a dataset that are needed to obtain a given confidence interval radius at a
    given confidence level, when performing cross-validation with a given number of splits.

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
def langford_confidence_level(sample_size: int, interval_radius: float) -> float:
    """
    Estimates the confidence level of an interval based on the sample size, according to Langford's approximation.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set. Must be greater than 0.
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.

    """
    _check_n_radius(sample_size, interval_radius)

    pr2 = interval_radius**2
    exponent = math.exp(2 * sample_size * pr2)
    conf = 1 - 2 / exponent

    return conf


@cap(low=0.0, high=1.0)
def t_test_confidence_level(sample_size: int, interval_radius: float) -> float:
    """
    Estimates the confidence level of an interval based on the sample size, according to the t-test approximation

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set. Must be greater than 0.
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    """
    _check_n_radius(sample_size, interval_radius)

    t = interval_radius / math.sqrt(0.25 / sample_size)
    conf = 2 * st.t.cdf(t, sample_size - 1) - 1
    return conf


@cap(low=0.0, high=1.0)
def z_test_confidence_level(sample_size: int, interval_radius: float) -> float:
    """
    Estimates the confidence level of an interval based on the sample size, according to the Z-test
    (normal distribution) approximation.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set. Must be greater than 0.
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    """
    _check_n_radius(sample_size, interval_radius)

    z = (math.sqrt(sample_size) * interval_radius) / 0.5
    conf = 2 * st.norm.cdf(z) - 1
    return conf


@cap(low=0.0, high=1.0)
def cross_validation_confidence_level(
    sample_size: int, interval_radius: float, n_splits: int
) -> float:
    """
    Estimates the confidence level of an interval based on the sample size for cross-validation experiments.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set. Must be greater than 0.
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    n_splits : int
        Number of cross-validation splits. Must be greater than 1.
    """
    conf = -2 * math.exp(-sample_size * 2 * (interval_radius**2) / n_splits) + 1
    return conf


@cap(low=0.0, high=1.0)
def percentiles_confidence_level(
    accuracies: list, interval_radius: float, method="rank"
):
    """
    Estimates the confidence level of an interval based on the bootstrap results.

    Parameters
    ----------
    accuracies : list
        List of resamples accuracies from each bootstrapping.
        Accuracies should be between 0 and 1.
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    method : str
        Percentile calculation method. One of 'rank', 'weak', 'strict', 'mean'. Default: 'rank'. See
        scipy.stats.percentileofscore for more details.
    """
    accuracies = np.array(sorted(list(accuracies)))
    _check_accuracies_conf_radius(accuracies, 0.5, interval_radius)

    accuracies_median = np.median(accuracies)
    conf_lower = st.percentileofscore(
        accuracies, accuracies_median - interval_radius, method
    )
    conf_upper = st.percentileofscore(
        accuracies, accuracies_median + interval_radius, method
    )

    confidence_level = (conf_upper - conf_lower) / 100

    return confidence_level


def estimate_confidence_interval(
    sample_size: int,
    accuracy: float or list,
    confidence_level: float,
    n_splits: int = None,
    method: str = "holdout",
):
    """
    Wrapper function for estimating accuracy confidence intervals, according to different approximation functions for
    different classifier evaluation procedures.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set. For the holdout procedure this will be the size of the holdout test set.
        For cross-validation this should be the total number of examples in all the folds (typically the size of
        the dataset). For progressive validation this is the size of the entire dataset. For bootstrapping this
        parameter will be ignored.
    accuracy : float or list
        Estimated accuracy. For the holdout procedure this is the accuracy obtained on the holdout test set, for
         cross-validation and progressive validation it is the mean accuracy from all folds/progressive test sets, for
          bootstrapping this should be a list of accuracies obtained for each bootstrap sample.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    n_splits : int
        Optional. Number of folds used in cross validation. Ignored when method is different than 'cv'.
    method : str
        Evaluation method. Parameter used to determine the confidence interval approximation method. Should be one of:
        'holdout', 'holdout_wilson', 'holdout_langford', 'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test',
        'bootstrap', 'cv', 'progressive'. When 'holdout' uses the 'holdout_wilson' approximation.  Default: 'holdout'.
    """
    if method == "holdout_wilson" or method == "holdout":
        return wilson_ci(sample_size, accuracy, confidence_level)
    elif method == "holdout_langford" or method == "progressive":
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
        if n_splits <= 1:
            raise Exception("Provide the n_splits parameter with a value > 1.")
        return cross_validation_ci(sample_size, n_splits, accuracy, confidence_level)
    else:
        raise Exception(
            "Unknown CI estimation method. Should be one of: 'holdout', 'holdout_wilson', 'holdout_langford', "
            "'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test', 'bootstrap', "
            "'cv', 'progressive'"
        )


def estimate_sample_size(
    interval_radius: float,
    confidence_level: float,
    n_splits: int = None,
    method: str = "holdout",
):
    """
    Wrapper function for estimating the sample size needed to obtain a specified confidence interval, for different
    classifier evaluation procedures.

    Parameters
    ----------
    interval_radius : float
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    confidence_level : float
        Desired confidence level. Should be between 0 and 1.
    n_splits : int
        Optional. Number of folds used in cross validation. Ignored when method is different than 'cv'.
    method : str
        Evaluation method. Parameter used to determine the confidence interval approximation method. Should be one of:
        'holdout', 'holdout_z_test', 'holdout_langford', 'cv', 'bootstrap', 'progressive'. When 'holdout' uses the
        'holdout_z_test' approximation. Default: 'holdout'.
    """
    if method == "holdout_z_test" or method == "holdout" or method == "bootstrap":
        return z_test_sample_size(interval_radius, confidence_level)
    elif method == "holdout_langford" or method == "progressive":
        return langford_sample_size(interval_radius, confidence_level)
    elif method == "cv":
        if n_splits <= 1:
            raise Exception("Provide the n_splits parameter with a value > 1.")
        return cross_validation_sample_size(interval_radius, confidence_level, n_splits)
    else:
        raise Exception(
            "Unknown sample size estimation method. Should be one of: 'holdout', 'holdout_z_test', 'holdout_langford', "
            "'cv', 'bootstrap', 'progressive'."
        )


def estimate_confidence_level(
    sample_size: int,
    interval_radius: float,
    n_splits: int = None,
    method: str = "holdout",
    accuracies: list = None,
):
    """
    Wrapper function for estimating the confidence level of interval radius for a given sample size and a given
    evaluation procedure.

    Parameters
    ----------
    sample_size : int
        Number of samples used in a test set. For the holdout procedure this will be the size of the holdout test set.
        For cross-validation this should be the total number of examples in all the folds (typically the size of
        the dataset). For progressive validation this is the size of the entire dataset. For bootstrapping this
        parameter will be ignored.
    interval_radius : float or list
        Half of the expected confidence interval width. Should be between 0 and 0.5.
    n_splits : int
        Optional. Number of folds used in cross validation. Ignored when method is different than 'cv'.
    method : str
        Evaluation method. Parameter used to determine the confidence interval approximation method. Should be one of:
        'holdout', 'holdout_z_test', 'holdout_t_test', 'holdout_langford', 'cv', 'progressive', 'bootstrap'.
        When 'holdout' uses the 'holdout_z_test' approximation. Default: 'holdout'.
    accuracies: list
        Used only when method='bootstrap'. This should be a list of accuracies obtained for each bootstrap sample.
    """
    if method == "holdout_z_test" or method == "holdout":
        return z_test_confidence_level(sample_size, interval_radius)
    if method == "holdout_t_test":
        return t_test_confidence_level(sample_size, interval_radius)
    elif method == "holdout_langford" or method == "progressive":
        return langford_confidence_level(sample_size, interval_radius)
    elif method == "cv":
        if n_splits <= 1:
            raise Exception("Provide the n_splits parameter with a value > 1.")
        return cross_validation_confidence_level(sample_size, interval_radius, n_splits)
    elif method == "bootstrap":
        if accuracies is None:
            raise Exception(
                "Provide the accuracies parameter with a list of bootstrapping results."
            )
        return percentiles_confidence_level(accuracies, interval_radius)
    else:
        raise Exception(
            "Unknown confidence level estimation method. Should be one of: 'holdout', 'holdout_z_test', "
            "'holdout_t_test', 'holdout_langford', 'cv', 'progressive', 'bootstrap'"
        )


def plot_classifier_intervals(
    names,
    sizes,
    accuracies,
    method,
    confidence_levels=[0.9, 0.95, 0.98],
    n_splits=None,
    xlab="Accuracy",
    width=12,
    height=4,
):
    """
    Wrapper function for estimating the confidence level of interval radius for a given sample size and a given
    evaluation procedure.

    Parameters
    ----------
    names : list
        Names of classifiers the error bars will be plotted.
    sizes : list
        Sample sizes for estimating confidence intervals.
    accuracies : list
        Accuracies for each classifier.
    method : str
        Evaluation method. Parameter used to determine the confidence interval approximation method. Should be one of:
        'holdout', 'holdout_wilson', 'holdout_langford', 'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test',
        'bootstrap', 'cv', 'progressive'. When 'holdout' uses the 'holdout_wilson' approximation.
    confidence_levels : list
        Desired confidence levels, for which graded error bars will be plotted.
    n_splits : int
        Optional. Number of folds used in cross validation. Ignored when method is different than 'cv'.
    xlab: str
        X-axis label.
    width: int
        Plot width in inches.
    height: int
        Plot height in inches.
    """
    colors = [
        "#03045E",
        "#023E8A",
        "#0077B6",
        "#0096C7",
        "#00B4D8",
        "#48CAE4",
        "#90E0EF",
        "#ADE8F4",
    ]
    i = 0
    clf_num = len(names)
    f = plt.figure(figsize=(width, height))

    for name_size_acc in zip(names, sizes, accuracies):
        patches = []
        j = len(confidence_levels) - 1
        for conf in sorted(confidence_levels, reverse=True):
            interval = estimate_confidence_interval(
                name_size_acc[1],
                name_size_acc[2],
                conf,
                method=method,
                n_splits=n_splits,
            )

            if method == "bootstrap":
                mean_acc = np.mean(name_size_acc[2])
            else:
                mean_acc = name_size_acc[2]

            plt.errorbar(
                mean_acc,
                i,
                xerr=np.array([[mean_acc - interval[0], interval[1] - mean_acc]]).T,
                fmt="o",
                color="#ee6c4d",
                ecolor=colors[j],
                elinewidth=(1 - conf) * 100,
                capsize=3 * len(confidence_levels) - j,
                mew=4,
                markersize=5,
            )
            patches.append(
                mpatches.Patch(
                    color=colors[j], label=f"{sorted(confidence_levels)[j] * 100:.0f}%"
                )
            )
            j -= 1
        i += 0.5
    plt.xticks(fontsize=14)
    plt.yticks(ticks=np.arange(0, clf_num / 2, 0.5), labels=list(names), fontsize=14)
    plt.xlabel(xlab, fontsize=16, labelpad=10)
    plt.grid()
    plt.legend(
        handles=patches,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=14,
        title_fontsize=14,
        title="Confidence level:",
    )
    plt.grid(b=None)
    return f
