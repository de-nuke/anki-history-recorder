import csv
import os
import shutil
from abc import abstractmethod

from aqt import mw

from .const import HEADERS, USER_FILES_DIR
from .contrib import RecordsSender
from .utils import normalize_to_filename


FILE_NAME_EXT = ".csv"


def ensure_directory_exists():
    if not os.path.exists(USER_FILES_DIR):
        try:
            os.mkdir(USER_FILES_DIR)
        except OSError:
            print("Creation of the directory %s failed" % USER_FILES_DIR)
        else:
            print("Successfully created the directory %s " % USER_FILES_DIR)


def create_initial_file(path):
    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)


def backup_old_file(file_path):
    i = 0
    path = file_path + ".old%s"
    while os.path.exists(path % i):
        i += 1
    shutil.copy2(file_path, path % i)


def get_profile_name():
    profile_name = mw.pm.name
    if not profile_name:
        profile_name = mw.pm.meta.get('id') or "unknown"
    return profile_name


def get_file_name():
    return normalize_to_filename(get_profile_name()) + FILE_NAME_EXT


def get_file_path():
    return os.path.join(USER_FILES_DIR, get_file_name())


class Storage:
    """Abstract base class for different storage classes"""

    @abstractmethod
    def save(self, data):
        """Save data"""

    @abstractmethod
    def init_storage(self):
        """Perform some initialization operations"""


class RemoteStorage(Storage):
    """
    Storage that sends a record to the server, than pass it to AWS DynamoDB.
    """

    def __init__(self):
        self.records_sender = None
        self._on_started_hooks = []
        self._on_finished_hooks = []

    def save(self, data):
        self.records_sender = RecordsSender([data])
        self.records_sender.started.connect(self.run_on_started)
        self.records_sender.finished.connect(self.run_on_finished)
        self.records_sender.start()

    def init_storage(self):
        pass

    def on_started(self, func):
        self._on_started_hooks.append(func)

    def on_finished(self, func):
        self._on_finished_hooks.append(func)

    def run_on_started(self):
        for hook in self._on_started_hooks:
            hook()

    def run_on_finished(self, is_success):
        for hook in self._on_finished_hooks:
            hook(is_success)


class LocalStorage(Storage):
    """Storage that saves all the records in a local CSV files"""
    def __init__(self):
        self.file_path = None

    def save(self, data: dict):
        with self.get_file() as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writerow(data)

    def get_file(self):
        if self.file_path:
            return open(self.file_path, 'a', encoding='utf-8', newline='\n')
        else:
            self.init_storage()

    def init_storage(self):
        """
        Create history file if it doesn't exist and return its name
        """
        ensure_directory_exists()
        file_path = get_file_path()
        try:
            correct = True
            with open(file_path, encoding='utf-8') as f:
                reader = csv.reader(f)
                try:
                    first_row = next(reader)
                    if not len(first_row) == len(HEADERS):
                        correct = False
                except StopIteration:
                    correct = False
            if not correct:
                backup_old_file(file_path)
                create_initial_file(file_path)
        except FileNotFoundError:
            create_initial_file(file_path)

        self.file_path = file_path
