import csv
import os
import shutil
import uuid

from aqt.reviewer import Reviewer
from aqt import mw

BASE_DIR = os.path.dirname(__file__)
USER_FILES_DIR = os.path.join(BASE_DIR, 'user_files')
FILE_NAME_BASE = str(uuid.getnode())
FILE_NAME_EXT = ".csv"
FILE_NAME = FILE_NAME_BASE + FILE_NAME_EXT
USER_FILE = os.path.join(USER_FILES_DIR, FILE_NAME)


HEADERS = ['uid', 'card_id', 'deck_id', 'card_cat', 'deck_cat', 'question',
           'answer', 'ease', 'maturity', 'last_shown', 'answered_at',
           'think_time', 'grade_time', 'has_image', 'has_sound',
           'total_study_time', 'ESTIMATED_INTERVAL']


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
