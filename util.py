# Graph generation imports
import confidence_planner as cp
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

palette = ["#cc6677", "#f6cf71", "#0f8554", "#1d6996", "#ff9900"]

marks_accuracy={
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
        1.0: {'label': '100%', 'style': {'color': 'black'}}
    }

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

def calculate_multiple_ci(
    sample_size,
    accuracy,
    confidence_level,
    method,
    n_splits=None,
    additional_levels=[0.90, 0.95, 0.99],
):
    levels = [confidence_level]
    levels.extend(additional_levels)

    intervals = []
    for level in levels:
        ci = cp.estimate_confidence_interval(
            sample_size, accuracy, level, method=method, n_splits=n_splits
        )
        intervals.append((level, ci))

    return intervals


def ci_callback(sample_size, accuracy, confidence_level, method, n_splits=None):
    if method == "bootstrap":
        accuracy = [float(accuracy) for accuracy in accuracy.split(",")]

    intervals = calculate_multiple_ci(
        sample_size, accuracy, confidence_level, method=method, n_splits=n_splits
    )
    divs = [
        html.P(f"Using the {method} method to approximate the certainty around the obtained accuracy of {accuracy} on a " \
               f"holdout test set of {sample_size} examples, the confidence intervals are:", style={"margin-bottom": "14px"})
    ]

    for level, interval in intervals:
        div_str = (
            f"{level*100}% CI: {interval[0]:.2f} - {interval[1]:.2f}"
        )
        divs.append(html.Div(div_str))

    plot = plot_confidence_interval(intervals)



    return divs, plot


def sample_size_callback(interval_radius, confidence_level, method, n_splits=None):
    sample_size = cp.estimate_sample_size(
        interval_radius, confidence_level, method=method, n_splits=n_splits
    )
    return html.Div(
        f"The estimated number of samples needed to obtain a {round(confidence_level*100, 0)}% confidence "
        f"interval with a {interval_radius} radius is : {sample_size}"
    )


def confidence_level_callback(
    sample_size, interval_radius, method, n_splits=None, accuracies=None
):
    confidence_level = cp.estimate_confidence_level(
        sample_size,
        interval_radius,
        method=method,
        n_splits=n_splits,
        accuracies=accuracies,
    )
    return html.Div(
        f"The estimated confidence level of an {interval_radius} radius "
        f"interval is : {confidence_level*100:.1f}%"
    )


def create_estimation_form(name, identifier, description, sample_size, accuracy=0.75, confidence_level=0.8,
                           n_splits=None, result_title="Estimated confidence intervals"):
    return dbc.Container(
        dbc.Row(children=[
            create_input_panel(name, identifier, description, sample_size, accuracy, confidence_level, n_splits),
            create_result_panel(identifier, result_title),
        ], id=f"{identifier}")
    )


def create_result_panel(identifier, result_title):
    return dbc.Col(children=[
        html.H2(result_title),
        html.Div('', id=f"{identifier}_result"),
        html.Div(children=[
            dcc.Graph(
                id=f"{identifier}_result_graph",
                config={'displayModeBar': False},
            ),
        ], className='right_pane_content')
    ], id=f"{identifier}_right_pane", className='estimation-panel')


def create_input_panel(name, identifier, description, sample_size, accuracy, confidence_level, n_splits):
    return dbc.Col(children=[
        html.H2(name),
        html.Div(children=[
            # Test description:
            html.P(description),
            html.Div(children=[
                dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                    "size": 12, "offset": 0}),
                        style={'display': 'none' if identifier == 'bootstrap' else 'flex'}),
                dbc.Row(dbc.Col(dcc.Input(
                    id=f"{identifier}_sample",
                    type='number',
                    min=1,
                    placeholder='Number of samples',
                    value=sample_size,
                    style={'width': '100%', 'text-align': 'center'}
                ), width={
                    "size": 12}),
                    style={'display': 'none' if identifier == 'bootstrap' else 'flex'}),

                dbc.Row(dbc.Col(html.H4("Number of folds", style={'text-align': 'center'}),
                                width={"size": 12, "offset": 0}),
                        style={'display': 'none' if n_splits is None else 'flex'}),
                dbc.Row(dbc.Col(dcc.Input(
                    id=f"{identifier}_folds",
                    type='number',
                    min=1,
                    placeholder='Number of folds',
                    value=n_splits,
                    style={'width': '100%', 'text-align': 'center'}
                ), width={
                    "size": 12}),
                    style={'display': 'none' if n_splits is None else 'flex'}),

                dbc.Row(dbc.Col(
                    html.H4("List of bootstrap accuracies" if identifier == 'bootstrap' else "Accuracy",
                            style={'text-align': 'center'}), width={
                        "size": 12, "offset": 0})),
                dbc.Row(dbc.Col(
                    dcc.Input(
                        id=f"{identifier}_accuracy",
                        type='text',
                        placeholder='Comma-separated list of accuracies',
                        value='0.48816081929448714,0.5114709379333421,0.48965710829479676,0.4974254738927312,0.482690776015456,0.48998736540599175,0.4993842963069065,0.4961912108773732,0.508291825511268,0.4877569233805326,0.48118148168598296,0.4996073070469448,0.52654630031446054,0.5022854894045708,0.49882020732992565,0.52362079495748944,0.5065141753519736,0.49240679510693,0.4941949423340501,0.4987517007791748,0.50361147539058706,0.5155906551034035,0.5030881438235992,0.4936394118427662,0.503656429452781,0.5009448246004594,0.4925057762446265,0.49936815425902495,0.4934037929543002,0.5093328650923615,0.49305816916146895,0.4946163639595628,0.5008023376306553,0.5154222936632961,0.5063290402049816,0.5014251782692496,0.5137857859269866,0.512492371738837,0.4936233661933695,0.5015461644572862,0.4981650467132479,0.4863393898242631,0.4893700517753274,0.5134078859448949,0.49381009308535916,0.5110882324683109,0.510843922475742,0.49724939225615906,0.50198142644277645,0.4929213417184266',
                        style={'width': '100%', 'text-align': 'center'}
                    )
                    if identifier == 'bootstrap' else
                    dcc.Slider(min=0, max=1, step=0.005,
                               value=accuracy,
                               marks=marks_accuracy,
                               included=False,
                               id=f"{identifier}_accuracy",
                               tooltip={"placement": "top", "always_visible": True},
                               ),

                    width={
                        "size": 12})),

                dbc.Row(dbc.Col(html.H4("Confidence level", style={'text-align': 'center'}), width={
                    "size": 12})),
                dbc.Row(dbc.Col(

                    dcc.Slider(min=0, max=1, step=0.01,
                               value=confidence_level,
                               marks=marks_confidence,
                               included=False,
                               id=f"{identifier}_confidence",
                               tooltip={"placement": "top", "always_visible": True},
                               ),

                    width={
                        "size": 12}))
            ])
        ], className='left_pane_content')
    ], id=f"{identifier}_left_pane", className='estimation-panel')


def plot_confidence_interval(confidence_intervals):
    fig = go.Figure()
    fig.update_yaxes(showgrid=True)

    col_number = 0
    for level, ci in confidence_intervals:
        category = str(level)
        x = [ci[0], ci[1]]
        y = [level, level]
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                text=[round(v, 2) for v in x],
                mode="lines+markers+text",
                textposition=["bottom center", "bottom center"],
                line_color=palette[col_number],
                name=category,
            )
        )
        col_number += 1

    fig.update_layout(
        {
            "yaxis": {"title": "Confidence level", "tickformat": ',.0%', "range": [max(0, confidence_intervals[0][0] - 0.05), 1.0]},
            "xaxis": {"title": "Accuracy"},
            "template": "plotly_white",
            "showlegend": False,
            "height": 250,
            "margin": dict(l=0, r=0, t=0, b=0),
        }
    )

    return fig
