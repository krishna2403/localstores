import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.dependencies import Input, Output, State

# Generate some in-memory data.
locations = [dict(lat=50.064840, lon=14.442720), dict(lat=50.082525, lon=14.451692), dict(lat=50.075539, lon=14.437800)]
Prague1 = dlx.dicts_to_geojson(locations)





app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
# For Heroku deployment.
server = app.server


df_spending = pd.DataFrame({
    "Day": ["Mo", "Tue", "We", "Tu", "Fr", "Sa", "So"],
    "Amount": [300, 500, 0, 600, 200, 0, 400],
})

df_status = pd.DataFrame(
    {
        "Parameter": ["Points", "Level", "Number of visits"],
        "Value": ["5000", "3", "20"],
    }
)

df_ranking = pd.DataFrame(
    {
        "Place": [x for x in range(1,5)],
        "Username": ["chrisO", "DavidP", "JosefH", "PeterK"],
        "Level": ["5", "8", "20", "7"],
        "Points": ["5000", "8000", "20000", "7000"],
    }
)


fig_spending = px.bar(df_spending, x="Day", y="Amount", title="Purchases last week")
fig_spending.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
})

regionalRanking = dbc.Table.from_dataframe(df_ranking, striped=True, bordered=True, hover=True)
friendsRanking = dbc.Table.from_dataframe(df_ranking, striped=True, bordered=True, hover=True)


app.layout = html.Div([

    dbc.Nav(
        [
            dbc.NavbarBrand(html.H3("Local Heroes"), className="ml-2"),
            dbc.NavLink("Dashboard", href="#"),
            dbc.NavLink("Sign-Up as Customer", href="#"),
            dbc.NavLink("Sign-Up as Owner", href="#"),
            dbc.NavLink("Login", href="#"),
            dbc.NavLink("Invite Friends", href="#"),
        ], className= 'navbar navbar-expand-lg navbar-light bg-light fixed-top'
    ),
    # Row: Title
#    html.Div([
#        dbc.Input(id='inputLocation', type="text", className="col-4"),
#        dbc.Button("Primary", color="primary", className="mr-1 mt-2")
#    ], className="pt-5"),
    # Row: Map + Bar Chart
    html.Div([
        # Column: Map
        html.Div([
            html.H5("Map of local stores and restaurants"),
            dl.Map(center=[50.064840, 14.442720], zoom=13, children=[
                    dl.TileLayer(),
                    dl.GeoJSON(data=Prague1),
                # in-memory geojson (slowest option)
                ], style={'width': '100%', 'height': '35vh', 'margin': "auto", "display": "block"}, id="map"),
                html.Div(id="stores")
        ], className="col-md-4"),
        # Column: Bar Chart
        html.Div([
            html.H5("Statistics"),
            dbc.Table.from_dataframe(df_status, striped=True, bordered=True, hover=True)
        ], className="col-md-4"),
        html.Div([
            html.H5("Messages from store owners"),
            html.Article([
                html.Article([
                    html.P("Hey everone, today I am offering your a special thing bla bla bla")
                ],className="each_message2"),
            html.Article([
                    html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi,")
                ],className="each_message1"),
            html.Article([
                    html.P("At placeat explicabo temporibus eius est tenetur? Maiores impedit")
                ],className="each_message2"),
            html.Article([
                    html.P("Hello, we are open today until 10 pm. Stop by and try our new ...")
                ],className="each_message1")
            ],className="message_section")
        ], className="col-md-4")
    ], className="row my-5"),
    # Row: Line Chart + Donut Chart
    html.Div([
        # Column: Line Chart
        html.Div([
            html.H5("Rewards"),
            dbc.ListGroup([
                dbc.ListGroupItem("20% discount at Rob's Pizza"),
                dbc.ListGroupItem("Next beer for free at BeerGeek"),
                dbc.ListGroupItem("Free coffee at MyBackery"),
    ])], className="col-md-4"),
        html.Div([
            dcc.Graph(id="spending", figure=fig_spending)
        ], className="col-md-4"),
        html.Div([
            html.H5("Ranking"),
    dbc.Tabs(
        [
            dbc.Tab(regionalRanking, label="Friends"),
            dbc.Tab(friendsRanking, label="People Around Me")
        ]
    )
        ], className="col-md-4")
    ], className="row mt-5"),

], className="container-fluid pt-5")



if __name__ == '__main__':
    app.run_server(debug=True)