# Graph generation imports
import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle

palette = cycle(px.colors.qualitative.Antique)

def plot_confidence_interval(confidence_intervals, user_def):
    layout_ = go.Layout({"yaxis": {"title":"Confidence"},
                       "xaxis": {"title":"Confidence Interval for given confidence"},
                       "template": 'plotly_white',
                       "showlegend": False})
    
    intervals = [f'{user_def}%', '90%', '95%', '98%', '99%']

    fig = go.Figure(layout=layout_)
    # fig.update_xaxes(range=[-3,103])
    fig.update_yaxes(showgrid=True, type='category')

    for conf_int, category in zip(confidence_intervals, intervals):
        x = [round(conf_int[0], 2), round(conf_int[1], 2)]
        y = [category, category]
        fig.add_trace(go.Scatter(x=x, y=y, text=x,
                    mode='lines+markers+text',
                    textposition=['top center', 'top center'],
                    line_color=next(palette),
                    name=category))
    #fig.show()
    return fig