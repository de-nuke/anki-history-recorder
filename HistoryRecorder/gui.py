from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QMenu,
    QAction
)
from aqt import mw, qconnect

from HistoryRecorder.contrib import open_files_folder, show_files_choice_window, \
    open_upload_page


class RecorderMenu(QMenu):

    on_off_toggled = pyqtSignal()

    def __init__(self, *args, recorder, **kwargs):
        self.recorder = recorder
        super().__init__(*args, **kwargs)
        self.setTitle("History Recorder")

        # Create actions
        self.open_dir_action = QAction("Open files folder", mw)
        self.open_browser_action = QAction("Open upload form in browser", mw)
        self.submit_history_action = QAction("Submit history...", mw)
        self.on_off_action = QAction("Turn off", mw)

        # Add to self
        self.addAction(self.on_off_action)
        self.addAction(self.open_dir_action)
        self.addAction(self.open_browser_action)
        self.addAction(self.submit_history_action)

        # Connect actions signals to slots
        qconnect(self.open_dir_action.triggered, open_files_folder)
        qconnect(self.submit_history_action.triggered, show_files_choice_window)
        qconnect(self.open_browser_action.triggered, open_upload_page)
        qconnect(self.on_off_action.triggered, self.on_off_toggled.emit)

    def change_on_off_text(self, is_enabled):
        if is_enabled:
            self.on_off_action.setText("Turn off")
        else:
            self.on_off_action.setText("Turn on")


class StatusIndicator:
    template = """
    <div id="history-recorder-status">
        <span class="text {on_off_class}">{label}</span>
        <label class="history-recorder-switch">
            <input type="checkbox" {checked} id="history-recorder-checkbox">
            <span class="slider round"></span>
        </label>
    </div>
    """

    def __init__(self, recorder):
        self.addon_package = mw.addonManager.addonFromModule(__name__)
        self.recorder = recorder

    def get_js(self):
        return [
            f"/_addons/{self.addon_package}/web/script.js"
        ]

    def get_css(self):
        return [
            f"/_addons/{self.addon_package}/web/style.css"
        ]

    def get_body(self):
        return self.template.format(
            checked="checked" if self.recorder.enabled else "",
            label="Your answers are being recorded"
            if self.recorder.enabled else "Answer recording is stopped",
            on_off_class="on" if self.recorder.enabled else "off"
        )

    def update_status(self, is_enabled: bool):
        enabled = "true" if is_enabled else "false"
        mw.reviewer.bottom.web.eval(f"setRecorderEnabled({enabled})")


class GUIManager:
    def __init__(self):
        self.recorder = None
        self.recorder_menu = None
        self.status_indicator = None

    def setup(self, recorder):
        self.recorder = recorder
        self.recorder_menu = RecorderMenu(mw.form.menuTools, recorder=recorder)
        self.status_indicator = StatusIndicator(recorder=recorder)
        mw.form.menuTools.addMenu(self.recorder_menu)
        self.recorder_menu.on_off_toggled.connect(self.toggle_recorder_enabled)

    def toggle_recorder_enabled(self):
        is_enabled = self.recorder.toggle_on_off()
        self.recorder_menu.change_on_off_text(is_enabled)
        self.status_indicator.update_status(is_enabled)
