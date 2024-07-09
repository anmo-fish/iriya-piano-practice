import threading
import mido
import logging
import time
from queue import Queue
from src.database import update_total_duration, update_end_time, insert_start_time

# ログ設定
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger()
# handler = logging.FileHandler('midi_log.txt', 'w')
# logger.addHandler(handler)

message_queue = Queue()
stop_event = threading.Event()
start_time = None
last_off_time = None
running = False


def log_message(message):
    logging.info(message)
    message_queue.put(message)


def midi_input_callback(message):
    global start_time, last_off_time, stop_event
    current_time = time.time()
    # logging.info(f"MIDI message received: {message}")

    if message.type == "note_on" and message.velocity > 0:
        if start_time is None:
            start_time = current_time
        stop_event.set()

    elif message.type == "note_off" or (
        message.type == "note_on" and message.velocity == 0
    ):
        # log_message(f'Note OFF: {message.note} velocity={message.velocity}')
        last_off_time = current_time
        stop_event.set()


def start_midi_input(device_name):
    global running, start_time, last_off_time
    running = True
    start_time = time.time()
    last_off_time = None
    logging.info("MIDI input started")

    try:
        insert_start_time(start_time)
        logging.info(f"Start time inserted: {start_time}")
    except Exception as e:
        logging.error(f"Error inserting start time: {e}")

    def input_thread():
        global last_off_time, start_time
        try:
            with mido.open_input(device_name, callback=midi_input_callback) as port:
                logging.info(f"Opened MIDI input: {device_name}")
                while running:
                    if stop_event.wait(3):
                        stop_event.clear()
                    else:
                        if start_time is not None and last_off_time is not None:
                            total_time = last_off_time - start_time
                            try:
                                update_total_duration(total_time)
                                log_message(
                                    f"Total performance time: {total_time:.2f} seconds"
                                )
                            except Exception as e:
                                logging.error(f"Error updating total duration: {e}")
                            start_time = None
                            last_off_time = None
                    time.sleep(0.1)
        except Exception as e:
            logging.error(f"Error in input_thread: {e}")

    thread = threading.Thread(target=input_thread)
    thread.daemon = True
    thread.start()


def stop_midi_input():
    global running, start_time, last_off_time
    running = False
    start_time = None
    last_off_time = None
    try:
        update_end_time()
        logging.info("MIDI input stopped")
    except Exception as e:
        logging.error(f"Error in stop_midi_input: {e}")
