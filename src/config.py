# Constants Management
# 定数管理：ここでMIDIのデバイス名設定とブラウザ上に表示される値を管理できます

"""
MIDI DEVICE NAME
"""
# Set your MIDI device name here after checking it
MIDI_DEVICE_NAME = "CH345:CH345 MIDI 1 28:0"

"""
Texts for the application
"""
# Language setting: "en" for English, "jp" for Japanese
LANGUAGE = "jp"

# Text dictionaries
TEXTS = {
    "en": {
        "START_BUTTON_TEXT": "Start Lesson",
        "END_BUTTON_TEXT": "End Lesson",
        "TOTAL_LESSON_TIME_TODAY": "Total Lesson Time Today",
        "TOTAL_PLAY_TIME_TODAY": "Total Play Time Today",
        "DF_START_TIME_COLUMN": "Lesson Start Time",
        "DF_END_TIME_COLUMN": "Lesson End Time",
        "DF_PLAY_TIME_COLUMN": "Play Time",
    },
    "jp": {
        "START_BUTTON_TEXT": "レッスン開始🐟",
        "END_BUTTON_TEXT": "レッスン終了🌀",
        "TOTAL_LESSON_TIME_TODAY": "今日のレッスン時間合計",
        "TOTAL_PLAY_TIME_TODAY": "ピアノを弾いていた時間",
        "DF_START_TIME_COLUMN": "レッスン開始時間",
        "DF_END_TIME_COLUMN": "レッスン終了時間",
        "DF_PLAY_TIME_COLUMN": "ピアノを弾いていた時間",
    },
}


# Function to get text based on the current language setting
def get_text(key):
    return TEXTS[LANGUAGE].get(key, "")


# Examples of how to use get_text function
START_BUTTON_TEXT = get_text("START_BUTTON_TEXT")
END_BUTTON_TEXT = get_text("END_BUTTON_TEXT")
TOTAL_LESSON_TIME_TODAY = get_text("TOTAL_LESSON_TIME_TODAY")
TOTAL_PLAY_TIME_TODAY = get_text("TOTAL_PLAY_TIME_TODAY")
DF_START_TIME_COLUMN = get_text("DF_START_TIME_COLUMN")
DF_END_TIME_COLUMN = get_text("DF_END_TIME_COLUMN")
DF_PLAY_TIME_COLUMN = get_text("DF_PLAY_TIME_COLUMN")
