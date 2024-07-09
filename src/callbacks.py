import dash
import time
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from src.midi_handler import (
    start_midi_input,
    stop_midi_input,
    message_queue,
    running,
    start_time,
)
from src.database import calculate_today_durations, fetch_latest_performances
from src.utils import format_duration
from src.config import (
    MIDI_DEVICE_NAME,
    TOTAL_LESSON_TIME_TODAY,
    TOTAL_PLAY_TIME_TODAY,
    DF_START_TIME_COLUMN,
    DF_END_TIME_COLUMN,
    DF_PLAY_TIME_COLUMN,
)

log_messages = []


def register_callbacks(app):
    @app.callback(
        # Output("log-messages", "children"),
        Output("start-duration", "children"),
        Output("total-duration", "children"),
        Output("performance-table", "children"),
        Input("interval-component", "n_intervals"),
        Input("stop-button", "n_clicks"),
    )
    def update_output(n, stop_clicks):
        global log_messages, running, start_time

        # while not message_queue.empty():
        #     log_messages.append(message_queue.get())

        current_time = time.time()
        if running and start_time is not None:
            current_duration = current_time - start_time
        else:
            current_duration = 0

        start_duration, total_duration = calculate_today_durations()
        start_duration_text = f"{TOTAL_LESSON_TIME_TODAY}: {format_duration(start_duration + current_duration)}"
        total_duration_text = (
            f"{TOTAL_PLAY_TIME_TODAY}: {format_duration(total_duration)}"
        )

        performances = fetch_latest_performances()
        # print(f"Log messages: {log_messages}")  # デバッグ情報
        # print(f"Start duration: {start_duration_text}, Total duration: {total_duration_text}")  # デバッグ情報

        table_header = [
            html.Thead(
                html.Tr(
                    [
                        html.Th("ID"),
                        html.Th(DF_START_TIME_COLUMN),
                        html.Th(DF_END_TIME_COLUMN),
                        html.Th(DF_PLAY_TIME_COLUMN),
                    ]
                )
            )
        ]
        rows = [
            html.Tr(
                [
                    html.Td(perf[0]),
                    html.Td(perf[1]),
                    html.Td(perf[2]),
                    html.Td(format_duration(perf[3])),
                ]
            )
            for perf in performances
        ]
        table_body = [html.Tbody(rows)]

        return (
            # "\n".join(log_messages),
            start_duration_text,
            total_duration_text,
            dbc.Table(
                table_header + table_body, bordered=True, striped=True, hover=True
            ),
        )

    @app.callback(
        Output("start-button", "n_clicks"),
        Output("stop-button", "n_clicks"),
        Output("stop-button", "disabled"),
        Output("start-button", "disabled"),
        Input("start-button", "n_clicks"),
        Input("stop-button", "n_clicks"),
        State("start-button", "disabled"),
        State("stop-button", "disabled"),
    )
    def handle_button_clicks(start_clicks, stop_clicks, start_disabled, stop_disabled):
        global running, start_time

        ctx = dash.callback_context
        if not ctx.triggered:
            return start_clicks, stop_clicks, stop_disabled, start_disabled

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "start-button":
            start_midi_input(MIDI_DEVICE_NAME)
            running = True
            start_time = time.time()  # start_time を開始時に設定
            return start_clicks, stop_clicks, False, True
        elif button_id == "stop-button":
            stop_midi_input()
            running = False
            start_time = None  # stop 時に start_time をリセット
            return start_clicks, stop_clicks, True, False

        return start_clicks, stop_clicks, stop_disabled, start_disabled
