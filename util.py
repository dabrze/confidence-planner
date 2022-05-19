import numpy as np
import confidence_planner as cp
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from constants import *


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


def create_estimation_form(task, name, method, sample_size=None, accuracy=0.75, confidence_level=0.8,
                           n_splits=None, interval_radius=0.05):
    if task == "ci":
        result_title = "Estimated confidence intervals"
    elif task == "sample_size":
        result_title = "Estimated sample size"
    else:
        result_title = "Estimated confidence level"

    return dbc.Container(
        dbc.Row(children=[
            create_input_panel(task, name, method, sample_size, accuracy, confidence_level, n_splits, interval_radius),
            create_result_panel(task, method, result_title),
        ], id=f"{task}_{method}")
    )


def create_input_panel(task, name, method, sample_size, accuracy, confidence_level, n_splits,
                       interval_radius):
    elements = list()
    elements.append(html.H2(name))
    elements.append(html.P(descriptions_dict[f"{task}_{method}"], className="method-description"))

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
    if task == "ci" or task == "confidence_level":
        if method == "bootstrap" or task == "ci":
            displayClass = ""
        else:
            displayClass = "hidden"

        elements.append(html.H4("List of bootstrap accuracies" if method == 'bootstrap' else "Accuracy",
                                className=displayClass))
        elements.append(
            dcc.Input(type='text', placeholder='Comma-separated list of accuracies',
                      value=accuracy, id=f"{task}_{method}_accuracy", className=displayClass)
            if method == 'bootstrap' else
            dcc.Slider(min=0, max=1, step=0.005, value=accuracy, marks=marks_accuracy, included=False,
                       id=f"{task}_{method}_accuracy", tooltip={"placement": "top", "always_visible": True},
                       className=displayClass)
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
            "yaxis": {"title": "Confidence level", "tickformat": ',.0%',
                      "range": [max(0, confidence_intervals[0][0] - 0.05), 1.0]},
            "xaxis": {"title": "Accuracy"},
            "template": "plotly_white",
            "showlegend": False,
            "height": 250,
            "margin": dict(l=0, r=0, t=0, b=0),
        }
    )

    return fig
