import csv
import os
import shutil
import uuid

from anki.hooks import wrap
from aqt.reviewer import Reviewer
from aqt import mw, gui_hooks

from .session import session


BASE_DIR = os.path.dirname(__file__)
USER_FILES_DIR = os.path.join(BASE_DIR, 'user_files')
FILE_NAME_BASE = str(uuid.getnode())
FILE_NAME_EXT = ".csv"
FILE_NAME = FILE_NAME_BASE + FILE_NAME_EXT
USER_FILE = os.path.join(USER_FILES_DIR, FILE_NAME)

HEADERS = ['uid', 'sid', 'card_id', 'deck_id', 'card_cat', 'deck_cat',
           'question', 'answer', 'question_has_sound', 'answer_has_sound',
           'question_has_video', 'answer_has_video', 'question_has_image',
           'answer_has_image', 'ease', 'type', 'queue', 'due', 'interval',
           'answered_at', 'think_time', 'grade_time', 'total_study_time',
           'ESTIMATED_INTERVAL']


"""
reviewer_did_show_answer
reviewer_did_answer_card
review_did_undo

"""


def ensure_directory_exists():
    if not os.path.exists(USER_FILES_DIR):
        try:
            os.mkdir(USER_FILES_DIR)
        except OSError:
            print("Creation of the directory %s failed" % USER_FILES_DIR)
        else:
            print("Successfully created the directory %s " % USER_FILES_DIR)


def create_initial_file(name=None):
    if name is None:
        name = USER_FILE
    with open(name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)


def backup_old_file():
    i = 0
    file_name = FILE_NAME_BASE + ".old%s" + FILE_NAME_EXT
    path = os.path.join(USER_FILES_DIR, file_name)
    while os.path.exists(path % i):
        i += 1
    shutil.copy2(USER_FILE, path % i)


def init():
    """Create history file if it doesn't exist"""
    ensure_directory_exists()
    try:
        correct = True
        with open(USER_FILE) as f:
            reader = csv.reader(f)
            try:
                first_row = next(reader)
                if not len(first_row) == len(HEADERS):
                    correct = False
            except StopIteration:
                correct = False
        if not correct:
            backup_old_file()
            create_initial_file()
    except FileNotFoundError:
        create_initial_file()


init()


def did_answer_card(reviewer, card, ease):
    session.save_answer(reviewer, card, ease)


def start_session(self):
    session.start()


def stop_session():
    session.stop()


Reviewer.show = wrap(Reviewer.show, start_session)
gui_hooks.reviewer_will_end.append(stop_session)
gui_hooks.reviewer_did_answer_card.append(did_answer_card)
