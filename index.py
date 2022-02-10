from distutils.log import debug
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Graph generation imports
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

# Test code imports
from tests.holdout.z_test import ztest_pr, reverse_ztest_pr, reverse_ztest_pr_conf
import layouts

external_theme = [dbc.themes.COSMO]

app = dash.Dash(external_stylesheets=external_theme,
    suppress_callback_exceptions=True)

# The layout of the home all pages (only the last div changes while moving to different page)
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    layouts.elements['navbar'],
    html.Div(children=layouts.elements['/home'],
             id='page_content', className='page_content'),
    ]
)

# Callback taking care of changing webpage content with respect to given url
@app.callback(Output('page_content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        try:
            page = layouts.elements['/home']
            print('Home webpage already created')
            return page
        except Exception as ex:
            print('No home webpage found' + str(ex))
            return 'No home webpage found' + str(ex)
    else:
        try:
            page = layouts.elements[str(pathname)]
            return page
        except Exception as ex:
            return 'Ups... Something went wrong.\n404 Error, Website not found...' + str(ex)


# Z TEST callback:

@app.callback(
    Output('z_test_result', 'children'), # Text form output
    Output('z_test_result_graph', 'figure'), # Graph form output
    Input('z_test_button', 'n_clicks'), # Button clicks
    State('z_test_sample', 'value'), # Number of samples
    State('z_test_accuracy', 'value'), # Accuracy
    State('z_test_confidence', 'value'), # User defined confidence
    prevent_initial_call=False

)
def z_test_callback(n_click, n, accuracy, confidence):

    intervals = ztest_pr(n, accuracy, confidence)

    plot = plot_confidence_interval(intervals)

    return html.Div(str(intervals)), plot



# Reverse Z TEST (samples) callback:

@app.callback(
    Output('z_test_rev_samples_result', 'children'),
    Input('z_test_rev_samples_button', 'n_clicks'),
    State('z_test_rev_samples_diff', 'value'),
    State('z_test_rev_samples_confidence', 'value'),
    prevent_initial_call=False
)
def reverse_z_test_samples_callback(n_clicks, difference, confidence):
    return html.Div(reverse_ztest_pr(difference, confidence))


# Reverse Z TEST (confidence) callback:

@app.callback(
    Output('z_test_rev_confidence_result', 'children'),
    Input('z_test_rev_confidence_button', 'n_clicks'),
    State('z_test_rev_confidence_sample', 'value'),
    State('z_test_rev_confidence_diff', 'value'),
    prevent_initial_call=False
)
def reverse_z_test_samples_callback(n_clicks, n, difference):
    return html.Div(reverse_ztest_pr_conf(difference, n))
    



if __name__ == '__main__':
    app.run_server(debug=True, port=8080)