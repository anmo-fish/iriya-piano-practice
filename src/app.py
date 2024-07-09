import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from src.callbacks import register_callbacks
from src.layout import create_layout

# Dashアプリケーションのセットアップ
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], update_title=None
)
app.title = "Iriya"
server = app.server
app.layout = create_layout(app)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
