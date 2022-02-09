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
                dbc.DropdownMenuItem("Z-test", href="/z_test"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Methods",
        ),
        dbc.NavItem(dbc.NavLink('About', href='/about'))
    ],
    brand="Prediction Confidence Planner",
    brand_href="#",
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
                html.P(texts.z_test_text),
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

##########  ##########
##########  ##########

##########  ##########
##########  ##########


elements = {
    'navbar': navbar,
    '/home': HOME,
    '/about': ABOUT,
    '/z_test': Z_TEST,
}