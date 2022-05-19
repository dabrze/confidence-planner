import numpy as np
import confidence_planner as cp
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

palette = ["#cc6677", "#f6cf71", "#0f8554", "#1d6996", "#ff9900"]

marks_accuracy = {
    0:   {'label': '0.0', 'style': {'color': 'black'}},
    0.1: {'label': '0.1', 'style': {'color': 'black'}},
    0.2: {'label': '0.2', 'style': {'color': 'black'}},
    0.3: {'label': '0.3', 'style': {'color': 'black'}},
    0.4: {'label': '0.4', 'style': {'color': 'black'}},
    0.5: {'label': '0.5', 'style': {'color': 'black'}},
    0.6: {'label': '0.6', 'style': {'color': 'black'}},
    0.7: {'label': '0.7', 'style': {'color': 'black'}},
    0.8: {'label': '0.8', 'style': {'color': 'black'}},
    0.9: {'label': '0.9', 'style': {'color': 'black'}},
    1.0: {'label': '1.0', 'style': {'color': 'black'}}
}

marks_interval={
    0: {'label': '0.0', 'style': {'color': 'black'}},
    0.1: {'label': '0.1', 'style': {'color': 'black'}},
    0.2: {'label': '0.2', 'style': {'color': 'black'}},
    0.3: {'label': '0.3', 'style': {'color': 'black'}},
    0.4: {'label': '0.4', 'style': {'color': 'black'}},
    0.5: {'label': '0.5', 'style': {'color': 'black'}},
}

marks_confidence = {
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


def ci_callback(sample_size, accuracy, confidence_level, task_method, n_splits=None):
    method = task_method[len("ci_"):]

    if method == "bootstrap":
        accuracy = [float(accuracy) for accuracy in accuracy.split(",")]
        mean_accuracy = np.mean(accuracy)
    else:
        mean_accuracy = accuracy

    intervals = calculate_multiple_ci(
        sample_size, accuracy, confidence_level, method=method, n_splits=n_splits
    )
    divs = [
        dcc.Markdown(f"For a **mean accuracy of {mean_accuracy:.2f}** obtained on **{method.split('_')[0]}** test "
                     f"data consisting of a total of **{sample_size} examples**, the confidence intervals are:",
                     style={"margin-bottom": "14px"})
    ]

    for level, interval in intervals:
        div_str = (
            f"{level*100}% CI: {interval[0]:.2f} - {interval[1]:.2f}"
        )
        divs.append(html.Div(div_str))

    plot = plot_confidence_interval(intervals)

    return divs, plot


def sample_size_callback(interval_radius, confidence_level, task_method, n_splits=None):
    method = task_method[len("sample_size_"):]

    sample_size = cp.estimate_sample_size(
        interval_radius, confidence_level, method=method, n_splits=n_splits
    )

    if n_splits is None:
        return dcc.Markdown(
            f"The estimated number of samples needed to obtain a **{round(confidence_level*100, 0)}% confidence "
            f"interval** with a **{interval_radius} radius** is: **{sample_size} samples.**"
        )
    else:
        return dcc.Markdown(
            f"The estimated number of samples needed to obtain a **{round(confidence_level * 100, 0)}% confidence "
            f"interval** with a **{interval_radius} radius** when performing **{n_splits}-fold** cross-validation is: "
            f"**{sample_size} samples**."
        )


def confidence_level_callback(
    sample_size, interval_radius, task_method, n_splits=None, accuracy=None
):
    method = task_method[len("confidence_level_"):]
    if method == "bootstrap":
        accuracy = [float(accuracy) for accuracy in accuracy.split(",")]

    confidence_level = cp.estimate_confidence_level(
        sample_size,
        interval_radius,
        method=method,
        n_splits=n_splits,
        accuracies=accuracy,
    )

    if n_splits is None:
        return dcc.Markdown(
            f"The estimated confidence level of an **{interval_radius} radius** "
            f"interval is : **{confidence_level*100:.1f}%**."
        )
    else:
        return dcc.Markdown(
            f"The estimated confidence level of  **{n_splits}-fold** cross-validation with an "
            f"**{interval_radius} radius** interval is : **{confidence_level*100:.1f}%**."
        )


def create_estimation_form(task, name, method, description, sample_size=None, accuracy=0.75, confidence_level=0.8,
                           n_splits=None, interval_radius=0.05, result_title="Estimated confidence intervals"):
    return dbc.Container(
        dbc.Row(children=[
            create_input_panel(task, name, method, description, sample_size, accuracy, confidence_level, n_splits,
                               interval_radius),
            create_result_panel(task, method, result_title),
        ], id=f"{task}_{method}")
    )


def create_input_panel(task, name, method, description, sample_size, accuracy, confidence_level, n_splits,
                       interval_radius):
    elements = list()
    elements.append(html.H2(name))
    elements.append(html.P(description))

    # Number of samples
    if task == "ci" or task == "confidence_level":
        elements.append(html.H4("Number of samples"))
        elements.append(dcc.Input(type='number', min=1, placeholder='Number of samples', value=sample_size,
                                  id=f"{task}_{method}_sample"))

    # Number of folds
    elements.append(html.H4("Number of folds", style={'display': 'none' if n_splits is None else 'block'}))
    elements.append(dcc.Input(type='number', min=2, placeholder='Number of folds', value=n_splits,
                              id=f"{task}_{method}_folds", style={'display': 'none' if n_splits is None else 'block'}))

    # Accuracy
    if task == "ci" or (task == "confidence_level" and method == "bootstrap"):
        elements.append(html.H4("List of bootstrap accuracies" if method == 'bootstrap' else "Accuracy"))
        elements.append(
            dcc.Input(type='text', placeholder='Comma-separated list of accuracies',
                      value=accuracy, id=f"{task}_{method}_accuracy") if method == 'bootstrap' else
            dcc.Slider(min=0, max=1, step=0.005, value=accuracy, marks=marks_accuracy, included=False,
                       id=f"{task}_{method}_accuracy", tooltip={"placement": "top", "always_visible": True},)
        )

    # Interval radius
    if task == "sample_size" or task == "confidence_level":
        elements.append(html.H4("Expected interval radius"))
        elements.append(
            dcc.Slider(min=0, max=0.5, step=0.01, value=interval_radius, marks=marks_interval, included=False,
                       id=f"{task}_{method}_interval_radius", tooltip={"placement": "top", "always_visible": True})
        )

    # Confidence level
    if task == "ci" or task == "sample_size":
        elements.append(html.H4("Confidence level"))
        elements.append(
            dcc.Slider(min=0, max=1, step=0.01, value=confidence_level, marks=marks_confidence, included=False,
                       id=f"{task}_{method}_confidence", tooltip={"placement": "top", "always_visible": True})
        )

    return dbc.Col(elements, id=f"{method}_left_panel", className='estimation-panel')


def create_result_panel(task, method, result_title):
    elements = list()
    elements.append(html.H2(result_title))
    elements.append(html.Div('', id=f"{task}_{method}_result"))

    if task == "ci":
        elements.append(
            dcc.Graph(
                id=f"{task}_{method}_result_graph",
                config={'displayModeBar': False},
            )
        )

    return dbc.Col(elements, id=f"{method}_right_panel", className='estimation-panel')


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
