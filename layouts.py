from click import style
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import components.texts as texts
from app import app

marks_accuracy={
        0: {'label': '0%', 'style': {'color': 'black'}},
        10: {'label': '10%', 'style': {'color': 'black'}},
        20: {'label': '20%', 'style': {'color': 'black'}},
        30: {'label': '30%', 'style': {'color': 'black'}},
        40: {'label': '40%', 'style': {'color': 'black'}},
        50: {'label': '50%', 'style': {'color': 'black'}},
        60: {'label': '60%', 'style': {'color': 'black'}},
        70: {'label': '70%', 'style': {'color': 'black'}},
        80: {'label': '80%', 'style': {'color': 'black'}},
        90: {'label': '90%', 'style': {'color': 'black'}},
        100: {'label': '100%', 'style': {'color': 'black'}}
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

# Webpage elements:

########## SIDEBAR -> deprecated ##########
# SIDEBAR_ICON = '/assets/sidebar_icon32.png'

# sidebar_button = dbc.Button(className='sidebar_button', children=[html.Img(src=SIDEBAR_ICON)], id='sidebar_button',
#                             outline=True, color='Secondary')


# sidebar = html.Div(className='sidebar_on', children=[
#     dbc.Nav(children=[
#         dbc.NavLink('Home', href='/', active='exact', className='nav_entry'),
#         dbc.NavLink('Z test', href='/z_test',
#                     active='exact', className='nav_entry'),
#         dbc.NavLink('Reverse z test', href='/reverse_z_test',
#                     active='exact', className='nav_entry'),
#         dbc.NavLink('T test', href='/t_test',
#                     active='exact', className='nav_entry'),
#         dbc.NavLink('Loose langford', href='/langford_test',
#                     active='exact', className='nav_entry'),
#         dbc.NavLink('Reverse loose langford',
#                     href='/reverse_langford_test', active='exact', className='nav_entry'), 
#         dbc.NavLink('Clopper pearson', href='/clopper_test',
#                     active='exact', className='nav_entry'),
#         dbc.NavLink('Wilson', href='/wilson_test',
#                     active='exact', className='nav_entry'),
#         dbc.NavLink('Bootstrap', href='/bootstrap_test',
#                     active='exact', className='nav_entry'),  
#         dbc.NavLink('Standard Error', href='/standard_error_test',
#                     active='exact', className='nav_entry'),  

#     ],
#         vertical=True,
#         pills=True,
#         id='sidebar-content',
#     ),
# ],
#     id='sidebar',
# )
########## SIDEBAR ##########

########## Navbar ##########

# navbar used together with sidebar
# navbar = dbc.Navbar(
#     id='navbar',
#     className='navbar',
#     children=[
#         sidebar_button,
#         dbc.NavbarBrand(
#             "Prediction Confidence Planner"),

#     ],
#     color='#082433',
#     dark=True,
# )

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.DropdownMenu(
            children=[
                # dbc.DropdownMenuItem("Bootstrap", header=True),
                dbc.DropdownMenuItem("Percentile Bootstrap", href="/percentile_bootstrap_method"),
                # dbc.DropdownMenuItem("Cross Validation", header=True),
                dbc.DropdownMenuItem("Cross-Validation", href="/cross_validation"),
                # dbc.DropdownMenuItem("Progressive Validation", header=True),
                dbc.DropdownMenuItem("Progressive-Validation", href="/progressive_validation"),
                dbc.DropdownMenuItem("Clopper-Pearson test", href="/clopper_pearson", toggle=False),
                dbc.DropdownMenuItem("Wilson test", href="/wilson"),
                dbc.DropdownMenuItem("Z-test", header=True),
                dbc.DropdownMenuItem("Z-test", href="/z_test"),
                dbc.DropdownMenuItem("Reverse Z-test - samples", href="/z_test_reverse_samples"),
                dbc.DropdownMenuItem("Reverse Z-test - confidence", href="/z_test_reverse_confidence"),
                # html.Div(dbc.DropdownMenu(children=[
                #     dbc.DropdownMenuItem("Z-test", href="/z_test"),
                #     dbc.DropdownMenuItem("Reverse Z-test - samples", href="/z_test_reverse_samples"),
                #     dbc.DropdownMenuItem("Reverse Z-test - confidence", href="/z_test_reverse_confidence"),
                #     ],
                #     color='white',
                #     direction="left",
                #     label='Z-test'), style={'width': '100px'}),
                dbc.DropdownMenuItem("T-test", header=True),
                dbc.DropdownMenuItem("T-test", href="/t_test"),
                dbc.DropdownMenuItem("Reverse T-test - confidence", href="/t_test_reverse_confidence"),
                # dbc.DropdownMenu(children=[
                #     dbc.DropdownMenuItem("T-test", href="/t_test"),
                #     dbc.DropdownMenuItem("Reverse T-test - confidence", href="/t_test_reverse_confidence"),
                #     ],
                #     color='white',
                #     direction="left",
                #     label='T-test'),
                dbc.DropdownMenuItem("Loose test set bound (Langford)", header=True),
                dbc.DropdownMenuItem("Loose test set bound (Langford)", href="/loose_langford"),
                dbc.DropdownMenuItem("Reverse Loose-Langford test - samples", href="/loose_langford_reverse_samples"),
                dbc.DropdownMenuItem("Reverse Loose-Langford test - confidence", href="/loose_langford_reverse_confidence"),
                # dbc.DropdownMenu(children=[
                #     dbc.DropdownMenuItem("Loose-Langford test", href="/loose_langford"),
                #     dbc.DropdownMenuItem("Reverse Loose-Langford test - samples", href="/loose_langford_reverse_samples"),
                #     dbc.DropdownMenuItem("Reverse Loose-Langford test - confidence", href="/loose_langford_reverse_confidence"),
                #     ],
                #     color='white',
                #     direction="left",
                #     label='Loose-Langford'),
                
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
    color="#003f9a",
    dark=True,
)

########## Navbar ##########

########## Footer ##########

footer = html.Footer(
    children=[
        html.Div(children=[
                html.P('2021 Poznan University of Technology.', className='')
            ]
        )
    ]
)

########## Footer ##########


# Webpages:


########## HOME PAGE ##########

HOME = html.Div(children=[
    dcc.Markdown(texts.home_text),
    html.Img(src=app.get_asset_url("Main_tree.png"), alt="Description of 4 options to choose from (Holdout, Bootstrap, Cross-Validation, Progressive-Validation)", width="75%", height="75%"), # width="500", height="600"
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
                        min=1,
                        placeholder='Number of samples',
                        value=100,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=80,
                            marks=marks_accuracy,
                            included=False,
                            id="z_test_accuracy",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    #     dcc.Input(
                    #     id="z_test_accuracy",
                    #     type='number',
                    #     placeholder='Obtained Accuracy',
                    #     value=80,
                    #     style={'width': '100%'}
                    # ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="z_test_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    #     dcc.Input(
                    #     id="z_test_confidence",
                    #     type='number',
                    #     placeholder='Confidence',
                    #     value=0.80,
                    #     style={'width': '100%'}
                    # ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='z_test_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="z_test_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("Z TEST Results"),
            html.Div(children=[
                dcc.Graph(
                    id='z_test_result_graph',
                    config= {'displayModeBar': False},
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
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0.5, max=100, step=0.5, 
                            value=7,
                            marks=marks_accuracy,
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

                        dcc.Slider(min=0, max=0.99, step=0.01, 
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
                        min=1,
                        placeholder='Number of samples',
                        value=180,
                        style={'width': '100%'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Difference from accuracy to lower/upper bound", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=7,
                            marks=marks_accuracy,
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
            html.H2("REVERSE Z TEST (Confidence) Results"),
            html.Div(children=[
                html.Div('z_test_rev_confidence_result', id='z_test_rev_confidence_result')
            ], className='right_pane_content')
        ], id="z_test_rev_confidence_right_pane", className='right_pane')),
    ])
])
########## Z TEST REVERSE PAGE (confidence) ##########






# T TESTS:
########## T TEST PAGE ##########

T_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("T TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.t_test_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="t_test_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=25,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=70,
                            marks=marks_accuracy,
                            included=False,
                            id="t_test_accuracy",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="t_test_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='t_test_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="t_test_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("T TEST Results"),
            html.Div(children=[
                dcc.Graph(
                    id='t_test_result_graph',
                    config= {'displayModeBar': False},
                ),
                html.Div('t_test result', id='t_test_result')
            ], className='right_pane_content')
        ], id="t_test_right_pane", className='right_pane')),
    ])
])

########## T TEST PAGE ##########

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
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=7,
                            marks=marks_accuracy,
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
            html.H2("REVERSE T TEST (Confidence) Results"),
            html.Div(children=[
                html.Div('t_test_rev_confidence_result', id='t_test_rev_confidence_result')
            ], className='right_pane_content')
        ], id="t_test_rev_confidence_right_pane", className='right_pane')),
    ])
])

########## T TEST REVERSE PAGE (confidence) ##########






# LOOSE LANGFORD TESTS:
########## LOOSE LANGFORD PAGE ##########
LOOSE_LANGFORD_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("LOOSE LANGFORD TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.loose_langford_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="loose_langford_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=100,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=80,
                            marks=marks_accuracy,
                            included=False,
                            id="loose_langford_accuracy",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="loose_langford_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='loose_langford_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="loose_langford_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("LOOSE LANGFORD Results"),
            html.Div(children=[
                dcc.Graph(
                    id='loose_langford_result_graph',
                    config= {'displayModeBar': False},
                ),
                html.Div('loose_langford result', id='loose_langford_result')
            ], className='right_pane_content')
        ], id="loose_langford_right_pane", className='right_pane')),
    ])
])
########## LOOSE LANGFORD PAGE ##########

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
                        
                        dcc.Slider(min=0.5, max=100, step=0.5, 
                            value=7,
                            marks=marks_accuracy,
                            included=False,
                            id="loose_langford_rev_samples_diff",
                            tooltip={"placement": "top", "always_visible": True},
                        ),
                    
                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(

                        dcc.Slider(min=0, max=0.99, step=0.01, 
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
            html.H2("REVERSE LOOSE LANGFORD (Samples) Results"),
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
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=7,
                            marks=marks_accuracy,
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
            html.H2("REVERSE LOOSE LANGFORD (Confidence) Results"),
            html.Div(children=[
                html.Div('loose_langford_rev_confidence_result', id='loose_langford_rev_confidence_result')
            ], className='right_pane_content')
        ], id="loose_langford_rev_confidence_right_pane", className='right_pane')),
    ])
])
########## LOOSE LANGFORD REVERSE PAGE (confidence) ##########






########## CLOPPER PEARSON PAGE ##########
CLOPPER_PEARSON_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("CLOPPER PEARSON TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.clopper_pearson_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="clopper_pearson_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=100,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=80,
                            marks=marks_accuracy,
                            included=False,
                            id="clopper_pearson_accuracy",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="clopper_pearson_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='clopper_pearson_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="clopper_pearson_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("CLOPPER PEARSON Results"),
            html.Div(children=[
                dcc.Graph(
                    id='clopper_pearson_result_graph',
                    config= {'displayModeBar': False},
                ),
                html.Div('clopper_pearson_result', id='clopper_pearson_result')
            ], className='right_pane_content')
        ], id="clopper_pearson_right_pane", className='right_pane')),
    ])
])
########## CLOPPER PEARSON PAGE ##########






########## WILSON PAGE ##########
WILSON_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("WILSON TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.wilson_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="wilson_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=100,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=80,
                            marks=marks_accuracy,
                            included=False,
                            id="wilson_accuracy",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="wilson_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='wilson_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="wilson_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("WILSON Results"),
            html.Div(children=[
                dcc.Graph(
                    id='wilson_result_graph',
                    config= {'displayModeBar': False},
                ),
                html.Div('wilson result', id='wilson_result')
            ], className='right_pane_content')
        ], id="wilson_right_pane", className='right_pane')),
    ])
])
########## WILSON PAGE ##########






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
                            value='50.099273887544065,49.46878483304577,51.50104411779424,50.30309460060942,48.76100352762221,49.32691077846691,48.888452270129854,49.64402669528858,47.75469797205529,46.48782120640318',
                            style={'width': '100%', 'text-align':'center'}
                        ), width={
                            "size": 6, "offset": 3}),]),
                        # dbc.Col(dcc.Upload(html.Div('Upload File'), id='upload_data'))]),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
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
            html.H2("PERCENTILE BOOTSTRAP Results"),
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






########## CROSS VALIDATION PAGE ##########
CROSS_VALIDATION_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("CROSS VALIDATION TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.cross_validation_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="cross_validation_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples',
                        value=100,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),
                    
                    dbc.Row(dbc.Col(html.H4("Number of folds", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="cross_validation_folds",
                        type='number',
                        min=1,
                        placeholder='Number of folds',
                        value=10,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),

                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=80,
                            marks=marks_accuracy,
                            included=False,
                            id="cross_validation_accuracy",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="cross_validation_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='cross_validation_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="cross_validation_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("CROSS VALIDATION Results"),
            html.Div(children=[
                dcc.Graph(
                    id='cross_validation_result_graph',
                    config= {'displayModeBar': False},
                ),
                html.Div('cross_validation result', id='cross_validation_result')
            ], className='right_pane_content')
        ], id="cross_validation_right_pane", className='right_pane')),
    ])
])
########## CROSS VALIDATION PAGE ##########






########## PROGRESSIVE VALIDATION PAGE ##########
PROGRESSIVE_VALIDATION_TEST = html.Div(children=[
    dbc.Row(children=[
        # Left pane (delivering information):
        dbc.Col(html.Div(children=[
            html.H2("PROGRESSIVE VALIDATION TEST"),
            html.Div(children=[
                # Test description:
                html.P(texts.progressive_validation_text),
                html.Div(children=[
                    dbc.Row(dbc.Col(html.H4("Number of samples from a test set", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(dcc.Input(
                        id="progressive_validation_sample",
                        type='number',
                        min=1,
                        placeholder='Number of samples from a test set',
                        value=100,
                        style={'width': '100%', 'text-align':'center'}
                    ), width={
                        "size": 6, "offset": 3})),
                    dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=100, step=0.5, 
                            value=80,
                            marks=marks_accuracy,
                            included=False,
                            id="progressive_validation_accuracy",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                    dbc.Row(dbc.Col(
                        
                        dcc.Slider(min=0, max=1, step=0.01, 
                            value=0.80,
                            marks=marks_confidence,
                            included=False,
                            id="progressive_validation_confidence",
                            tooltip={"placement": "top", "always_visible": True},
                        ),

                    width={
                        "size": 8, "offset": 2})),
                    dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                               id='progressive_validation_button', n_clicks=0), justify='center')
                ])
            ], className='left_pane_content')
        ], id="progressive_validation_left_pane", className='left_pane')),

        # Right pane (results):
        dbc.Col(html.Div(children=[
            html.H2("PROGRESSIVE VALIDATION Results"),
            html.Div(children=[
                dcc.Graph(
                    id='progressive_validation_result_graph',
                    config= {'displayModeBar': False},
                ),
                html.Div('progressive_validation result', id='progressive_validation_result')
            ], className='right_pane_content')
        ], id="progressive_validation_right_pane", className='right_pane')),
    ])
])
########## PROGRESSIVE VALIDATION PAGE ##########

##########  ##########
##########  ##########

##########  ##########
##########  ##########

##########  ##########
##########  ##########


elements = {
    'navbar': navbar,
    # 'sidebar': sidebar,
    'footer': footer,
    '/home': HOME,
    '/about': ABOUT,
    '/z_test': Z_TEST,
    '/z_test_reverse_samples': Z_TEST_REV_SAMPLES,
    '/z_test_reverse_confidence': Z_TEST_REV_CONFIDENCE,
    '/t_test' : T_TEST,
    '/t_test_reverse_confidence': T_TEST_REV_CONFIDENCE,
    '/loose_langford': LOOSE_LANGFORD_TEST,
    '/loose_langford_reverse_samples': LOOSE_LANGFORD_TEST_REV_SAMPLES,
    '/loose_langford_reverse_confidence': LOOSE_LANGFORD_TEST_REV_CONFIDENCE,
    '/clopper_pearson': CLOPPER_PEARSON_TEST,
    '/wilson': WILSON_TEST,
    '/percentile_bootstrap_method': PERCENTILE_BOOTSTRAP_TEST,
    '/cross_validation': CROSS_VALIDATION_TEST,
    '/progressive_validation': PROGRESSIVE_VALIDATION_TEST,

}