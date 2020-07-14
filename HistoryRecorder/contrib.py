import os
import platform
import subprocess
import webbrowser
from pathlib import Path
from typing import Iterable, Union, Callable

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from .const import UPLOAD_HOST, UPLOAD_PATH, FIELD_NAME, USER_FILES_DIR, \
    RECORDS_PATH
from .http_helper import post_file, server_test, post_records

FULL_PATH_USER_FILES_DIR = os.path.abspath(USER_FILES_DIR)
EXCLUDED_FILES = [".gitkeep"]
WidgetOrWidgets = Union[Iterable[QtWidgets.QWidget], QtWidgets.QWidget]


def open_folder(path: str):
    """Open a directory specified by path in a system's default explorer"""
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def show_message_box(
        text_main: str,
        text_info: str = None,
        on_close_callback: Callable = None
):
    """Show message box with "Close" button"""
    msg_box = QtWidgets.QMessageBox()
    msg_box.setText(text_main)
    if text_info:
        msg_box.setInformativeText(text_info)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Close)
    msg_box.exec_()

    if on_close_callback:
        on_close_callback()


def open_files_folder():
    try:
        open_folder(FULL_PATH_USER_FILES_DIR)
    except Exception:
        show_message_box(
            "There was a problem opening a files directory.",
            f"""
            <p>You can manually go to the directory:<p>
            <p>{FULL_PATH_USER_FILES_DIR}<p>
            """
        )


def get_filename(path: str) -> str:
    """Get file name from path"""
    return Path(path).name


def detect_user_files() -> list:
    """Detect all files in "user_files" folder"""
    (_, _, filenames) = next(os.walk(FULL_PATH_USER_FILES_DIR))
    return filenames


def abs_path(filename):
    """Get absolute path for a file"""
    return os.path.join(FULL_PATH_USER_FILES_DIR, filename)


def set_margin(widgets: WidgetOrWidgets, where: str, pixels: int):
    """Set widget's margin"""
    if not isinstance(widgets, Iterable):
        widgets = [widgets]
    for widget in widgets:
        name = widget.__class__.__name__
        widget.setStyleSheet(f"{name} {{margin-{where}: {pixels}px}}")


def progress_msg(uploaded: int, total: int) -> str:
    """Construct an info message about upload progress"""
    return f"Uploading {total} files... ({uploaded}/{total})"


class FilesSender(QThread):
    """
    Send files to the server.
    """
    submitted = pyqtSignal(int, int, str, int, str)
    finished = pyqtSignal()

    def __init__(self, paths_to_files, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paths_to_files = paths_to_files

    def run(self):
        files_submitted = 0
        for path in self.paths_to_files:
            with open(path, encoding='utf-8') as f:
                response = post_file(UPLOAD_HOST, UPLOAD_PATH, FIELD_NAME, f)
            files_submitted += 1
            self.submitted.emit(
                files_submitted,
                len(self.paths_to_files),
                get_filename(path),
                response.status,
                response.read().decode("utf-8")
            )
        self.finished.emit()


class ServerTest(QThread):
    """Run a request to check server availability"""
    available = pyqtSignal(str)
    not_available = pyqtSignal(str)

    def run(self):
        is_available, message = server_test(UPLOAD_HOST)
        if is_available:
            self.available.emit(message)
        else:
            self.not_available.emit(message)


class SubmitFilesDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        """Initialize Dialog window. Add all needed widgets"""
        super().__init__(*args, **kwargs)
        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.title_label = QtWidgets.QLabel(self)
        self.button_box = QtWidgets.QDialogButtonBox()
        self.btn_cancel, self.btn_accept = None, None
        self.list_view = QtWidgets.QListView()
        self.pb = QtWidgets.QProgressBar()
        self.list_model = QStandardItemModel()
        self.upload_progress_label = QtWidgets.QLabel()
        self.checkboxes = {}
        self.loading_msg_label = QtWidgets.QLabel(
            "Checking server availability... Please wait"
        )
        self.loading_msg_label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.loading_msg_label.setAlignment(Qt.AlignCenter)
        self.loading_pb = QtWidgets.QProgressBar()
        self.loading_pb.setMaximum(0)
        self.v_layout.addWidget(self.loading_msg_label)
        self.v_layout.addWidget(self.loading_pb)

        self.server_tester = ServerTest()
        self.server_tester.available.connect(self.on_server_available)
        self.server_tester.not_available.connect(self.on_server_not_available)
        self.server_tester.start()

        self.files_sender = None

    def on_server_not_available(self, msg: str):
        show_message_box(
            "Sorry, the server is not available at the moment",
            f"Error details: {msg}",
            on_close_callback=self.reject
        )

    def on_server_available(self, msg):
        self.v_layout.removeWidget(self.loading_pb)
        self.loading_pb.deleteLater()
        self.loading_pb = None
        self.loading_msg_label.setText(msg)
        self.loading_msg_label.setStyleSheet("""
        QLabel {
            color: green; 
            font-style: italic;
            margin-top: -5px;
            margin-bottom: 10px;
        }
        """)
        self.init_ui()

    def init_ui(self):
        """Initialize and show widgets"""
        self.title_label.setText("Select files to submit")
        self.title_label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.title_label.setAlignment(Qt.AlignCenter)
        set_margin(self.title_label, 'bottom', 10)

        checkboxes_grid = QtWidgets.QGridLayout()
        files = detect_user_files()

        for filename in files:
            if filename not in EXCLUDED_FILES:
                checkbox = QtWidgets.QCheckBox(filename, self)
                self.checkboxes[abs_path(filename)] = checkbox

        for i, checkbox in enumerate(self.checkboxes.values()):
            row = i % 5
            column = i // 5
            checkboxes_grid.addWidget(checkbox, row, column)
            checkbox.toggled.connect(self.toggle_submit)

        self.button_box.addButton("Cancel", self.button_box.RejectRole)
        self.button_box.addButton("Submit", self.button_box.AcceptRole)

        self.btn_cancel, self.btn_accept = \
            self.button_box.findChildren(QtWidgets.QPushButton)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_accept.clicked.connect(self.on_submit)
        self.btn_accept.setEnabled(False)
        self.button_box.setCenterButtons(True)
        set_margin([self.btn_accept, self.btn_cancel], 'top', 20)

        self.v_layout.addWidget(self.title_label)
        self.v_layout.addLayout(checkboxes_grid)
        self.v_layout.addWidget(self.button_box)
        self.v_layout.setContentsMargins(20, 20, 20, 20)
        self.setWindowModality(Qt.ApplicationModal)

        self.list_view.setEditTriggers(self.list_view.NoEditTriggers)
        self.list_view.setModel(self.list_model)

    def toggle_submit(self):
        """
        Set "Submit" button enabled only when at least one checkbox is checked
        """
        is_enabled = any(
            checkbox.isChecked() for checkbox in self.checkboxes.values()
        )
        self.btn_accept.setEnabled(is_enabled)

    def on_submit(self):
        """Slot to perform some actions after "Submit" button is clicked"""
        self.btn_accept.setEnabled(False)

        # 1. Collect selected files
        files_to_submit = []
        for filename, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                files_to_submit.append(filename)

        n_files = len(files_to_submit)

        # 2. Set initial values for progress bar
        self.pb.setMaximum(n_files)
        self.pb.setValue(0)

        # 3. Set initial message
        self.upload_progress_label.setText(progress_msg(0, n_files))
        set_margin(self.upload_progress_label, 'top', 10)

        # 4. Add progress bar, list view and message label to the layout
        layout = self.layout()
        pos = layout.count() - 1
        layout.insertWidget(pos, self.upload_progress_label)
        layout.insertWidget(pos+1, self.pb)
        layout.insertWidget(pos+2, self.list_view)
        self.upload_progress_label.show()
        self.pb.show()

        # 5. Start a Thread which sends files and connect slots it its signals
        self.files_sender = FilesSender(files_to_submit)
        self.files_sender.submitted.connect(self.on_file_submitted)
        self.files_sender.finished.connect(self.on_sending_finished)
        self.files_sender.start()

    def on_file_submitted(
            self, i: int, total: int, filename: str, status: int, msg: str
    ):
        """Update progress information when single file is sent"""
        # 1. Update progress bar
        self.pb.setValue(i)

        # 2. Update List View
        text = f"{status} {msg} ({filename})"
        idx = self.list_model.rowCount()
        item = QStandardItem()
        color = Qt.darkGreen if status // 100 == 2 else Qt.darkRed
        item.setForeground(color)
        item.setText(text)
        self.list_model.setItem(idx, item)

        # 3. Update message
        self.upload_progress_label.setText(progress_msg(i, total))

    def on_sending_finished(self):
        """Slot called when all files are sent"""
        self.btn_cancel.setText("Close")


def show_files_choice_window():
    dialog = SubmitFilesDialog()
    dialog.exec_()


def open_upload_page():
    webbrowser.open(UPLOAD_HOST)


class RecordsSender(QThread):
    started = pyqtSignal()
    finished = pyqtSignal(bool)

    def __init__(self, records, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = records

    def run(self):
        self.started.emit()
        succeeded = False
        try:
            response = post_records(UPLOAD_HOST, RECORDS_PATH, self.records)
            succeeded = response.status == 200
        except Exception as e:
            pass
        self.finished.emit(succeeded)


# On startup, fire a simple request to the server to wake it up
s = ServerTest()
s.start()
