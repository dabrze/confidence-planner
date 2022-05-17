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


def ci_callback(button, sample_size, accuracy, confidence_level, method, n_splits=None):
    intervals = calculate_multiple_ci(
        sample_size, accuracy, confidence_level, method=method, n_splits=n_splits
    )
    divs = []

    for level, interval in intervals:
        div_str = (
            f"{level*100}% confidence interval: {interval[0]:.2f} - {interval[1]:.2f}"
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


def create_confidence_interval_view(name, identifier, description, sample_size, accuracy=0.75, confidence_level=0.8,
                                    n_splits=None):
    return html.Div(children=[
        dbc.Row(children=[
            # Left pane (delivering information):
            dbc.Col(html.Div(children=[
                html.H2(name),
                html.Div(children=[
                    # Test description:
                    html.P(description),
                    html.Div(children=[
                        dbc.Row(dbc.Col(html.H4("Number of samples", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                        dbc.Row(dbc.Col(dcc.Input(
                            id=f"{identifier}_sample",
                            type='number',
                            min=1,
                            placeholder='Number of samples',
                            value=sample_size,
                            style={'width': '100%', 'text-align': 'center'}
                        ), width={
                            "size": 6, "offset": 3})),


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
                            "size": 6, "offset": 3}),
                            style={'display': 'none' if n_splits is None else 'flex'}),

                        dbc.Row(dbc.Col(html.H4("Obtained Accuracy", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                        dbc.Row(dbc.Col(

                            dcc.Slider(min=0, max=1, step=0.005,
                                       value=accuracy,
                                       marks=marks_accuracy,
                                       included=False,
                                       id=f"{identifier}_accuracy",
                                       tooltip={"placement": "top", "always_visible": True},
                                       ),

                            width={
                                "size": 8, "offset": 2})),
                        dbc.Row(dbc.Col(html.H4("Confidence", style={'text-align': 'center'}), width={
                            "size": 12, "offset": 0})),
                        dbc.Row(dbc.Col(

                            dcc.Slider(min=0, max=1, step=0.01,
                                       value=confidence_level,
                                       marks=marks_confidence,
                                       included=False,
                                       id=f"{identifier}_confidence",
                                       tooltip={"placement": "top", "always_visible": True},
                                       ),

                            width={
                                "size": 8, "offset": 2})),
                        dbc.Row(dbc.Button("Calculate", outline=False, className='calculate_button',
                                           id=f"{identifier}_button", n_clicks=0), justify='center')
                    ])
                ], className='left_pane_content')
            ], id=f"{identifier}_left_pane", className='left_pane')),

            # Right pane (results):
            dbc.Col(html.Div(children=[
                html.H2("Estimated confidence intervals"),
                html.Div(children=[
                    dcc.Graph(
                        id=f"{identifier}_result_graph",
                        config={'displayModeBar': False},
                    ),
                    html.Div('t_test result', id=f"{identifier}_result")
                ], className='right_pane_content')
            ], id=f"{identifier}_right_pane", className='right_pane')),
        ])
    ], id=f"{identifier}")


def plot_confidence_interval(confidence_intervals):
    layout_ = go.Layout(
        {
            "yaxis": {"title": "Confidence level"},
            "xaxis": {"title": "Accuracy"},
            "template": "plotly_white",
            "showlegend": False,
        }
    )

    fig = go.Figure(layout=layout_)
    fig.update_yaxes(showgrid=True, type="category")

    col_number = 0
    for level, ci in confidence_intervals:
        category = str(level)
        x = [round(ci[0], 2), round(ci[1], 2)]
        y = [category, category]
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                text=x,
                mode="lines+markers+text",
                textposition=["top center", "top center"],
                line_color=palette[col_number],
                name=category,
            )
        )
        col_number += 1

    return fig
