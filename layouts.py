import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

########## SIDEBAR ##########
SIDEBAR_ICON = '/assets/sidebar_icon32.png'

sidebar_button = dbc.Button(className='sidebar_button', children=[html.Img(src=SIDEBAR_ICON)], id='sidebar_button',
                            outline=True, color='Secondary')


sidebar = html.Div(className='sidebar_on', children=[
    dbc.Nav(children=[
        dbc.NavLink('Home', href='/', active='exact', className='nav_entry'),
        dbc.NavLink('Z test', href='/z_test',
                    active='exact', className='nav_entry'),
        dbc.NavLink('Reverse z test', href='/reverse_z_test',
                    active='exact', className='nav_entry'),
        dbc.NavLink('T test', href='/t_test',
                    active='exact', className='nav_entry'),
        dbc.NavLink('Loose langford', href='/langford_test',
                    active='exact', className='nav_entry'),
        dbc.NavLink('Reverse loose langford',
                    href='/reverse_langford_test', active='exact', className='nav_entry'),  # TODO
        dbc.NavLink('Clopper pearson', href='/clopper_test',
                    active='exact', className='nav_entry'),
        dbc.NavLink('Wilson', href='/wilson_test',
                    active='exact', className='nav_entry'),
        dbc.NavLink('Bootstrap', href='/bootstrap_test',
                    active='exact', className='nav_entry'),  # TODO
        dbc.NavLink('Standard Error', href='/standard_error_test',
                    active='exact', className='nav_entry'),  # TODO

    ],
        vertical=True,
        pills=True,
        id='sidebar-content',
    ),
],
    id='sidebar',
)
########## SIDEBAR ##########

########## Dropdown for Navbar ###############
# dropdown = html.Div(
#     [
#         dbc.DropdownMenu(
#             [
#                 dbc.DropdownMenuItem(
#                     "Z test", href='z_test'
#                 ),
#                 dbc.DropdownMenuItem(
#                     "Reverse z test", href="reverse_z_test"
#                 ),
#                 dbc.DropdownMenuItem(
#                     "T test", href="t_test"
#                 ),
#                 dbc.DropdownMenuItem(
#                     "Loose langford", href="langford_test"
#                 ),
#                 dbc.DropdownMenuItem(
#                     "Clopper pearson", href="clopper_test"
#                 ),
#                 dbc.DropdownMenuItem(
#                     "Wilson", href="wilson_test"
#                 ),
#             ],
#             label="Methods",
#         ),
#     ]
# )
########## Dropdown for Navbar ###############

########## NAVBAR ##########
navbar = dbc.Navbar(
    id='navbar',
    className='navbar',
    children=[
        sidebar_button,
        dbc.NavbarBrand(
            "Prediction Confidence Planner"),

    ],
    color='#082433',
    dark=True,
)
########## NAVBAR ##########


########## MAIN PAGE ##########
MAIN = html.Div(children=[
    dbc.Row(children=[
        dbc.Col(html.H2("How to use the app"))
    ]),
    dbc.Row(children=[
        dbc.Col(
            html.Div('Here will be the instruction and short description of the app'))
    ]),
    dbc.Row(children=[
        dbc.Col(html.Div('Here to put tree plot about where to use which option'))
    ])
], id='main')
########## MAIN PAGE ##########


########## Z TEST PAGE ##########
z_test_explanation = '''
This test assumes that data is normally distributed and works well for bigger number of samples (>30).
Function takes number of samples (Sample size), mean value (Sample mean),
standard deviation (Sample standard deviation) and confidence (Sample confidence interval).
Returns lower and upper bounds for the confidence interval.
'''

Z_TEST = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("Z TEST"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(z_test_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample size", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_sample",
                        type='number',
                        placeholder='Sample size',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample standard deviation", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_std_dev",
                        type='number',
                        placeholder='Sample standard deviation',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample confidence interval", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_confidence",
                        type='number',
                        placeholder='Sample confidence interfal',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='z_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="z_test_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('z_test result', id='z_test_result')
            ], className='right_pane_content')
        ], id="z_test_right_pane", className='right_pane')),
    ])
])
########## Z TEST PAGE ##########


########## REVERSE Z TEST PAGE ##########
z_test_reverse_explanation = '''
Function takes mean of data (Sample mean), standard deviation of data (Sample standard deviation),
difference from mean to lower/upper bound (Sample difference between upper and lower bound)
and confidence (Sample confidence interval).
Returns rounded number of samples which should be taken to obtain a given confidence interval.
'''

Z_TEST_REVERSE = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("REVERSE Z TEST"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(z_test_reverse_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_reverse_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample standard deviation", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_reverse_std_dev",
                        type='number',
                        placeholder='Sample standard deviation',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample difference between upper and lower bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_reverse_diff",
                        type='number',
                        placeholder='Difference mean - upper/lower bound',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample confidence interval", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_reverse_confidence",
                        type='number',
                        placeholder='Sample confidence interval',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='t_test_reverse_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="z_test_reverse_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('z_test_reverse result', id='z_test_reverse_result')
            ], className='right_pane_content')
        ], id="z_test_reverse_right_pane", className='right_pane')),
    ])
])
########## REVERSE Z TEST PAGE ##########

########## Z TEST WITH PRECISION ##########

########## Z TEST WITH PRECISION ##########

########## REVERSE Z TEST WITH PRECISION ##########

########## REVERSE Z TEST WITH PRECISION ##########


########## T TEST ##########
t_test_explanation = '''
This test works for smaller number of samples (<30), uses t-distribution instead the normal one.
Function takes number of samples (n), mean value (mean), standard deviation and confidence (conf).
Returns lower and upper bounds for the confidence interval.
'''

T_TEST = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("T TEST"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(t_test_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample size", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="t_test_sample",
                        type='number',
                        placeholder='Sample size',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="t_test_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample standard deviation", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="t_test_std_dev",
                        type='number',
                        placeholder='Sample standard deviation',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="t_test_confidence",
                        type='number',
                        placeholder='Sample confidence interval',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate...", outline=False,
                                               id='t_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="t_test_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('t_test result', id='t_test_result')
            ], className='right_pane_content')
        ], id="t_test_right_pane", className='right_pane')),
    ])
])
########## T TEST ##########


########## LANGFORD LOOSE TEST ##########
loose_test_explanation = '''
Function takes mean of data (mean), difference from mean to lower/upper bound which is upper_bound-mean
or mean-lower_bound (diff) and confidence (conf).
Returns rounded number of samples which should be taken to obtain a given confidence interval.
'''
LOOSE_TEST = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("LANGFORD LOOSE TEST"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(loose_test_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample size", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_test_sample",
                        type='number',
                        placeholder='Sample size',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_test_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_test_confidence",
                        type='number',
                        placeholder='Sample confidence interval',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='loose_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="loose_test_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('z_test result', id='loose_test_result')
            ], className='right_pane_content')
        ], id="loose_test_right_pane", className='right_pane')),
    ])
])
########## LANGFORD LOOSE TEST ##########


########## REVERSE LANGFORD LOOSE TEST ##########
loose_test_reverse_explanation = '''
Function takes mean of data (mean), difference from mean to lower/upper bound which is upper_bound-mean
or mean-lower_bound (diff) and confidence (conf).
Returns rounded number of samples which should be taken to obtain a given confidence interval.
'''

LOOSE_TEST_REVERSE = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("REVERSE LOOSE LANGFORD TEST"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(loose_test_reverse_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_test_reverse_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample difference between upper and lower bound", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_test_reverse_diff",
                        type='number',
                        placeholder='Difference mean - upper/lower bound',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_test_reverse_confidence",
                        type='number',
                        placeholder='Sample confidence interval',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='loose_test_reverse_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="loose_test_reverse_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('loose_test_reverse result',
                         id='loose_test_reverse_result')
            ], className='right_pane_content')
        ], id="loose_test_reverse_right_pane", className='right_pane')),
    ])
])
########## REVERSE LANGFORD LOOSE TEST ##########


########## CLOPPER PEARSOON TEST ##########
clopper_test_explanation = '''
Function takes number of samples (n), mean value (mean) and confidence (conf).
Returns lower and upper bounds for the confidence interval.
'''

CLOPPER_TEST = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("CLOPPER PEARSOON TEST"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(clopper_test_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample size", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="clopper_test_sample",
                        type='number',
                        placeholder='Sample size',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="clopper_test_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="clopper_test_confidence",
                        type='number',
                        placeholder='Sample confidence interval',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='clopper_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="clopper_test_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('clopper_test result', id='clopper_test_result')
            ], className='right_pane_content')
        ], id="clopper_test_right_pane", className='right_pane')),
    ])
])
########## CLOPPER PEARSOON TEST  ##########


########## WILSON SCORE INTERVAL  ##########
wilson_test_explanation = '''
Function takes number of samples (n), mean value (mean) and confidence (conf).
Returns lower and upper bounds for the confidence interval.
'''

WILSON_TEST = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("WILSON SCORE INTERVAL"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(wilson_test_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample size", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="wilson_test_sample",
                        type='number',
                        placeholder='Sample size',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="wilson_test_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="wilson_test_confidence",
                        type='number',
                        placeholder='Sample confidence interval',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='wilson_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="wilson_test_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('wilson_test result', id='wilson_test_result')
            ], className='right_pane_content')
        ], id="wilson_test_right_pane", className='right_pane')),
    ])
])
########## WILSON SCORE INTERVAL  ##########


########## Percentile Bootstrap Method ##########
bootstrap_test_explanation = '''
Function takes list of resamples means obtained from bootstrap (Sample means CSV format) and confidence (Sample confidence interval).
Returns lower and upper bounds for the confidence interval.
'''

BOOTSTRAP_TEST = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("PERCENTILE BOOTSTRAP METHOD"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(bootstrap_test_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample means CSV format", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="bootstrap_test_means",
                        type='text',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="bootstrap_test_confidence",
                        type='number',
                        placeholder='Sample confidence interval',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='bootstrap_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="bootstrap_test_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('bootstrap_test result', id='bootstrap_test_result')
            ], className='right_pane_content')
        ], id="bootstrap_test_right_pane", className='right_pane')),
    ])
])

########## Percentile Bootstrap Method ##########


########## Standard error method ##########
standard_test_explanation = '''
Function takes mean of the data (mean), list of resamples means obtained from bootstrap (means) and confidence (conf).
Returns lower and upper bounds for the confidence interval.
'''

STANDARD_TEST = html.Div(children=[
    dbc.Row(dbc.Col(html.H2("STANDARD ERROR METHOD"))),
    dbc.Row(children=[
        # Left pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.P(standard_test_explanation),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="standard_test_mean",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample means", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="standard_test_means",
                        type='text',
                        placeholder='Sample means',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="standard_test_confidence",
                        type='number',
                        placeholder='Sample mean',
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='standard_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')

        ], id="standard_test_left_pane", className='left_pane')),
        # Right pane
        dbc.Col(html.Div(children=[
            html.Div(children=[
                html.Div('standard_test result', id='standard_test_result')
            ], className='right_pane_content')
        ], id="standard_test_right_pane", className='right_pane')),
    ])
])
########## Standard error method ##########


elements = {
    '/main': MAIN,
    'navbar': navbar,
    'sidebar': sidebar,
    '/z_test': Z_TEST,
    '/reverse_z_test': Z_TEST_REVERSE,
    '/t_test': T_TEST,
    '/langford_test': LOOSE_TEST,
    '/reverse_langford_test': LOOSE_TEST_REVERSE,
    '/clopper_test': CLOPPER_TEST,
    '/wilson_test': WILSON_TEST,
    '/bootstrap_test': BOOTSTRAP_TEST,
    '/standard_error_test': STANDARD_TEST
}

# TEMPLATE = html.Div(children=[
#     dbc.Row(dbc.Col(html.H2("TEST"))),
#     dbc.Row(children=[
#         # Left pane
#         dbc.Col(html.Div(children=[
#             html.Div(children=[
#                 html.P(z_test_explanation),
#                 html.Div(children=[
#                     dbc.Row(dbc.Col(html.H4("Sample size", style={'text-align': 'center'}), width={
#                         "size": 12, "offset": 0})),
#                     dbc.Row(dbc.Col(, width={
#                         "size": 6, "offset": 3})),
#                     dbc.Row(dbc.Col(html.H4("Sample mean", style={'text-align': 'center'}), width={
#                         "size": 12, "offset": 0})),
#                     dbc.Row(dbc.Col(, width={
#                         "size": 6, "offset": 3})),
#                     dbc.Row(dbc.Col(html.H4("Sample standard deviation", style={'text-align': 'center'}), width={
#                         "size": 12, "offset": 0})),
#                     dbc.Row(dbc.Col(, width={
#                         "size": 6, "offset": 3})),
#                     dbc.Row(dbc.Col(html.H4("Sample Confidence interval", style={'text-align': 'center'}), width={
#                         "size": 12, "offset": 0})),
#                     dbc.Row(dbc.Col(, width={
#                         "size": 6, "offset": 3})),
#                     dbc.Row(dbc.Col(dbc.Button("Calculate...", outline=False,
#                                                id='t_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
#                 ])
#             ], className='left_pane_content')
#
#         ], id="z_test_left_pane", className='left_pane')),
#         # Right pane
#         dbc.Col(html.Div(children=[
#             html.Div(children=[
#                 html.Div('z_test result', id='z_test_result')
#             ], className='right_pane_content')
#         ], id="z_test_right_pane", className='right_pane')),
#     ])
# ])
