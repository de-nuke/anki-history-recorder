import csv
import os
import shutil

from aqt import mw

from .const import HEADERS


BASE_DIR = os.path.dirname(__file__)
USER_FILES_DIR = os.path.join(BASE_DIR, 'user_files')
FILE_NAME_BASE = str(mw.pm.meta.get('id'))
FILE_NAME_EXT = ".csv"
FILE_NAME = FILE_NAME_BASE + FILE_NAME_EXT
USER_FILE = os.path.join(USER_FILES_DIR, FILE_NAME)


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


def init_storage():
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


class Storage:
    def __init__(self):
        init_storage()

    def save(self, data: dict):
        with open(USER_FILE, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writerow(data)
