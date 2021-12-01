import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import plotly.express as px

import plotly.io as pio
import numpy as np
import pandas as pd
import time
import datetime

import scipy.stats as st
import math
import statsmodels as sm

import layouts

external_theme = [dbc.themes.COSMO]

app = dash.Dash(external_stylesheets=external_theme,
                suppress_callback_exceptions=True)

# The layout of the home all pages (only the last div changes...)
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='side_click'),  # sidebar -> HIDDEN/SHOW
    layouts.elements['navbar'],
    layouts.elements['sidebar'],
    html.Div(children=layouts.elements['/main'],
             id='page_content', className='page_content'),
]
)

# Callback taking care of changing webpage content with respect given url


@app.callback(Output('page_content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        try:
            page = layouts.elements['/main']
            print('Main webpage already created')
            return page
        except Exception as ex:
            print('No main webpage found' + str(ex))
            return 'No main webpage found' + str(ex)
    else:
        try:
            page = layouts.elements[str(pathname)]
            return page
        except Exception as ex:
            return 'Ups... Something went wrong.\n404 Error, Website not found...' + str(ex)

# Toggling sidebar_button


@app.callback(
    Output('sidebar_button', 'className'),
    [Input('sidebar_button', 'n_clicks')],
    [State('side_click', 'data')]
)
def toggle_sidebar_button(n_clicks, state):
    print('buttan', n_clicks, state)
    if n_clicks:
        if state == 'SHOW':
            styl = 'sidebar_button_off'
            state = 'HIDDEN'
        else:  # state == 'HIDDEN':
            styl = 'sidebar_button_on'
            state = 'SHOW'
    else:
        styl = 'sidebar_button_off'
        state = 'HIDDEN'
    return styl


# Toggling sidebar
@app.callback(
    [
        Output("sidebar", "className"),
        Output("page_content", "className"),
        Output("side_click", "data"),
    ],

    [Input("sidebar_button", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    print('sidebar', n, nclick)
    if n:
        if nclick == "SHOW":
            sidebar_style = 'sidebar_off'
            content_style = 'content_off'
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = 'sidebar_on'
            content_style = 'content_on'
            cur_nclick = "SHOW"
    else:
        sidebar_style = 'sidebar_off'
        content_style = 'content_off'
        cur_nclick = 'HIDDEN'

    return sidebar_style, content_style, cur_nclick


# Z TEST callback:

@app.callback(
    Output('z_test_result', 'children'),
    Input('z_test_button', 'n_clicks'),
    State('z_test_sample', 'value'),
    State('z_test_mean', 'value'),
    State('z_test_std_dev', 'value'),
    State('z_test_confidence', 'value'),
    prevent_initial_call=True

)
def ztest(n_click, n, mean, std_dev, conf):
    '''
    This test assumes that data is normally distributed and works well for bigger number of samples (>30).
    Function takes number of samples (n), mean value (mean),
    standard deviation (std_dev) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    z = st.norm.ppf(1 - (1 - conf) / 2)
    upper_bound = mean + z * std_dev / math.sqrt(n)
    lower_bound = mean - z * std_dev / math.sqrt(n)

    # return [lower_bound, upper_bound]
    return html.Div('Lower bound: ' + str(lower_bound) + ' Upper bound: ' + str(upper_bound))


# reverse Z TEST
@app.callback(
    Output('z_test_reverse_result', 'children'),
    Input('t_test_reverse_button', 'n_clicks'),
    State('z_test_reverse_mean', 'value'),
    State('z_test_reverse_std_dev', 'value'),
    State('z_test_reverse_diff', 'value'),
    State('z_test_reverse_confidence', 'value'),
    prevent_initial_call=True
)
def reverse_ztest(n_clicks, mean, std_dev, diff, conf):
    '''
    Function takes mean of data (mean), standard deviation of data (std_dev),
    difference from mean to lower/upper bound which is upper_bound-mean or mean-lower_bound (diff)
    and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.
    '''
    print('z_reverse works')
    z = st.norm.ppf(1 - (1 - conf) / 2)
    n = (z * std_dev / (diff))**2
    return int(round(n))

# T TEST callback


@app.callback(
    Output('t_test_result', 'children'),
    Input('t_test_button', 'n_clicks'),
    State('t_test_sample', 'value'),
    State('t_test_mean', 'value'),
    State('t_test_std_dev', 'value'),
    State('t_test_confidence', 'value'),
    prevent_initial_call=True
)
def ttest(n_clicks, n, mean, std_dev, conf):
    '''
    This test works for smaller number of samples (<30), uses t-distribution instead the normal one.
    Function takes number of samples (n), mean value (mean), standard deviation and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    t = st.t.ppf(1 - (1 - conf) / 2, n - 1)
    upper_bound = mean + t * std_dev / math.sqrt(n)
    lower_bound = mean - t * std_dev / math.sqrt(n)

    return [lower_bound, upper_bound]


# LOOSE LANGFORD callback


@app.callback(
    Output('loose_test_result', 'children'),
    Input('loose_test_button', 'n_clicks'),
    State('loose_test_sample', 'value'),
    State('loose_test_mean', 'value'),
    State('loose_test_confidence', 'value'),
    prevent_initial_call=True
)
def loose_langford(n_clicks, n, mean, conf):
    '''
    Function takes number of samples (n), mean value (mean) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    pr = math.sqrt(math.log(2 / (1 - conf)) / (n * 2))
    upper_bound = mean + pr * 10
    lower_bound = mean - pr * 10
    return [lower_bound, upper_bound]


# LOOSE LANGFORD REVERSE callback

@app.callback(
    Output('loose_test_reverse_result', 'children'),
    Input('loose_test_reverse_button', 'n_clicks'),
    State('loose_test_reverse_mean', 'value'),
    State('loose_test_reverse_diff', 'value'),
    State('loose_test_reverse_confidence', 'value'),
    prevent_initial_call=True
)
def loose_langford_reverse(n_clicks, mean, diff, conf):
    '''
    Function takes mean of data (mean), difference from mean to lower/upper bound which is upper_bound-mean
    or mean-lower_bound (diff) and confidence (conf).
    Returns rounded number of samples which should be taken to obtain a given confidence interval.
    '''
    n = math.log(2 / (1 - conf)) / (2 * (diff / 10)**2)
    return int(round(n))


# CLOPPER PEARSOON callback

@app.callback(
    Output('clopper_test_result', 'children'),
    Input('clopper_test_button', 'n_clicks'),
    State('clopper_test_sample', 'value'),
    State('clopper_test_mean', 'value'),
    State('clopper_test_confidence', 'value'),

    prevent_initial_call=True
)
def clopper_pearson(n_clicks, n, mean, conf):
    '''
    Function takes number of samples (n), mean value (mean) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    low, high = sm.stats.proportion.proportion_confint(
        n / 2, n, alpha=1 - conf, method="beta")
    return [mean - (0.5 - low) * 10, mean + (high - 0.5) * 10]


# Wilson Score interval callback:

@app.callback(
    Output('wilson_test_result', 'children'),
    Input('wilson_test_button', 'n_clicks'),
    State('wilson_test_sample', 'value'),
    State('wilson_test_mean', 'value'),
    State('wilson_test_confidence', 'value'),
    prevent_initial_call=True
)
def wilson(n_clicks, n, mean, conf):
    '''
    Function takes number of samples (n), mean value (mean) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    low, high = sm.stats.proportion.proportion_confint(
        n / 2, n, alpha=1 - conf, method="wilson")
    return [mean - (0.5 - low) * 10, mean + (high - 0.5) * 10]


# Percentile bootstrap Method

@app.callback(
    Output('bootstrap_test_result', 'children'),
    Input('bootstrap_test_button', 'n_clicks'),
    State('bootstrap_test_means', 'value'),
    State('bootstrap_test_confidence', 'value'),
    prevent_initial_call=True
)
def percentile_BM(n_clicks, means, conf):
    '''
    Function takes list of resamples means obtained from bootstrap (means) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    # As means temporary are served as text in format: '1,2,3,4,5,6...'
    means = means.split(',')
    map_object = map(int, means)
    means = list(map_object)

    means.sort()
    means = np.array(means)
    lower_bound = np.percentile(means, 100 * ((1 - conf) / 2))
    upper_bound = np.percentile(means, 100 * (conf + (1 - conf) / 2))
    # return [lower_bound, upper_bound]
    return "Lower bound: " + str(lower_bound) + " Upper bound: " + str(upper_bound)


# Standard method error
@app.callback(
    Output('standard_test_result', 'children'),
    Input('standard_test_button', 'n_clicks'),
    State('standard_test_mean', 'value'),
    State('standard_test_means', 'value'),
    State('standard_test_confidence', 'value'),
    prevent_initial_call=True
)
def std_method(n_click, mean, means, conf):
    '''
    Function takes mean of the data (mean), list of resamples means obtained from bootstrap (means) and confidence (conf).
    Returns lower and upper bounds for the confidence interval.
    '''
    # As means temporary are served as text in format: '1,2,3,4,5,6...'
    means = means.split(',')
    map_object = map(int, means)
    means = list(map_object)

    z = st.norm.ppf(1 - (1 - conf) / 2)
    se = np.std(means)
    print(se)
    lower_bound = mean - z * se
    upper_bound = mean + z * se
    return [lower_bound, upper_bound]


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
