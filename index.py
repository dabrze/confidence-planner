from distutils.log import debug
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

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




if __name__ == '__main__':
    app.run_server(debug=True, port=8080)