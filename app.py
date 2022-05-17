from distutils.log import debug
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import confidence_planner as cp
from util import (
    plot_confidence_interval,
    ci_callback,
    sample_size_callback,
    confidence_level_callback,
)
import layouts

external_theme = [dbc.themes.COSMO]

app = dash.Dash(
    __name__, external_stylesheets=external_theme, suppress_callback_exceptions=True
)
server = app.server


######################## HOME WEBPAGE EDIT ########################
# Storing Home layout here due to possible circural imports:

home_text = """### **How to use the app**
The application provides different methods for calculating confidence interval for obtained accuracy from different training techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from.

#### **Map of usage**
"""
home_text_2 = """#### **More insightfull about options and methods**
 - **Holdout methods** - Holdout  is  when  one  splits  up  a  dataset  into  a  "train"  and "test"  set.  The  training  set  is  what  the  model  is  trained  on,  and  the  test  set is  used  to  see  how  well  that  model  performs  on  unseen  data.
 - **Bootstrap method** - Bootstrap is a resampling method by independently  sampling  with  replacement  from  an  existing  sample  data  with same sample size n, and performing inference among these resampled data.
 - **Cross-Validation method** - Cross-validation or "k-fold cross-validation" is when the dataset is randomly split up into k groups. One of the groups is used as the test set and the rest are used as the training set. The model is trained on the training set and scored on the test set. Then, the process is repeated until each unique group has been used as the test set.
 - **Progressive Validation method** - Progressive validation starts by first learning a hypothesis on the training set and then testing on the first example of the test set. Then, we train on the training set plus the first example of the test set and test on the second example of the test set. The process then continues. The progressive validation technique is used in data streams."""

home_text_3 = """ - **Holdout methods:**
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
For z-test and loose test set bound, if you know confidence interval and number of holdout samples, you can obtain confidence."""


HOME = html.Div(
    children=[
        dcc.Markdown(home_text),
        html.Img(
            src=app.get_asset_url("map.svg"),
            alt="Description of 4 options to choose from (Holdout, Bootstrap, Cross-Validation, Progressive-Validation)",
            width="75%",
            height="75%",
        ),  # width="500", height="600"
        # html.Img(src=app.get_asset_url("Main_tree.png"),
        dcc.Markdown(home_text_2),
        dcc.Markdown(home_text_3),
        layouts.elements["footer"],
    ],
    id="home",
)

layouts.elements["/home"] = HOME

######################## HOME WEBPAGE EDIT ########################

# The layout of the home all pages (only the last div changes while moving to different page)
app.layout = html.Div(
    id="entire_app",
    children=[
        dcc.Location(id="url", refresh=False),
        layouts.elements["navbar"],
        html.Div(
            children=layouts.elements["/home"],
            id="page_content",
            className="page_content",
        ),
        # layouts.elements['footer'],
    ],
)

# Callback taking care of changing webpage content with respect to given url
@app.callback(Output("page_content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        try:
            page = layouts.elements["/home"]
            print("Home webpage already created")
            return page
        except Exception as ex:
            print("No home webpage found" + str(ex))
            return "No home webpage found" + str(ex)
    else:
        try:
            page = layouts.elements[str(pathname)]
            return page
        except Exception as ex:
            return (
                "Ups... Something went wrong.\n404 Error, Website not found..."
                + str(ex)
            )


##########################################
# Confidence interval estimation callbacks
##########################################


for method in ['holdout_wilson', 'holdout_langford', 'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test',
               'progressive', 'cv']:
    app.callback(
        Output(f"{method}_result", "children"),
        Output(f"{method}_result_graph", "figure"),
        Input(f"{method}_button", "n_clicks"),
        State(f"{method}_sample", "value"),
        State(f"{method}_accuracy", "value"),
        State(f"{method}_confidence", "value"),
        State(f"{method}", "id"),
        State(f"{method}_folds", "value"),
    )(ci_callback)


@app.callback(
    Output("bootstrap_result", "children"),
    Output("bootstrap_result_graph", "figure"),
    Input("bootstrap_button", "n_clicks"),
    State("bootstrap_samples", "value"),
    State("bootstrap_confidence", "value"),
    prevent_initial_call=False,
)
def ci_bootstrap_callback(n_click, accuracies, confidence_level):
    accuracies_float = [float(accuracy) for accuracy in accuracies.split(",")]
    return ci_callback(n_click, None, accuracies_float, confidence_level, method="bootstrap")


##########################################
# Sample size estimation callbacks
##########################################


@app.callback(
    Output("z_test_rev_samples_result", "children"),
    Input("z_test_rev_samples_button", "n_clicks"),
    State("z_test_rev_samples_diff", "value"),
    State("z_test_rev_samples_confidence", "value"),
    prevent_initial_call=False,
)
def sample_size_holdout_z_test(n_clicks, interval_radius, confidence_level):
    return sample_size_callback(
        interval_radius, confidence_level, method="holdout_z_test"
    )


@app.callback(
    Output("loose_langford_rev_samples_result", "children"),
    Input("loose_langford_rev_samples_button", "n_clicks"),
    State("loose_langford_rev_samples_diff", "value"),
    State("loose_langford_rev_samples_confidence", "value"),
    prevent_initial_call=False,
)
def sample_size_holdout_langford(n_clicks, interval_radius, confidence_level):
    return sample_size_callback(
        interval_radius, confidence_level, method="holdout_langford"
    )


##########################################
# Confidence level estimation callbacks
##########################################


@app.callback(
    Output("z_test_rev_confidence_result", "children"),
    Input("z_test_rev_confidence_button", "n_clicks"),
    State("z_test_rev_confidence_sample", "value"),
    State("z_test_rev_confidence_diff", "value"),
    prevent_initial_call=False,
)
def reverse_z_test_confidence_callback(n_clicks, sample_size, interval_radius):
    return confidence_level_callback(
        sample_size, interval_radius, method="holdout_z_test"
    )


@app.callback(
    Output("t_test_rev_confidence_result", "children"),
    Input("t_test_rev_confidence_button", "n_clicks"),
    State("t_test_rev_confidence_sample", "value"),
    State("t_test_rev_confidence_diff", "value"),
    prevent_initial_call=False,
)
def reverse_t_test_confidence_callback(n_clicks, sample_size, interval_radius):
    return confidence_level_callback(
        sample_size, interval_radius, method="holdout_t_test"
    )


@app.callback(
    Output("loose_langford_rev_confidence_result", "children"),
    Input("loose_langford_rev_confidence_button", "n_clicks"),
    State("loose_langford_rev_confidence_sample", "value"),
    State("loose_langford_rev_confidence_diff", "value"),
    prevent_initial_call=False,
)
def reverse_loose_langford_confidence_callback(n_clicks, sample_size, interval_radius):
    return confidence_level_callback(
        sample_size, interval_radius, method="holdout_langford"
    )


if __name__ == "__main__":
    app.run_server(debug=False)
