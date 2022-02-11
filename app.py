from distutils.log import debug
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


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
from functions import plot_confidence_interval
import layouts

external_theme = [dbc.themes.COSMO]

app = dash.Dash(__name__, external_stylesheets=external_theme,
    suppress_callback_exceptions=True)
server = app.server







# Storing Home layout here due to possible circural imports:

home_text = '''### **How to use the app**
The application provides different methods for calculating confidence interval for obtained accuracy from different training techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from.

#### **Map of usage**
'''
home_text_2 = '''#### **More insightfull about options and methods**
 - **Holdout methods** - Holdout  is  when  one  splits  up  a  dataset  into  a  "train"  and "test"  set.  The  training  set  is  what  the  model  is  trained  on,  and  the  test  set is  used  to  see  how  well  that  model  performs  on  unseen  data.
 - **Bootstrap method** - Bootstrap is a resampling method by independently  sampling  with  replacement  from  an  existing  sample  data  with same sample size n, and performing inference among these resampled data.
 - **Cross-Validation method** - Cross-validation or "k-fold cross-validation" is when the dataset is randomly split up into k groups. One of the groups is used as the test set and the rest are used as the training set. The model is trained on the training set and scored on the test set. Then, the process is repeated until each unique group has been used as the test set.
 - **Progressive Validation method** - Progressive validation starts by first learning a hypothesis on the training set and then testing on the first example of the test set. Then, we train on the training set plus the first example of the test set and test on the second example of the test set. The process then continues. The progressive validation technique is used in data streams.'''

home_text_3 = ''' - **Holdout methods:**
   - **Z-test** - use when holdout sample size is big (>30) and the distribution of the test statistic can be approximated by a normal distribution
   - **T-test** - use when holdout sample size is small (<30) and the test statistic follows a normal distribution
   - **Loose test set bound** - use when you would like to be sure that the obtained interval will be at least of provided confidence, the interval may be much wider than the tighest possible one
   - **Clopper-Pearson** - use when you would like to be sure that the obtained interval will be at least of provided confidence, so the interval may be wider but not as wide as in the Loose test set bound
   - **Wilson score** - use to obtain the interval, which on average is precisely for the given confidence; do not use when your accuracy is close to 0 or 1
 - **Bootstrap method:**
   - **Percentile Bootstrap** - use when number of bootstrap resamples is big (at least 100) and you have accuracies from each resample
 - **Cross-Validation method:**
   - **Cross Validation** - use when you have an accuracy from CV and you know number of samples and number of folds
 - **Progressive Validation method:**
   - **Progressive Validation** - use when you have an accuracy from Progressive Validation technique and you know test set size
    
Moreover, for z-test, t-test and loose test set bound there are reverse tests. With their help, when you know what confidence interval you want to obtain at a given confidence, tests will return number of samples needed for a holdout method.
For z-test and loose test set bound, if you know confidence interval and number of holdout samples, you can obtain confidence.'''


HOME = html.Div(children=[
    dcc.Markdown(home_text),
    html.Img(src=app.get_asset_url("Main_tree.png"), alt="Description of 4 options to choose from (Holdout, Bootstrap, Cross-Validation, Progressive-Validation)", width="75%", height="75%"), # width="500", height="600"
    # html.Img(src=app.get_asset_url("Main_tree.png"),
    dcc.Markdown(home_text_2),
    dcc.Markdown(home_text_3),
], id='home')

layouts.elements['/home'] = HOME




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