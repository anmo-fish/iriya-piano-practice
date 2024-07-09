from dash import dcc, html
import dash_bootstrap_components as dbc
from src.config import START_BUTTON_TEXT, END_BUTTON_TEXT


def create_layout(app):
    return dbc.Container(
        [
            dbc.Container(
                [
                    # dbc.Row(
                    #     html.H1("Iriya 🐈🐈🐈"),
                    #     className="bg-dark text-white text-center",
                    #     style={"height": "8vh", "padding": "10px 0"},
                    # ),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                children=[
                                    html.Img(
                                        src=app.get_asset_url("logo.png"),
                                        style={
                                            "height": "40px",
                                            "margin-right": "10px",
                                        },
                                    ),
                                    html.H1(
                                        "Iriya",
                                        style={
                                            "display": "inline-block",
                                            "vertical-align": "middle",
                                        },
                                    ),
                                    html.Img(
                                        src=app.get_asset_url("logo.png"),
                                        style={
                                            "height": "40px",
                                            "margin-left": "10px",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center",
                                },
                            ),
                            className="bg-dark text-white text-center",
                            style={"height": "8vh", "padding": "10px 0"},
                        )
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    START_BUTTON_TEXT,
                                    id="start-button",
                                    color="success",
                                    disabled=False,
                                    style={"font-size": "20px", "width": "100%"},
                                ),
                                width={"size": 4, "offset": 2},
                                className="text-center",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    END_BUTTON_TEXT,
                                    id="stop-button",
                                    color="danger",
                                    disabled=True,
                                    style={"font-size": "20px", "width": "100%"},
                                ),
                                width={"size": 4},
                                className="text-center",
                            ),
                        ],
                        className="my-3",
                    ),
                    # dbc.Row([
                    #     dbc.Col(html.Div(id="log-messages", className="p-2 border rounded"), width=12)
                    # ], className="my-3"),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    id="start-duration",
                                    className="p-2 border rounded text-center",
                                ),
                                width=6,
                            ),
                            dbc.Col(
                                html.Div(
                                    id="total-duration",
                                    className="p-2 border rounded text-center",
                                ),
                                width=6,
                            ),
                        ],
                        className="my-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    id="performance-table",
                                    className="p-2 border rounded",
                                ),
                                width=12,
                            )
                        ],
                        className="my-3",
                    ),
                    dcc.Interval(
                        id="interval-component", interval=1 * 1000, n_intervals=0
                    ),
                ],
                style={"max-width": "1280px", "margin": "0 auto"},
            )
        ],
        fluid=True,
    )
