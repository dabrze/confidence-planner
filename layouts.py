from click import style
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import components.texts as texts
from util import create_confidence_interval_view

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


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Holdout", header=True),
                dbc.DropdownMenuItem("Wilson's approximation", href="/ci_holdout_wilson"),
                dbc.DropdownMenuItem("Clopper-Pearson approximation", href="/ci_holdout_clopper_pearson"),
                dbc.DropdownMenuItem("Langford's approximation", href="/ci_holdout_langford"),
                dbc.DropdownMenuItem("Z-test", href="/ci_holdout_z_test"),
                dbc.DropdownMenuItem("t-test", href="/ci_holdout_t_test"),
                dbc.DropdownMenuItem("Cross-validation", header=True),
                dbc.DropdownMenuItem("Blum's approximation", href="/ci_cv"),
                dbc.DropdownMenuItem("Bootstrapping", header=True),
                dbc.DropdownMenuItem("Percentile approximation", href="/ci_bootstrap"),
                dbc.DropdownMenuItem("Progressive validation", header=True),
                dbc.DropdownMenuItem("Langford's approximation", href="/ci_progressive"),
            ],
            nav=True,
            in_navbar=True,
            direction='down',
            label="Estimate confidence interval",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Holdout", header=True),
                dbc.DropdownMenuItem("Langford's approximation", href="/loose_langford_reverse_samples"),
                dbc.DropdownMenuItem("Z-test", href="/z_test_reverse_samples"),
                dbc.DropdownMenuItem("Cross-validation", header=True),
                dbc.DropdownMenuItem("Blum's approximation", href="/cross_validation_reverse_samples"),
                dbc.DropdownMenuItem("Bootstrapping", header=True),
                dbc.DropdownMenuItem("Percentile approximation", href="/percentile_reverse_samples"),
                dbc.DropdownMenuItem("Progressive validation", header=True),
                dbc.DropdownMenuItem("Langford's approximation", href="/progressive_validation_reverse_samples"),
            ],
            nav=True,
            in_navbar=True,
            direction='down',
            label="Estimate sample size",
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Holdout", header=True),
                dbc.DropdownMenuItem("Langford's approximation", href="/loose_langford_reverse_confidence"),
                dbc.DropdownMenuItem("Z-test", href="/z_test_reverse_confidence"),
                dbc.DropdownMenuItem("t-test", href="/t_test_reverse_confidence"),
                dbc.DropdownMenuItem("Cross-validation", header=True),
                dbc.DropdownMenuItem("Blum's approximation", href="/cross_validation_reverse_confidence"),
                dbc.DropdownMenuItem("Bootstrapping", header=True),
                dbc.DropdownMenuItem("Percentile approximation", href="/percentile_reverse_confidence"),
                dbc.DropdownMenuItem("Progressive validation", header=True),
                dbc.DropdownMenuItem("Langford's approximation", href="/progressive_validation_reverse_confidence"),
            ],
            nav=True,
            in_navbar=True,
            direction='down',
            label="Estimate confidence level",
        ),
        dbc.NavItem(dbc.NavLink('About', href='/about'))
    ],
    brand="Prediction Confidence Planner",
    brand_href="/home",
    color="#003f9a",
    dark=True,
)

########## Navbar ##########

########## Footer ##########

footer = html.Footer(
    children=[
        html.Div(children=[
                html.A(html.P('2022 Poznan University of Technology.', className=''), href='https://www.put.poznan.pl/en?q=')
            ]
        )
    ]
)

########## Footer ##########


# Webpages:


########## HOME PAGE ##########

HOME = html.Div(children=[
    dcc.Markdown(texts.home_text),
    html.Img(src="map.svg", alt="Description of 4 options to choose from (Holdout, Bootstrap, Cross-Validation, Progressive-Validation)", width="75%", height="75%"), # width="500", height="600"
    # html.Img(src=app.get_asset_url("Main_tree.png"),
    dcc.Markdown(texts.home_text_2),
    footer
], id='home')

########## HOME PAGE ##########

########## ABOUT PAGE ##########

ABOUT = html.Div(children=[
    dcc.Markdown(texts.about_text),
     html.Footer(
    children=[
        html.Div(children=[
                html.A(html.P('2022 Poznan University of Technology.', className=''), href='https://www.put.poznan.pl/en?q=')
            ]
        )
    ]
)])

########## ABOUT PAGE ##########


# Test webpages:

# Z TESTS:


########## Z TEST REVERSE PAGE (# samples) ##########
Z_TEST_REV_SAMPLES = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE Z TEST (Samples)"),
            html.Div(children=[
                # Test description:
                html.P(texts.z_test_text_reverse_samples),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Difference from accuracy to lower/upper bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0.005, max=0.5, step=0.005,
                            value=0.05,
                            marks=marks_interval,
                            included=False,
                            id="z_test_rev_samples_diff",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    #     dcc.Input(
                    #     id="z_test_rev_samples_diff",
                    #     type='number',
                    #     placeholder='Number of samples',
                    #     value=11,
                    #     style={'width': '100%'}
                    # ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(

                        dcc.Slider(min=0.01, max=0.99, step=0.01, 
                            value=0.90,
                            marks=marks_confidence,
                            included=False,
                            id="z_test_rev_samples_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    #     dcc.Input(
                    #     id="z_test_rev_samples_confidence",
                    #     type='number',
                    #     placeholder='Confidence',
                    #     value=0.80,
                    #     style={'width': '100%'}
                    # ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='z_test_rev_samples_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="z_test_rev_samples_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE Z TEST (Samples) RESULT"),
            html.Div(children=[
                html.Div('z_test_rev_samples_result', id='z_test_rev_samples_result')
            ], className='right_pane_content')
        ], id="z_test_rev_samples_right_pane", className='right_pane')),
    ])
])
########## Z TEST REVERSE PAGE (# samples) ##########

########## Z TEST REVERSE PAGE (confidence) ##########
Z_TEST_REV_CONFIDENCE = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE Z TEST (Confidence)"),
            html.Div(children=[
                # Test description:
                html.P(texts.z_test_text_reverse_confidence),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_rev_confidence_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=180,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Difference from accuracy to lower/upper bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0.005, max=0.5, step=0.005,
                            value=0.05,
                            marks=marks_interval,
                            included=False,
                            id="z_test_rev_confidence_diff",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    #     dcc.Input(
                    #     id="z_test_rev_confidence_diff",
                    #     type='number',
                    #     placeholder='Confidence',
                    #     value=5,
                    #     style={'width': '100%'}
                    # ), 
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='z_test_rev_confidence_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="z_test_rev_confidence_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE Z TEST (Confidence) RESULT"),
            html.Div(children=[
                html.Div('z_test_rev_confidence_result', id='z_test_rev_confidence_result')
            ], className='right_pane_content')
        ], id="z_test_rev_confidence_right_pane", className='right_pane')),
    ])
])
########## Z TEST REVERSE PAGE (confidence) ##########






# T TESTS:

########## T TEST REVERSE PAGE (confidence) ##########

T_TEST_REV_CONFIDENCE = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE T TEST (Confidence)"),
            html.Div(children=[
                # Test description:
                html.P(texts.t_test_text_reverse),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="t_test_rev_confidence_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=25,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Difference from accuracy to lower/upper bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0.005, max=0.5, step=0.005,
                            value=0.05,
                            marks=marks_interval,
                            included=False,
                            id="t_test_rev_confidence_diff",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='t_test_rev_confidence_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="t_test_rev_confidence_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE T TEST (Confidence) RESULT"),
            html.Div(children=[
                html.Div('t_test_rev_confidence_result', id='t_test_rev_confidence_result')
            ], className='right_pane_content')
        ], id="t_test_rev_confidence_right_pane", className='right_pane')),
    ])
])

########## T TEST REVERSE PAGE (confidence) ##########






# LOOSE LANGFORD TESTS:

########## LOOSE LANGFORD REVERSE PAGE (# samples) ##########
LOOSE_LANGFORD_TEST_REV_SAMPLES = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE LOOSE LANGFORD (Samples)"),
            html.Div(children=[
                # Test description:
                html.P(texts.loose_langford_text_reverse_samples),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Difference from accuracy to lower/upper bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0.005, max=0.5, step=0.005,
                            value=0.05,
                            marks=marks_interval,
                            included=False,
                            id="loose_langford_rev_samples_diff",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(

                        dcc.Slider(min=0.01, max=0.99, step=0.01, 
                            value=0.90,
                            marks=marks_confidence,
                            included=False,
                            id="loose_langford_rev_samples_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='loose_langford_rev_samples_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="loose_langford_rev_samples_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE LOOSE LANGFORD (Samples) RESULT"),
            html.Div(children=[
                html.Div('loose_langford_rev_samples_result', id='loose_langford_rev_samples_result')
            ], className='right_pane_content')
        ], id="loose_langford_rev_samples_right_pane", className='right_pane')),
    ])
])
########## LOOSE LANGFORD REVERSE PAGE (# samples) ##########

########## LOOSE LANGFORD REVERSE PAGE (confidence) ##########
LOOSE_LANGFORD_TEST_REV_CONFIDENCE = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE LOOSE LANGFORD (Confidence)"),
            html.Div(children=[
                # Test description:
                html.P(texts.loose_langford_text_reverse_confidence),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_langford_rev_confidence_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=180,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Difference from accuracy to lower/upper bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0.005, max=0.5, step=0.005,
                            value=0.05,
                            marks=marks_interval,
                            included=False,
                            id="loose_langford_rev_confidence_diff",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='loose_langford_rev_confidence_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="loose_langford_rev_confidence_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE LOOSE LANGFORD (Confidence) RESULT"),
            html.Div(children=[
                html.Div('loose_langford_rev_confidence_result', id='loose_langford_rev_confidence_result')
            ], className='right_pane_content')
        ], id="loose_langford_rev_confidence_right_pane", className='right_pane')),
    ])
])
########## LOOSE LANGFORD REVERSE PAGE (confidence) ##########


########## PERCENTILE BOOTSTRAP PEARSON PAGE ##########
PERCENTILE_BOOTSTRAP_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("PERCENTILE BOOTSTRAP TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.bootstrap_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("List of resample accuracies", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(children=[
                        dbc.Col(dcc.Input(
                            id="bootstrap_samples",
                            type='text',
                            placeholder='Number of samples',
                            value='0.48816081929448714,0.5114709379333421,0.48965710829479676,0.4974254738927312,0.482690776015456,0.48998736540599175,0.4993842963069065,0.4961912108773732,0.508291825511268,0.4877569233805326,0.48118148168598296,0.4996073070469448,0.52654630031446054,0.5022854894045708,0.49882020732992565,0.52362079495748944,0.5065141753519736,0.49240679510693,0.4941949423340501,0.4987517007791748,0.50361147539058706,0.5155906551034035,0.5030881438235992,0.4936394118427662,0.503656429452781,0.5009448246004594,0.4925057762446265,0.49936815425902495,0.4934037929543002,0.5093328650923615,0.49305816916146895,0.4946163639595628,0.5008023376306553,0.5154222936632961,0.5063290402049816,0.5014251782692496,0.5137857859269866,0.512492371738837,0.4936233661933695,0.5015461644572862,0.4981650467132479,0.4863393898242631,0.4893700517753274,0.5134078859448949,0.49381009308535916,0.5110882324683109,0.510843922475742,0.49724939225615906,0.50198142644277645,0.4929213417184266',
                            style={'width': '100%', 'text-align':'center'}
                        ), width={
                            "size": 6, "offset": 3}),]),
                        # dbc.Col(dcc.Upload(html.Div('Upload File'), id='upload_data'))]),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0.01, max=0.99, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="bootstrap_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='bootstrap_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="bootstrap_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("PERCENTILE BOOTSTRAP RESULTS"),
            html.Div(children=[
                dcc.Graph(
                    id='bootstrap_result_graph',
                    config= {'displayModeBar': False},
                ),
                html.Div('bootstrap_result', id='bootstrap_result')
            ], className='right_pane_content')
        ], id="bootstrap_right_pane", className='right_pane')),
    ])
])
########## CLOPPER PEARSON PAGE ##########


elements = {
    'navbar': navbar,
    # 'sidebar': sidebar,
    'footer': footer,
    '/home': HOME,
    '/about': ABOUT,
    '/ci_holdout_wilson': create_confidence_interval_view("Holdout Wilson approximation", "holdout_wilson", texts.wilson_text, 100),
    '/ci_holdout_clopper_pearson': create_confidence_interval_view("Holdout Clopper-Pearson approximation", "holdout_clopper_pearson", texts.clopper_pearson_text, 100),
    '/ci_holdout_langford': create_confidence_interval_view("Holdout Langford approximation", "holdout_langford", texts.loose_langford_text, 100),
    '/ci_holdout_z_test': create_confidence_interval_view("Holdout Z-test", "holdout_z_test", texts.z_test_text, 50),
    '/ci_holdout_t_test': create_confidence_interval_view("Holdout t-test", "holdout_t_test", texts.t_test_text, 25),
    '/ci_progressive': create_confidence_interval_view("Progressive validation", "progressive", texts.progressive_validation_text, 300),
    '/ci_cv': create_confidence_interval_view("Cross-validation", "cv", texts.cross_validation_text, 500, n_splits=10),
    '/ci_bootstrap': PERCENTILE_BOOTSTRAP_TEST,

    '/z_test_reverse_samples': Z_TEST_REV_SAMPLES,
    '/z_test_reverse_confidence': Z_TEST_REV_CONFIDENCE,

    '/t_test_reverse_confidence': T_TEST_REV_CONFIDENCE,

    '/loose_langford_reverse_samples': LOOSE_LANGFORD_TEST_REV_SAMPLES,
    '/loose_langford_reverse_confidence': LOOSE_LANGFORD_TEST_REV_CONFIDENCE,



}