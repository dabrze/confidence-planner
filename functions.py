import scipy.stats as st
import math
import statsmodels as sm

# Z-Test


def ztest(n, mean, std_dev, conf):
    '''
    This test assumes that data is normally distributed and works well for bigger number of samples (>30).
    Function takes number of samples (n), mean value (mean),
    standard deviation (std_dev) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    z = st.norm.ppf(1 - (1 - conf) / 2)
    upper_bound = mean + z * std_dev / math.sqrt(n)
    lower_bound = mean - z * std_dev / math.sqrt(n)

    return [lower_bound, upper_bound]


print(ztest(100, 50, 5, 0.95))


def reverse_ztest(mean, std_dev, diff, conf):
    '''
    Function takes mean of data (mean), standard deviation of data (std_dev),
    difference from mean to lower/upper bound which is upper_bound-mean or mean-lower_bound (diff)
    and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.
    '''
    z = st.norm.ppf(1 - (1 - conf) / 2)
    n = (z * std_dev / (diff))**2
    return int(round(n))


print(reverse_ztest(50, 5, 1.39, 0.95))


# T-test

def ttest(n, mean, std_dev, conf):
    '''
    This test works for smaller number of samples (<30), uses t-distribution instead the normal one.
    Function takes number of samples (n), mean value (mean), standard deviation and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    t = st.t.ppf(1 - (1 - conf) / 2, n - 1)
    upper_bound = mean + t * std_dev / math.sqrt(n)
    lower_bound = mean - t * std_dev / math.sqrt(n)

    return [lower_bound, upper_bound]


ttest(9, 50, 3, 0.95)


# Langford tests

def loose_langford(n, mean, conf):
    '''
    Function takes number of samples (n), mean value (mean) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    pr = math.sqrt(math.log(2 / (1 - conf)) / (n * 2))
    upper_bound = mean + pr * 10
    lower_bound = mean - pr * 10
    return [lower_bound, upper_bound]


print(loose_langford(50, 50, 0.95))


def loose_langford_reverse(mean, diff, conf):
    '''
    Function takes mean of data (mean), difference from mean to lower/upper bound which is upper_bound-mean
    or mean-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.
    '''
    n = math.log(2 / (1 - conf)) / (2 * (diff / 10)**2)
    return int(round(n))


print(loose_langford_reverse(50, 1.92, 0.95))


def clopper_pearson(n, mean, conf):
    '''
    Function takes number of samples (n), mean value (mean) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    low, high = sm.stats.proportion.proportion_confint(
        n / 2, n, alpha=1 - conf, method="beta")
    return [mean - (0.5 - low) * 10, mean + (high - 0.5) * 10]


print(clopper_pearson(50, 50, 0.95))


# Wilson score interval

def wilson(n, mean, conf):
    '''
    Function takes number of samples (n), mean value (mean) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    low, high = sm.stats.proportion.proportion_confint(
        n / 2, n, alpha=1 - conf, method="wilson")
    return [mean - (0.5 - low) * 10, mean + (high - 0.5) * 10]


print(wilson(50, 50, 0.95))


# dcc.Slider(
#         id='my-slider',
#         min=0,
#         max=20,
#         step=0.5,
#         value=10,
#     ),
#     html.Div(id='slider-output-container')
# ])
#
# @app.callback(
#     dash.dependencies.Output('slider-output-container', 'children'),
#     [dash.dependencies.Input('my-slider', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)
