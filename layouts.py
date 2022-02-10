import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import components.texts as texts


# Webpage elements:


########## Navbar ##########

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Methods", header=True),
                dbc.DropdownMenu(children=[
                    dbc.DropdownMenuItem("Z-test", href="/z_test"),
                    dbc.DropdownMenuItem("Reverse Z-test - samples", href="/z_test_reverse_samples"),
                    dbc.DropdownMenuItem("Reverse Z-test - confidence", href="/z_test_reverse_confidence"),
                    ],
                    color='white',
                    direction="right",
                    label='Z-test'),
                    
                dbc.DropdownMenuItem("Page 3", href="/home"),
            ],
            nav=True,
            in_navbar=True,
            direction='down',
            label="Methods",
        ),
        dbc.NavItem(dbc.NavLink('About', href='/about'))
    ],
    brand="Prediction Confidence Planner",
    brand_href="/home",
    color="primary",
    dark=True,
)

########## Navbar ##########

##########  ##########
##########  ##########


# Webpages:


########## HOME PAGE ##########

HOME = html.Div(children=[
    dcc.Markdown(texts.home_text),
    html.Img(src="assets/Main_tree.png", alt="Description of 4 options to choose from (Holdout, Bootstrap, Cross-Validation, Progressive-Validation)", width="75%", height="75%"), # width="500", height="600"
    dcc.Markdown(texts.home_text_2),
], id='home')

########## HOME PAGE ##########

########## ABOUT PAGE ##########

ABOUT = html.Div(children=[
    dcc.Markdown(texts.about_text)])

########## ABOUT PAGE ##########


# Test webpages:

# Z TESTS:
########## Z TEST PAGE ##########
Z_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("Z TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.z_test_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_sample",
                        type='number',
                        placeholder='Number of samples',
                        value=100,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_accuracy",
                        type='number',
                        placeholder='Obtained Accuracy',
                        value=80,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_confidence",
                        type='number',
                        placeholder='Confidence',
                        value=0.80,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='z_test_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')
        ], id="z_test_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("Z TEST Results"),
            html.Div(children=[
                dcc.Graph(
                    id='z_test_result_graph',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    }
                ),
                html.Div('z_test result', id='z_test_result')
            ], className='right_pane_content')
        ], id="z_test_right_pane", className='right_pane')),
    ])
])
########## Z TEST PAGE ##########

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
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_rev_samples_diff",
                        type='number',
                        placeholder='Number of samples',
                        value=11,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_rev_samples_confidence",
                        type='number',
                        placeholder='Confidence',
                        value=0.80,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='z_test_rev_samples_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')
        ], id="z_test_rev_samples_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE Z TEST (Samples) Results"),
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
                        placeholder='Number of samples',
                        value=180,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Difference from accuracy to lower/upper bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="z_test_rev_confidence_diff",
                        type='number',
                        placeholder='Confidence',
                        value=5,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(dbc.Button("Calculate", outline=False,
                                               id='z_test_rev_confidence_button', n_clicks=0), width={'size': 6, 'offset': 3}), justify='center')
                ])
            ], className='left_pane_content')
        ], id="z_test_rev_confidence_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("REVERSE Z TEST (Confidence) Results"),
            html.Div(children=[
                html.Div('z_test_rev_confidence_result', id='z_test_rev_confidence_result')
            ], className='right_pane_content')
        ], id="z_test_rev_confidence_right_pane", className='right_pane')),
    ])
])
########## Z TEST REVERSE PAGE (confidence) ##########

# T TESTS:
##########  ##########
##########  ##########

##########  ##########
##########  ##########

##########  ##########
##########  ##########

##########  ##########
##########  ##########

##########  ##########
##########  ##########

##########  ##########
##########  ##########


elements = {
    'navbar': navbar,
    '/home': HOME,
    '/about': ABOUT,
    '/z_test': Z_TEST,
    '/z_test_reverse_samples': Z_TEST_REV_SAMPLES,
    '/z_test_reverse_confidence': Z_TEST_REV_CONFIDENCE,
}