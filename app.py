import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

data = pd.read_csv("vgsales.csv")
data = data.dropna(subset = ['Year', 'Genre', 'Publisher'])


# sub dataframe
df_eu = data[['Year', 'Name', 'Global_Sales']]
df_eu = df_eu.groupby(['Year']).agg({'Global_Sales':['sum']}).reset_index()
df_eu.columns = ['Year', 'Global_Sales_sum']
df_eu = df_eu.sort_values(by='Year', ascending=True)



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Video Games Sales"



app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(className="header-emoji"),
                html.H1(
                    children="Video Games Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of video game sales"
                             " in EU, Japan, NA and global sales"
                             " between 1980 and 2016",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=dcc.Graph(
                id="price-bar-chart",
                config={"displayModeBar": True},
                figure={
                    "data": [
                        {
                            "x": df_eu["Year"],
                            "y": df_eu["Global_Sales_sum"],
                            "type": "bar",
                            "hovertemplate": "$%{y:.2f}"
                                                "<extra></extra>",
                        },
                    ],
                    "layout": {
                        "title": {
                            "text": "Yearly Global sales",
                            "x": 0.05,
                            "xanchor": "left",
                        },
                        "xaxis": {"fixedrange": True},
                        "yaxis": {
                            "tickprefix": "$",
                            "fixedrange": True,
                        },
                        "colorway": ["#0CAFFF"],
                    },
                },
            ),
            className="card-title",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Genre", className="menu-title"),
                        dcc.Dropdown(
                            id="genre-filter",
                            options=[
                                {"label": Genre, "value": Genre}
                                for Genre in np.sort(data.Genre.unique())
                            ],
                            value="Sports",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Publisher", className="menu-title"),
                        dcc.Dropdown(
                            id="publisher-filter",
                            options=[
                                {"label": Publisher, "value": Publisher}
                                for Publisher in data.Publisher.unique()
                            ],
                            value="Nintendo",
                            clearable=False,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                )
            ],
            className="menu",
        ),
            html.Div(
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id="price-chart-na", config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id="price-chart-eu", config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id="price-chart-jp", config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                ],
                className="wrapper",
            ),
    ]
)





@app.callback(
    [Output("price-chart-na", "figure"), Output("price-chart-eu", "figure"), Output("price-chart-jp", "figure")],
    [
        Input("genre-filter", "value"),
        Input("publisher-filter", "value")
    ],
)

def update_charts(Genre, Publisher):
    mask = (
        (data.Genre == Genre)
        & (data.Publisher == Publisher)
    )
    filtered_data = data.loc[mask, :]
    filtered_data = filtered_data.groupby(['Year']).agg({'EU_Sales': ['sum'],
                                         'NA_Sales':['sum'], 'JP_Sales':['sum']}).reset_index()
    filtered_data.columns = ['Year', 'EU_Sales', 'NA_Sales', 'JP_Sales']
    price_chart_na = {
        "data": [
            {
                "x": filtered_data["Year"],
                "y": filtered_data["NA_Sales"],
                "type": "bar",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "NA Sales",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#15f4ee"],
        },
    }

    price_chart_eu = {
        "data": [
            {
                "x": filtered_data["Year"],
                "y": filtered_data["EU_Sales"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {
                "text": "EU Sales",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#4D4DFF"],
        },
    }

    price_chart_jp = {
        "data": [
            {
                "x": filtered_data["Year"],
                "y": filtered_data["JP_Sales"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {
                "text": "JP Sales",
                "x": 0.05,
                "xanchor": "left"
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#007FFF"],
        },
    }
    return price_chart_na, price_chart_eu, price_chart_jp



if __name__ == "__main__":
    app.run_server(debug=True)

