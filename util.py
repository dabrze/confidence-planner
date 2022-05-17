# Graph generation imports
import confidence_planner as cp
import plotly.graph_objects as go
import plotly.express as px
import dash_html_components as html

palette = ["#cc6677", "#f6cf71", "#0f8554", "#1d6996", "#ff9900"]


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
