from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QMenu,
    QAction
)
from aqt import mw, qconnect

from .contrib import open_files_folder, show_files_choice_window, \
    open_upload_page
from .visualization import show_graph_dialog


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
        text = "Turn off" if recorder.enabled else "Turn on"
        self.on_off_action = QAction(text, mw)
        self.show_graphs = QAction("Show summary", mw)

        # Add to self
        self.addAction(self.on_off_action)
        self.addAction(self.open_dir_action)
        self.addAction(self.open_browser_action)
        self.addAction(self.submit_history_action)
        self.addAction(self.show_graphs)

        # Connect actions signals to slots
        qconnect(self.open_dir_action.triggered, open_files_folder)
        qconnect(self.submit_history_action.triggered, show_files_choice_window)
        qconnect(self.open_browser_action.triggered, open_upload_page)
        qconnect(self.on_off_action.triggered, self.on_off_toggled.emit)
        qconnect(self.show_graphs.triggered, show_graph_dialog)

    def change_on_off_text(self, is_enabled):
        if is_enabled:
            self.on_off_action.setText("Turn off")
        else:
            self.on_off_action.setText("Turn on")


class StatusIndicator:
    template = """
    <div id="history-recorder-status">
        <span id="saving-info" class="hidden">saving... </span>
        <label class="history-recorder-switch">
            <input type="checkbox" {checked} id="history-recorder-checkbox">
            <span class="slider round"></span>
        </label>
        <span class="text {on_off_class}">{label}</span>
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
        on = self.recorder.enabled
        return self.template.format(
            checked="checked" if on else "",
            label="Saving answers: ON" if on else "Saving answers: OFF",
            on_off_class="on" if on else "off"
        )

    def update_status(self, is_enabled: bool):
        enabled = "true" if is_enabled else "false"
        mw.reviewer.bottom.web.eval(f"setRecorderEnabled({enabled})")

    def show_sending_loader(self):
        # I have to check if function is defined, because when learning is
        # finished, the screen changes, so all JS structures defined in
        # previous webview are removed. The last execution of this function
        # is preformed after screen change, and would try to call non-existing
        # showSendingLoader function.
        def exec_func(function_exists: bool):
            if function_exists:
                mw.reviewer.bottom.web.eval(f"showSendingLoader()")

        mw.reviewer.bottom.web.evalWithCallback(
            "typeof showSendingLoader !== 'undefined'", exec_func
        )

    def hide_sending_loader(self):
        # I have to check if function is defined, because when learning is
        # finished, the screen changes, so all JS structures defined in
        # previous webview are removed. The last execution of this function
        # is preformed after screen change, and would try to call non-existing
        # hideSendingLoader function.
        def exec_func(function_exists: bool):
            if function_exists:
                mw.reviewer.bottom.web.eval(f"hideSendingLoader()")

        mw.reviewer.bottom.web.evalWithCallback(
            "typeof hideSendingLoader !== 'undefined'", exec_func
        )


class GUIManager:
    """
    Class responsible for communication between menu actions and status bar
    """
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

    def record_sending_started(self):
        self.status_indicator.show_sending_loader()

    def record_sending_finished(self, is_success):
        self.status_indicator.hide_sending_loader()
