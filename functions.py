# Graph generation imports
import plotly.graph_objects as go
import plotly.express as px

palette = ['#cc6677', '#f6cf71', '#0f8554', '#1d6996', '#ff9900']

def plot_confidence_interval(confidence_intervals, user_def):
    layout_ = go.Layout({"yaxis": {"title":"Confidence"},
                       "xaxis": {"title":"Confidence Interval for given confidence"},
                       "template": 'plotly_white',
                       "showlegend": False})
    
    intervals = [f'{user_def}%', '90%', '95%', '98%', '99%']

    fig = go.Figure(layout=layout_)
    # fig.update_xaxes(range=[-3,103])
    fig.update_yaxes(showgrid=True, type='category')

    col_number = 0
    for conf_int, category in zip(confidence_intervals, intervals):
        x = [round(conf_int[0], 2), round(conf_int[1], 2)]
        y = [category, category]
        fig.add_trace(go.Scatter(x=x, y=y, text=x,
                    mode='lines+markers+text',
                    textposition=['top center', 'top center'],
                    line_color=palette[col_number],
                    name=category))
        col_number += 1
    #fig.show()
    return fig