import plotly.graph_objects as go

def plot_confidence_interval(confidence_intervals):
    layout_ = go.Layout({"yaxis": {"title":"Confidence"},
                       "xaxis": {"title":"Confidence Interval for given confidence"},
                       "template": 'plotly_white',
                       "showlegend": False})
    
    intervals = ['User defined', '90%', '95%', '98%', '99%']

    fig = go.Figure(layout=layout_)
    fig.update_xaxes(range=[0,100])
    fig.update_yaxes(showgrid=True, type='category')

    for conf_int, category in zip(confidence_intervals, intervals):
        print(conf_int)
        x = [round(conf_int[0], 2), round(conf_int[1], 2)]
        y = [category, category]
        fig.add_trace(go.Scatter(x=x, y=y, text=x,
                    mode='lines+markers+text',
                    textposition='top center',
                    name=category))
    #fig.show()
    return fig