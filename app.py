from distutils.log import debug
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import confidence_planner as cp
from components.texts import about_text
from util import (
    plot_confidence_interval,
    ci_callback,
    sample_size_callback,
    confidence_level_callback,
)
import layouts

FONTS = "https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i"
GOOGLE_FONTS_PRECONNECT = { "rel": "preconnect", "href": "https://fonts.googleapis.com" }
GOOGLE_FONTS_GSTATIC = { "rel": "preconnect", "href": "https://fonts.gstatic.com", "crossorigin": "anonymous"}

external_theme = [dbc.themes.BOOTSTRAP, GOOGLE_FONTS_PRECONNECT, GOOGLE_FONTS_GSTATIC, FONTS]

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
home_text_2 = """
**Holdout methods** - Holdout  is  when  one  splits  up  a  dataset  into  a  "train"  and "test"  set.  The  training  set  is  what  the  model  is  trained  on,  and  the  test  set is  used  to  see  how  well  that  model  performs  on  unseen  data.

**Bootstrap method** - Bootstrap is a resampling method by independently  sampling  with  replacement  from  an  existing  sample  data  with same sample size n, and performing inference among these resampled data.

**Cross-Validation method** - Cross-validation or "k-fold cross-validation" is when the dataset is randomly split up into k groups. One of the groups is used as the test set and the rest are used as the training set. The model is trained on the training set and scored on the test set. Then, the process is repeated until each unique group has been used as the test set.

**Progressive Validation method** - Progressive validation starts by first learning a hypothesis on the training set and then testing on the first example of the test set. Then, we train on the training set plus the first example of the test set and test on the second example of the test set. The process then continues. The progressive validation technique is used in data streams."""

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
        dbc.Jumbotron(
            [
                dbc.Container(
                    [
                        html.H1("Confidence planner"),
                        html.P(
                            [
                                html.Span("This application offers eight different procedures that will help you "
                                          "determine and justify prediction confidence intervals, test set sizes, "
                                          "and confidence levels from holdout, bootstrap, cross-validation, and "
                                          "progressive validation experiments. Use the menu or the buttons below to "
                                          "start estimating. If you would rather estimate directly in your Python code, "
                                          "take a look at the confidence-planner package available on "),
                                html.A("GitHub", href="https://github.com/dabrze/confidence-planner"),
                                html.Span(".")
                            ],
                            id="hero-lead",
                        ),
                        html.Div(
                            [
                                dbc.DropdownMenu(
                                    layouts.ci_links, label="Confidence interval", color="primary", className="m-1", id="hero-ci-button"
                                ),
                                dbc.DropdownMenu(
                                    layouts.sample_size_links, label="Sample size", color="primary", className="m-1", id="hero-sample-size-button"
                                ),
                                dbc.DropdownMenu(
                                    layouts.confidence_level_links, label="Confidence level", color="primary", className="m-1", id="hero-confidence-level-button"
                                )
                            ], style={"display": "inline-flex", "flexWrap": "wrap"}, id="hero-action-buttons"
                        ),
                    ], className="text-center"),
            ], id="hero"
        ),
        dbc.Container(
            [
                html.H2("Estimation methods", className="landing-header"),
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown(home_text_2), md=5, sm=12),
                        dbc.Col(html.Img(src=app.get_asset_url("map.svg"), alt="Map of estimation methods",
                                         style={"width": "100%"}),
                                md=7, sm=12),
                    ]
                ),
                html.H2("About", className="landing-header"),
                dcc.Markdown('''
The **Prediction Confidence Planner** application provides different methods for calculating confidence interval for obtained accuracy from different training techniques. The aim of the confidence interval is to measure the degree of uncertainty or certainty in a sampling method. There are four available options and number of tests to choose from.

### Contributors
 - Antoni Klorek, Poznan University of Technology
 - Karol Roszak, Poznan University of Technology
 - Dariusz Brzezinski, Poznan University of Technology'''),
                html.H2("References", className="landing-header"),
                dcc.Markdown('''
1. Langford J. (2005) Tutorial on practical prediction theory for classification. *Journal of Machine Learning Research* 6, 273–306, [link](https://www.jmlr.org/papers/volume6/langford05a/langford05a.pdf).
2. Blum A., Kalai, A., Langford, J. (1999) Beating the hold-out: Bounds for k-fold and progressive cross-validation. *Proceedings of the Twelfth Annual Conference on Computational Learning Theory, COLT 1999*, pp. 203–208, [link](https://www.ri.cmu.edu/pub_files/pub1/blum_a_1999_1/blum_a_1999_1.pdf).
3. Puth M.T., Neuhauser M., Ruxton G.(2015) On the variety of methods for calculating confidence intervals by bootstrapping. *The Journal of Animal Ecology* 84, [link](https://doi.org/10.1111/1365-2656.12382).
4. Clopper C.J., Pearson E.S. (1934) The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4), 404–413, [link](http://www.jstor.org/stable/2331986).
5. Wilson E.B. (1927) Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association* 22(158), 209–212, [link](http://www.jstor.org/stable/2276774).
'''),
                    layouts.elements["footer"]
            ]),
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


for method in ['holdout_wilson', 'holdout_langford', 'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test',
               'progressive', 'cv', 'bootstrap']:
    app.callback(
        Output(f"ci_{method}_result", "children"),
        Output(f"ci_{method}_result_graph", "figure"),
        Input(f"ci_{method}_sample", "value"),
        Input(f"ci_{method}_accuracy", "value"),
        Input(f"ci_{method}_confidence", "value"),
        Input(f"ci_{method}", "id"),
        Input(f"ci_{method}_folds", "value"),
    )(ci_callback)


for method in ['holdout_langford', 'holdout_z_test', 'progressive', 'cv', 'bootstrap']:
    app.callback(
        Output(f"sample_size_{method}_result", "children"),
        Input(f"sample_size_{method}_interval_radius", "value"),
        Input(f"sample_size_{method}_confidence", "value"),
        Input(f"sample_size_{method}", "id"),
        Input(f"sample_size_{method}_folds", "value"),
    )(sample_size_callback)


for method in ['holdout_langford', 'holdout_z_test', 'holdout_t_test', 'progressive', 'cv', 'bootstrap']:
    app.callback(
        Output(f"confidence_level_{method}_result", "children"),
        Input(f"confidence_level_{method}_sample", "value"),
        Input(f"confidence_level_{method}_interval_radius", "value"),
        Input(f"confidence_level_{method}", "id"),
        Input(f"confidence_level_{method}_folds", "value"),
    )(confidence_level_callback)


if __name__ == "__main__":
    app.run_server(debug=False)
