from click import style
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import components.texts as texts
from util import create_estimation_form

marks_interval={
        0: {'label': '0%', 'style': {'color': 'black'}},
        0.1: {'label': '10%', 'style': {'color': 'black'}},
        0.2: {'label': '20%', 'style': {'color': 'black'}},
        0.3: {'label': '30%', 'style': {'color': 'black'}},
        0.4: {'label': '40%', 'style': {'color': 'black'}},
        0.5: {'label': '50%', 'style': {'color': 'black'}},
    }

marks_confidence={
        0: {'label': '0%', 'style': {'color': 'black'}},
        0.1: {'label': '10%', 'style': {'color': 'black'}},
        0.2: {'label': '20%', 'style': {'color': 'black'}},
        0.3: {'label': '30%', 'style': {'color': 'black'}},
        0.4: {'label': '40%', 'style': {'color': 'black'}},
        0.5: {'label': '50%', 'style': {'color': 'black'}},
        0.6: {'label': '60%', 'style': {'color': 'black'}},
        0.7: {'label': '70%', 'style': {'color': 'black'}},
        0.8: {'label': '80%', 'style': {'color': 'black'}},
        0.9: {'label': '90%', 'style': {'color': 'black'}},
        1: {'label': '100%', 'style': {'color': 'black'}},
    }

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
    dbc.DropdownMenuItem("Percentiles", href="/sample_size_bootstrap"),
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

elements = {
    'navbar': navbar,
    # 'sidebar': sidebar,
    'footer': html.Footer(html.P('Copyright 2022, Poznan University of Technology.', className='footer-text')),
    '/ci_holdout_wilson': create_estimation_form("ci", "Holdout Wilson", "holdout_wilson", texts.wilson_text, 100),
    '/ci_holdout_clopper_pearson': create_estimation_form("ci", "Holdout Clopper-Pearson", "holdout_clopper_pearson", texts.clopper_pearson_text, 100),
    '/ci_holdout_langford': create_estimation_form("ci", "Holdout Langford", "holdout_langford", texts.loose_langford_text, 100),
    '/ci_holdout_z_test': create_estimation_form("ci", "Holdout Z-test", "holdout_z_test", texts.z_test_text, 50),
    '/ci_holdout_t_test': create_estimation_form("ci", "Holdout t-test", "holdout_t_test", texts.t_test_text, 25),
    '/ci_progressive': create_estimation_form("ci", "Progressive validation", "progressive", texts.progressive_validation_text, 300),
    '/ci_cv': create_estimation_form("ci", "Cross-validation", "cv", texts.cross_validation_text, 500, n_splits=10),
    '/ci_bootstrap': create_estimation_form("ci", "Bootstrapping", "bootstrap", texts.bootstrap_text, 20, accuracy='0.48816081929448714,0.5114709379333421,0.48965710829479676,0.4974254738927312,0.482690776015456,0.48998736540599175,0.4993842963069065,0.4961912108773732,0.508291825511268,0.4877569233805326,0.48118148168598296,0.4996073070469448,0.52654630031446054,0.5022854894045708,0.49882020732992565,0.52362079495748944,0.5065141753519736,0.49240679510693,0.4941949423340501,0.4987517007791748,0.50361147539058706,0.5155906551034035,0.5030881438235992,0.4936394118427662,0.503656429452781,0.5009448246004594,0.4925057762446265,0.49936815425902495,0.4934037929543002,0.5093328650923615,0.49305816916146895,0.4946163639595628,0.5008023376306553,0.5154222936632961,0.5063290402049816,0.5014251782692496,0.5137857859269866,0.512492371738837,0.4936233661933695,0.5015461644572862,0.4981650467132479,0.4863393898242631,0.4893700517753274,0.5134078859448949,0.49381009308535916,0.5110882324683109,0.510843922475742,0.49724939225615906,0.50198142644277645,0.4929213417184266'),

    '/sample_size_langford': create_estimation_form("sample_size", "Holdout Langford", "holdout_langford", "TODO"),
    '/sample_size_z_test': create_estimation_form("sample_size", "Holdout Z-test", "holdout_z_test", "TODO"),
    '/sample_size_cv': create_estimation_form("sample_size", "Cross-validation", "cv", "TODO", n_splits=10),
    '/sample_size_bootstrap': create_estimation_form("sample_size", "Bootstrapping", "bootstrap", "TODO"),
    '/sample_size_progressive': create_estimation_form("sample_size", "Progressive validation", "progressive", "TODO"),

    '/confidence_level_langford': create_estimation_form("confidence_level", "Holdout Langford", "holdout_langford", "TODO", 100),
    '/confidence_level_z_test': create_estimation_form("confidence_level", "Holdout Z-test", "holdout_z_test", "TODO", 50),
    '/confidence_level_t_test': create_estimation_form("confidence_level", "Holdout t-test", "holdout_t_test", "TODO", 25),
    '/confidence_level_cv': create_estimation_form("confidence_level", "Cross-validation", "cv", "TODO", 500, n_splits=10),
    '/confidence_level_bootstrap': create_estimation_form("confidence_level", "Bootstrapping", "bootstrap", 20, "TODO"),
    '/confidence_level_progressive': create_estimation_form("confidence_level", "Progressive validation", 500, "progressive", "TODO"),
}