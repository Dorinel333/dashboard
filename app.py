from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from base64 import b64encode
import io

df = pd.read_csv('languages.csv', encoding='ISO-8859-1')

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Programming Languages"),
        html.P("Properties:"),
        dcc.Dropdown(
            id="values",
            options=[
                {"label": "Number of Users", "value": "number_of_users"},
                {"label": "Wikipedia Daily Page Views", "value": "wikipedia_daily_page_views"},
                {"label": "Number of Jobs", "value": "number_of_jobs"},
                {"label": "Book Count", "value": "book_count"},
                {"label": "Github Languages Repositories", "value": "github_language_repos"},
            ],
            value="number_of_users",
            clearable=False,
        ),
        dcc.Graph(id="graph"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph1")),
            ]
        )
    ]
)

@app.callback(
    Output("graph", "figure"),
    Output("graph1", "figure"),
    Input("values", "value"),
)
def generate_charts(values):
    fig_pie = px.pie(df, values=values, names="title", hole=0.3)

    label_mapping = {
        "number_of_users": "Number of Users",
        "wikipedia_daily_page_views": "Wikipedia Page Views",
        "number_of_jobs": "Number of Jobs",
        "book_count": "Book Count",
        "github_language_repos": "Github Languages Repositories",
    }
    x_label = label_mapping.get(values, "Default Label")
    
    dff = df[df[values] > 0].sort_values(by=values, ascending=True).head(10)
    fig_bar = px.bar(dff, x=values, y="title", labels={"title": "Language", values: x_label},)
    
    return fig_pie, fig_bar

if __name__ == "__main__":
    app.run_server(debug=True)
