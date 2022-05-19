from click import style
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from util import create_estimation_form


ci_links = [
    dbc.DropdownMenuItem("Holdout", header=True),
    dbc.DropdownMenuItem("Wilson", href="/ci_holdout_wilson"),
    dbc.DropdownMenuItem("Clopper-Pearson", href="/ci_holdout_clopper_pearson"),
    dbc.DropdownMenuItem("Langford", href="/ci_holdout_langford"),
    dbc.DropdownMenuItem("Z-test", href="/ci_holdout_z_test"),
    dbc.DropdownMenuItem("t-test", href="/ci_holdout_t_test"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Cross-validation", header=True),
    dbc.DropdownMenuItem("Blum", href="/ci_cv"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Bootstrapping", header=True),
    dbc.DropdownMenuItem("Percentiles", href="/ci_bootstrap"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Progressive validation", header=True),
    dbc.DropdownMenuItem("Langford progressive", href="/ci_progressive"),
]

sample_size_links = [
    dbc.DropdownMenuItem("Holdout", header=True),
    dbc.DropdownMenuItem("Langford", href="/sample_size_langford"),
    dbc.DropdownMenuItem("Z-test", href="/sample_size_z_test"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Cross-validation", header=True),
    dbc.DropdownMenuItem("Blum", href="/sample_size_cv"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Bootstrapping", header=True),
    dbc.DropdownMenuItem("Z-test", href="/sample_size_bootstrap"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Progressive validation", header=True),
    dbc.DropdownMenuItem("Langford progressive", href="/sample_size_progressive"),
]

confidence_level_links = [
    dbc.DropdownMenuItem("Holdout", header=True),
    dbc.DropdownMenuItem("Langford", href="/confidence_level_langford"),
    dbc.DropdownMenuItem("Z-test", href="/confidence_level_z_test"),
    dbc.DropdownMenuItem("t-test", href="/confidence_level_t_test"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Cross-validation", header=True),
    dbc.DropdownMenuItem("Blum", href="/confidence_level_cv"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Bootstrapping", header=True),
    dbc.DropdownMenuItem("Percentiles", href="/confidence_level_bootstrap"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Progressive validation", header=True),
    dbc.DropdownMenuItem("Langford progressive", href="/confidence_level_progressive"),
]

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=ci_links,
            nav=True,
            in_navbar=True,
            direction='down',
            label="Estimate confidence interval",
        ),
        dbc.DropdownMenu(
            children=sample_size_links,
            nav=True,
            in_navbar=True,
            direction='down',
            label="Estimate sample size",
        ),
        dbc.DropdownMenu(
            children=confidence_level_links,
            nav=True,
            in_navbar=True,
            direction='down',
            label="Estimate confidence level",
        ),
        dbc.NavItem(dbc.NavLink("About", href="/home"))
    ],
    brand="Confidence Planner",
    brand_href="/home",
)

descriptions_dict = {
    'holdout_wilson': 'TODO',
    'holdout_langford': 'TODO',
    'holdout_clopper_pearson': 'TODO',
    'holdout_z_test': 'TODO',
    'holdout_t_test': 'TODO',
    'progressive': 'TODO',
    'cv': 'TODO',
    'bootstrap': 'TODO',

    'about': """
The Confidence Planner website is a companion website to conifdence-planner python package that can be found on PyPI and
 Github: https://github.com/dabrze/confidence-planner. The package will allow you to integrate confidence interval
 estimations into your sklearn-based or any other machine learning analyses. If you have any questions or comments 
 please let us know in the project's [github discussion page](https://github.com/dabrze/confidence-planner/discussions).

### Contributors
 - Antoni Klorek, Poznan University of Technology
 - Karol Roszak, Poznan University of Technology
 - Dariusz Brzezinski, Poznan University of Technology""",

    'methods': """
**Holdout methods** Confidence and sample size estimations for accuracy on holdout test sets can be done with multiple methods.
The simplest method is to assume a normal distribution of the classifiers accuracy and then use the Z-test or t-test \[1\]. However,
there exist good approximations directly for binomial (0-1 loss) distribution. The Wilson method \[5\] offers the tightest confidence bounds
but might be slightly less reliable when accuracy is very close to 0.0 or 1.0. The Clopper-Pearson approximation \[4\] is more conservative, and the
Langford approximation \[1\] (based on the Hoeffding inequality) is the most conservative. For sample size and confidence level 
estimation, only the Langford and normal-distribution approximations are available.

**Cross-Validation method** Estimations for k-fold cross-validation experiments can be done using Blum's method \[2\]. This
 approximation is based on the Hoeffding inequality and is very conservative. It boils down to the fact that the confidence
 of k-fold experiment is no worse than a 1/k holdout experiment. Therefore, increasing the number of folds will make the
 confidence intervals wider.
 
**Bootstrap method** To estimate the confidence interval or confidence level of a bootstrapping experiment one can calculate
the percentiles of accuracies from all the bootstraps \[3\]. The larger the number of bootstraps, the more reliable the estimation will be. 
To estimate the sample size, one can assume a normal distribution of the bootstrap results and use the Z-test method.

**Progressive validation** Progressive validation is also known as time series validation, rolling validation, or the 
test-then-train method. In case of progressive validation experiments, one can use Langford's approximation and 
provide the size of the entire (rolled) dataset as the sample size \[2\].""",
    
    "references": """
1. Langford J. (2005) Tutorial on practical prediction theory for classification. *Journal of Machine Learning Research* 6, 273–306, [link](https://www.jmlr.org/papers/volume6/langford05a/langford05a.pdf).
2. Blum A., Kalai, A., Langford, J. (1999) Beating the hold-out: Bounds for k-fold and progressive cross-validation. *Proceedings of the Twelfth Annual Conference on Computational Learning Theory, COLT 1999*, pp. 203–208, [link](https://www.ri.cmu.edu/pub_files/pub1/blum_a_1999_1/blum_a_1999_1.pdf).
3. Puth M.T., Neuhauser M., Ruxton G.(2015) On the variety of methods for calculating confidence intervals by bootstrapping. *The Journal of Animal Ecology* 84, [link](https://doi.org/10.1111/1365-2656.12382).
4. Clopper C.J., Pearson E.S. (1934) The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4), 404–413, [link](http://www.jstor.org/stable/2331986).
5. Wilson E.B. (1927) Probable inference, the law of succession, and statistical inference. *Journal of the American Statistical Association* 22(158), 209–212, [link](http://www.jstor.org/stable/2276774).
"""
}

webpages_dict = {
    'navbar': navbar,
    'footer': html.Footer(html.P("Copyright 2022, Poznan University of Technology.", className="footer-text")),
    '/ci_holdout_wilson': create_estimation_form("ci", "Holdout Wilson", "holdout_wilson", descriptions_dict["holdout_wilson"], 100),
    '/ci_holdout_clopper_pearson': create_estimation_form("ci", "Holdout Clopper-Pearson", "holdout_clopper_pearson", descriptions_dict["holdout_clopper_pearson"], 100),
    '/ci_holdout_langford': create_estimation_form("ci", "Holdout Langford", "holdout_langford", descriptions_dict["holdout_langford"], 100),
    '/ci_holdout_z_test': create_estimation_form("ci", "Holdout Z-test", "holdout_z_test", descriptions_dict["holdout_z_test"], 50),
    '/ci_holdout_t_test': create_estimation_form("ci", "Holdout t-test", "holdout_t_test", descriptions_dict["holdout_t_test"], 25),
    '/ci_progressive': create_estimation_form("ci", "Progressive validation", "progressive", descriptions_dict["progressive"], 300),
    '/ci_cv': create_estimation_form("ci", "Cross-validation", "cv", descriptions_dict["cv"], 500, n_splits=10),
    '/ci_bootstrap': create_estimation_form("ci", "Bootstrapping", "bootstrap", descriptions_dict["bootstrap"], 20, accuracy='0.48, 0.51, 0.48, 0.49, 0.48, 0.48, 0.49, 0.49, 0.50, 0.48, 0.48, 0.49, 0.62, 0.70, 0.69, 0.52, 0.50, 0.49, 0.49, 0.49, 0.50, 0.51, 0.50, 0.49, 0.50, 0.50, 0.49, 0.49, 0.49, 0.50, 0.49, 0.49, 0.50, 0.51, 0.50, 0.50, 0.51, 0.51, 0.49, 0.50, 0.49, 0.49, 0.49, 0.51, 0.49, 0.51, 0.51, 0.49, 0.50, 0.49'),
    '/sample_size_langford': create_estimation_form("sample_size", "Holdout Langford", "holdout_langford", descriptions_dict["holdout_langford"]),
    '/sample_size_z_test': create_estimation_form("sample_size", "Holdout Z-test", "holdout_z_test", descriptions_dict["holdout_z_test"]),
    '/sample_size_cv': create_estimation_form("sample_size", "Cross-validation", "cv", descriptions_dict["cv"], n_splits=10),
    '/sample_size_bootstrap': create_estimation_form("sample_size", "Bootstrapping", "bootstrap", descriptions_dict["bootstrap"]),
    '/sample_size_progressive': create_estimation_form("sample_size", "Progressive validation", "progressive", descriptions_dict["progressive"]),

    '/confidence_level_langford': create_estimation_form("confidence_level", "Holdout Langford", "holdout_langford", descriptions_dict["holdout_langford"], 100),
    '/confidence_level_z_test': create_estimation_form("confidence_level", "Holdout Z-test", "holdout_z_test", descriptions_dict["holdout_z_test"], 50),
    '/confidence_level_t_test': create_estimation_form("confidence_level", "Holdout t-test", "holdout_t_test", descriptions_dict["holdout_t_test"], 25),
    '/confidence_level_cv': create_estimation_form("confidence_level", "Cross-validation", "cv", descriptions_dict["cv"], 500, n_splits=10),
    '/confidence_level_bootstrap': create_estimation_form("confidence_level", "Bootstrapping", "bootstrap", descriptions_dict["bootstrap"], 20, accuracy='0.48, 0.51, 0.48, 0.49, 0.48, 0.48, 0.49, 0.49, 0.50, 0.48, 0.48, 0.49, 0.62, 0.70, 0.69, 0.52, 0.50, 0.49, 0.49, 0.49, 0.50, 0.51, 0.50, 0.49, 0.50, 0.50, 0.49, 0.49, 0.49, 0.50, 0.49, 0.49, 0.50, 0.51, 0.50, 0.50, 0.51, 0.51, 0.49, 0.50, 0.49, 0.49, 0.49, 0.51, 0.49, 0.51, 0.51, 0.49, 0.50, 0.49'),
    '/confidence_level_progressive': create_estimation_form("confidence_level", "Progressive validation", "progressive", descriptions_dict["progressive"], 500),
}


def create_home_page(app):
    return html.Div(
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
                                          "start estimating. If you would rather estimate directly in your code, "
                                          "take a look at the confidence-planner python package available on "),
                                html.A("GitHub", href="https://github.com/dabrze/confidence-planner"),
                                html.Span(".")
                            ],
                            id="hero-lead",
                        ),
                        html.Div(
                            [
                                dbc.DropdownMenu(
                                    ci_links, label="Confidence interval", color="primary", className="m-1", id="hero-ci-button"
                                ),
                                dbc.DropdownMenu(
                                    sample_size_links, label="Sample size", color="primary", className="m-1", id="hero-sample-size-button"
                                ),
                                dbc.DropdownMenu(
                                    confidence_level_links, label="Confidence level", color="primary", className="m-1", id="hero-confidence-level-button"
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
                        dbc.Col(dcc.Markdown(descriptions_dict["methods"]), md=5, sm=12),
                        dbc.Col(html.Img(src=app.get_asset_url("map.svg"), alt="Map of estimation methods",
                                         style={"width": "100%"}),
                                md=7, sm=12),
                    ]
                ),
                html.H2("About", className="landing-header"),
                dcc.Markdown(descriptions_dict["about"]),
                html.H2("References", className="landing-header"),
                dcc.Markdown(descriptions_dict["references"])
            ]),
    ],
    id="home",
)