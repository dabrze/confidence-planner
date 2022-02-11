from distutils.log import debug
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os
import io
import base64
import pandas as pd
import pathlib

# Graph generation imports
import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle

palette = cycle(px.colors.qualitative.Antique)

def plot_confidence_interval(confidence_intervals, user_def):
    layout_ = go.Layout({"yaxis": {"title":"Confidence"},
                       "xaxis": {"title":"Confidence Interval for given confidence"},
                       "template": 'plotly_white',
                       "showlegend": False})
    
    intervals = [f'{user_def}%', '90%', '95%', '98%', '99%']

    fig = go.Figure(layout=layout_)
    fig.update_xaxes(range=[-3,103])
    fig.update_yaxes(showgrid=True, type='category')

    for conf_int, category in zip(confidence_intervals, intervals):
        x = [round(conf_int[0], 2), round(conf_int[1], 2)]
        y = [category, category]
        fig.add_trace(go.Scatter(x=x, y=y, text=x,
                    mode='lines+markers+text',
                    textposition='top center',
                    line_color=next(palette),
                    name=category))
    #fig.show()
    return fig

iterval_orders = ('Your confidence interval (for {}% confidence):', 'Confidence interval for 90% confidence:', 'Confidence interval for 95% confidence:'
                , 'Confidence interval for 98% confidence:', 'Confidence interval for 99% confidence:')

# Test code imports

from tests.holdout.z_test import ztest_pr, reverse_ztest_pr, reverse_ztest_pr_conf
from tests.holdout.t_test import ttest_pr, reverse_ttest_pr_conf
from tests.holdout.loose_langford import loose_langford, loose_langford_reverse,  loose_langford_conf
from tests.holdout.clooper_pearson import clopper_pearson
from tests.holdout.wilson import wilson
from tests.bootstrap.percentile_bootstrap import percentile_BM
from tests.cross_validation.cross_validation import cv_interval
from tests.progressive_validation.progressive_validation import prog_val
import layouts

external_theme = [dbc.themes.COSMO]

app = dash.Dash(__name__, external_stylesheets=external_theme,
    suppress_callback_exceptions=True)
server = app.server

# The layout of the home all pages (only the last div changes while moving to different page)
app.layout = html.Div(
    id='entire_app',
    children=[
        dcc.Location(id='url', refresh=False),
        layouts.elements['navbar'],
        html.Div(children=layouts.elements['/home'],
                id='page_content', className='page_content'),
        # layouts.elements['footer'],
    ],
    
)

# Callback taking care of changing webpage content with respect to given url
@app.callback(Output('page_content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        try:
            page = layouts.elements['/home']
            print('Home webpage already created')
            return page
        except Exception as ex:
            print('No home webpage found' + str(ex))
            return 'No home webpage found' + str(ex)
    else:
        try:
            page = layouts.elements[str(pathname)]
            return page
        except Exception as ex:
            return 'Ups... Something went wrong.\n404 Error, Website not found...' + str(ex)


# Z TEST callback:

@app.callback(
    Output('z_test_result', 'children'), # Text form output
    Output('z_test_result_graph', 'figure'), # Graph form output
    Input('z_test_button', 'n_clicks'), # Button clicks
    State('z_test_sample', 'value'), # Number of samples
    State('z_test_accuracy', 'value'), # Accuracy
    State('z_test_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def z_test_callback(n_click, n, accuracy, confidence):

    intervals = ztest_pr(n, accuracy, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot



# Reverse Z TEST (samples) callback:

@app.callback(
    Output('z_test_rev_samples_result', 'children'),
    Input('z_test_rev_samples_button', 'n_clicks'),
    State('z_test_rev_samples_diff', 'value'),
    State('z_test_rev_samples_confidence', 'value'),
    prevent_initial_call=False
)
def reverse_z_test_samples_callback(n_clicks, difference, confidence):
    return html.Div('Estimated number of samples needed: ' + str(round(reverse_ztest_pr(difference, confidence),0)))


# Reverse Z TEST (confidence) callback:

@app.callback(
    Output('z_test_rev_confidence_result', 'children'),
    Input('z_test_rev_confidence_button', 'n_clicks'),
    State('z_test_rev_confidence_sample', 'value'),
    State('z_test_rev_confidence_diff', 'value'),
    prevent_initial_call=False
)
def reverse_z_test_confidence_callback(n_clicks, n, difference):
    return html.Div('Estimated confidence needed: ' + str(round(reverse_ztest_pr_conf(difference, n)*100, 4)) + '%')






# T TEST callback

@app.callback(
    Output('t_test_result', 'children'), # Text form output
    Output('t_test_result_graph', 'figure'), # Graph form output
    Input('t_test_button', 'n_clicks'), # Button clicks
    State('t_test_sample', 'value'), # Number of samples
    State('t_test_accuracy', 'value'), # Accuracy
    State('t_test_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def t_test_callback(n_click, n, accuracy, confidence):

    intervals = ttest_pr(n, accuracy, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot


# Reverse T TEST (confidence) callback:

@app.callback(
    Output('t_test_rev_confidence_result', 'children'),
    Input('t_test_rev_confidence_button', 'n_clicks'),
    State('t_test_rev_confidence_sample', 'value'),
    State('t_test_rev_confidence_diff', 'value'),
    prevent_initial_call=False
)
def reverse_t_test_confidence_callback(n_clicks, n, difference):
    return html.Div('Estimated confidence needed: ' + str(round(reverse_ttest_pr_conf(difference, n)*100, 4)) + '%')






# LOOSE LANGFORD TEST callback:

@app.callback(
    Output('loose_langford_result', 'children'), # Text form output
    Output('loose_langford_result_graph', 'figure'), # Graph form output
    Input('loose_langford_button', 'n_clicks'), # Button clicks
    State('loose_langford_sample', 'value'), # Number of samples
    State('loose_langford_accuracy', 'value'), # Accuracy
    State('loose_langford_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def loose_langford_callback(n_click, n, accuracy, confidence):

    intervals = loose_langford(n, accuracy, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot



# Reverse LOOSE LANGFORD TEST (samples) callback:

@app.callback(
    Output('loose_langford_rev_samples_result', 'children'),
    Input('loose_langford_rev_samples_button', 'n_clicks'),
    State('loose_langford_rev_samples_diff', 'value'),
    State('loose_langford_rev_samples_confidence', 'value'),
    prevent_initial_call=False
)
def reverse_loose_langford_samples_callback(n_clicks, difference, confidence):
    return html.Div('Estimated number of samples needed: ' + str(round(loose_langford_reverse(difference, confidence),0)))


# Reverse LOOSE LANGFORD TEST (confidence) callback:

@app.callback(
    Output('loose_langford_rev_confidence_result', 'children'),
    Input('loose_langford_rev_confidence_button', 'n_clicks'),
    State('loose_langford_rev_confidence_sample', 'value'),
    State('loose_langford_rev_confidence_diff', 'value'),
    prevent_initial_call=False
)
def reverse_loose_langford_confidence_callback(n_clicks, n, difference):
    return html.Div('Estimated confidence needed: ' + str(round(loose_langford_conf(difference, n)*100, 4)) + '%')






# CLOPPER PEARSON TEST callback:

@app.callback(
    Output('clopper_pearson_result', 'children'), # Text form output
    Output('clopper_pearson_result_graph', 'figure'), # Graph form output
    Input('clopper_pearson_button', 'n_clicks'), # Button clicks
    State('clopper_pearson_sample', 'value'), # Number of samples
    State('clopper_pearson_accuracy', 'value'), # Accuracy
    State('clopper_pearson_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def clopper_pearson_callback(n_click, n, accuracy, confidence):

    intervals = clopper_pearson(n, accuracy, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot





# WILSON TEST callback:

@app.callback(
    Output('wilson_result', 'children'), # Text form output
    Output('wilson_result_graph', 'figure'), # Graph form output
    Input('wilson_button', 'n_clicks'), # Button clicks
    State('wilson_sample', 'value'), # Number of samples
    State('wilson_accuracy', 'value'), # Accuracy
    State('wilson_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def wilson_callback(n_click, n, accuracy, confidence):

    intervals = wilson(n, accuracy, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot




# PERCENTILE BOOTSTRAP METHOD callback

@app.callback(
    Output('bootstrap_result', 'children'), # Text form output
    Output('bootstrap_result_graph', 'figure'), # Graph form output
    Input('bootstrap_button', 'n_clicks'), # Button clicks
    State('bootstrap_samples', 'value'), # Number of samples
    State('bootstrap_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def percentile_bootstrap_callback(n_click, samples, confidence):

    samples = [float(sample) for sample in samples.split(',')]

    intervals = percentile_BM(samples, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot

# PERCENTILE BOOTSTRAP METHOD file upload


# @app.callback(
#     Output('useless', 'children'),
#     Input('upload_data', 'filename'),
#     Input('upload_data', 'contents'),
# )
# def percentile_bootstrap_file_upload(filename, content):
#     if content is not None:
#         childer
#     print('Filename and fragment of content:', filename, type(content))
#     return(html.Div(f'Hello its me {filename}'))

# def parse_contents(contents, filename, date):
#     content_type, content_string = contents.split(',')

#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#             return html.Div(df.to_string())
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#             return html.Div(df.to_string())
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])

# @app.callback(Output('useless', 'children'),
#               Input('upload_data', 'contents'),
#               State('upload_data', 'filename'),
#               State('upload_data', 'last_modified'),
#               prevent_initial_call=True)
# def update_output(contents, filename, date):
#     if contents is not None:
#         children = parse_contents(contents, filename, date)
#         return children





# CROSS VALIDATION TEST callback:

@app.callback(
    Output('cross_validation_result', 'children'), # Text form output
    Output('cross_validation_result_graph', 'figure'), # Graph form output
    Input('cross_validation_button', 'n_clicks'), # Button clicks
    State('cross_validation_sample', 'value'), # Number of samples
    State('cross_validation_folds', 'value'), # Number of samples
    State('cross_validation_accuracy', 'value'), # Accuracy
    State('cross_validation_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def cross_validation_callback(n_click, n, k, accuracy, confidence):

    intervals = cv_interval(n, k, accuracy, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot






# PROGRESSIVE VALIDATION TEST callback:

@app.callback(
    Output('progressive_validation_result', 'children'), # Text form output
    Output('progressive_validation_result_graph', 'figure'), # Graph form output
    Input('progressive_validation_button', 'n_clicks'), # Button clicks
    State('progressive_validation_sample', 'value'), # Number of samples from the test set
    State('progressive_validation_accuracy', 'value'), # Accuracy
    State('progressive_validation_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def progressive_validation_callback(n_click, n, accuracy, confidence):

    intervals = prog_val(n, accuracy, confidence)

    _ = 0 # variable for adding User defined confidence level to presentation
    divs = []

    for inter_desc, interval in zip(iterval_orders, intervals):
        lower = str(round(interval[0], 2)) + '%'
        upper = str(round(interval[1], 2)) + '%'

        if _ == 0: # updating values defined by the user
            inter_desc = "Your confidence interval (for {}% confidence):".format(confidence*100)
            _ = 1
        
        div_str = inter_desc + ' ' + lower + ' - ' + upper
        divs.append(html.Div(div_str))



    plot = plot_confidence_interval(intervals, confidence*100)

    return divs, plot

if __name__ == '__main__':
    app.run_server(debug=False)