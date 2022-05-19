from distutils.log import debug
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from util import ci_callback, sample_size_callback, confidence_level_callback
import layouts

FONTS = "https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i"
GOOGLE_FONTS_PRECONNECT = { "rel": "preconnect", "href": "https://fonts.googleapis.com" }
GOOGLE_FONTS_GSTATIC = { "rel": "preconnect", "href": "https://fonts.gstatic.com", "crossorigin": "anonymous"}

external_theme = [dbc.themes.BOOTSTRAP, GOOGLE_FONTS_PRECONNECT, GOOGLE_FONTS_GSTATIC, FONTS]

app = dash.Dash(
    __name__, external_stylesheets=external_theme, suppress_callback_exceptions=True
)
server = app.server

layouts.webpages_dict["/home"] = layouts.create_home_page(app)
app.layout = html.Div(
    id="entire_app",
    children=[
        dcc.Location(id="url", refresh=False),
        layouts.webpages_dict["navbar"],
        html.Div(
            children=layouts.webpages_dict["/home"],
            id="page_content",
            className="page_content",
        ),
        dbc.Container(
            html.Footer(html.P('Copyright 2022, Poznan University of Technology.', className='footer-text'))
        )
    ],
)


@app.callback(Output("page_content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        try:
            page = layouts.webpages_dict["/home"]
            print("Home webpage already created")
            return page
        except Exception as ex:
            print("No home webpage found" + str(ex))
            return "No home webpage found" + str(ex)
    else:
        try:
            page = layouts.webpages_dict[str(pathname)]
            return page
        except Exception as ex:
            return (
                "Ups... Something went wrong.\n404 Error, Website not found..."
                + str(ex)
            )


# CI estimation callbacks
for method in ['holdout_wilson', 'holdout_langford', 'holdout_clopper_pearson', 'holdout_z_test', 'holdout_t_test',
               'progressive', 'cv', 'bootstrap']:
    app.callback(
        Output(f"ci_{method}_result", "children"),
        Output(f"ci_{method}_result_graph", "figure"),
        Input(f"ci_{method}_sample", "value"),
        Input(f"ci_{method}_accuracy", "value"),
        Input(f"ci_{method}_confidence", "value"),
        Input(f"ci_{method}", "id"),
        Input(f"ci_{method}_folds", "value"),
    )(ci_callback)


# Sample size estimation callbacks
for method in ['holdout_langford', 'holdout_z_test', 'progressive', 'cv', 'bootstrap']:
    app.callback(
        Output(f"sample_size_{method}_result", "children"),
        Input(f"sample_size_{method}_interval_radius", "value"),
        Input(f"sample_size_{method}_confidence", "value"),
        Input(f"sample_size_{method}", "id"),
        Input(f"sample_size_{method}_folds", "value"),
    )(sample_size_callback)


# Confidence level estimation callbacks
for method in ['holdout_langford', 'holdout_z_test', 'holdout_t_test', 'progressive', 'cv', 'bootstrap']:
    app.callback(
        Output(f"confidence_level_{method}_result", "children"),
        Input(f"confidence_level_{method}_sample", "value"),
        Input(f"confidence_level_{method}_interval_radius", "value"),
        Input(f"confidence_level_{method}", "id"),
        Input(f"confidence_level_{method}_folds", "value"),
        Input(f"confidence_level_{method}_accuracy", "value"),
    )(confidence_level_callback)


if __name__ == "__main__":
    app.run_server(debug=False)
