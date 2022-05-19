import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from util import create_estimation_form
from constants import descriptions_dict


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

webpages_dict = {
    'navbar': navbar,
    'footer': html.Footer(html.P("Copyright 2022, Poznan University of Technology.", className="footer-text")),
    '/ci_holdout_wilson': create_estimation_form("ci", "Holdout Wilson", "holdout_wilson", 100),
    '/ci_holdout_clopper_pearson': create_estimation_form("ci", "Holdout Clopper-Pearson",
                                                          "holdout_clopper_pearson", 100),
    '/ci_holdout_langford': create_estimation_form("ci", "Holdout Langford", "holdout_langford", 100),
    '/ci_holdout_z_test': create_estimation_form("ci", "Holdout Z-test", "holdout_z_test", 50),
    '/ci_holdout_t_test': create_estimation_form("ci", "Holdout t-test", "holdout_t_test", 25),
    '/ci_progressive': create_estimation_form("ci", "Progressive validation", "progressive", 300),
    '/ci_cv': create_estimation_form("ci", "Cross-validation", "cv", 500, n_splits=10),
    '/ci_bootstrap': create_estimation_form("ci", "Bootstrapping", "bootstrap", 20, accuracy='0.48, 0.51, 0.48, 0.49, 0.48, 0.48, 0.49, 0.49, 0.50, 0.48, 0.48, 0.49, 0.62, 0.70, 0.69, 0.52, 0.50, 0.49, 0.49, 0.49, 0.50, 0.51, 0.50, 0.49, 0.50, 0.50, 0.49, 0.49, 0.49, 0.50, 0.49, 0.49, 0.50, 0.51, 0.50, 0.50, 0.51, 0.51, 0.49, 0.50, 0.49, 0.49, 0.49, 0.51, 0.49, 0.51, 0.51, 0.49, 0.50, 0.49'),

    '/sample_size_langford': create_estimation_form("sample_size", "Holdout Langford", "holdout_langford"),
    '/sample_size_z_test': create_estimation_form("sample_size", "Holdout Z-test", "holdout_z_test"),
    '/sample_size_cv': create_estimation_form("sample_size", "Cross-validation", "cv", n_splits=10),
    '/sample_size_bootstrap': create_estimation_form("sample_size", "Bootstrapping", "bootstrap"),
    '/sample_size_progressive': create_estimation_form("sample_size", "Progressive validation", "progressive"),

    '/confidence_level_langford': create_estimation_form("confidence_level", "Holdout Langford",
                                                         "holdout_langford", 100),
    '/confidence_level_z_test': create_estimation_form("confidence_level", "Holdout Z-test", "holdout_z_test", 50),
    '/confidence_level_t_test': create_estimation_form("confidence_level", "Holdout t-test", "holdout_t_test", 25),
    '/confidence_level_cv': create_estimation_form("confidence_level", "Cross-validation", "cv", 500, n_splits=10),
    '/confidence_level_bootstrap': create_estimation_form("confidence_level", "Bootstrapping", "bootstrap", 20, accuracy='0.48, 0.51, 0.48, 0.49, 0.48, 0.48, 0.49, 0.49, 0.50, 0.48, 0.48, 0.49, 0.62, 0.70, 0.69, 0.52, 0.50, 0.49, 0.49, 0.49, 0.50, 0.51, 0.50, 0.49, 0.50, 0.50, 0.49, 0.49, 0.49, 0.50, 0.49, 0.49, 0.50, 0.51, 0.50, 0.50, 0.51, 0.51, 0.49, 0.50, 0.49, 0.49, 0.49, 0.51, 0.49, 0.51, 0.51, 0.49, 0.50, 0.49'),
    '/confidence_level_progressive': create_estimation_form("confidence_level", "Progressive validation",
                                                            "progressive", 500),
}


def create_home_page(app):
    return html.Div(children=[
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
                                    ci_links, label="Confidence interval", color="primary",
                                    className="m-1", id="hero-ci-button"
                                ),
                                dbc.DropdownMenu(
                                    sample_size_links, label="Sample size", color="primary",
                                    className="m-1", id="hero-sample-size-button"
                                ),
                                dbc.DropdownMenu(
                                    confidence_level_links, label="Confidence level", color="primary",
                                    className="m-1", id="hero-confidence-level-button"
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
                                         style={"width": "100%", "margin": "20px 0px"}),
                                md=7, sm=12),
                    ]
                ),
                html.H2("About", className="landing-header"),
                dcc.Markdown(descriptions_dict["about"]),
                html.H2("References", className="landing-header"),
                dcc.Markdown(descriptions_dict["references"])
            ]),
    ], id="home"
    )
