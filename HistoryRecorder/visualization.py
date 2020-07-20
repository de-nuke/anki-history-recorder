import json
import os
import random

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QSizePolicy

from aqt.webview import AnkiWebView
from aqt import mw

from HistoryRecorder.dialog_ui import Ui_Dialog

parent_dir = os.path.abspath(os.path.dirname(__file__))


WORD_CLOUD = "word_cloud"
ANSWERED_CARDS_CLOCK = "answered_cards_clock"


class ChartWebView(AnkiWebView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mw = mw
        self.package_name = mw.addonManager.addonFromModule(__name__)
        self.setEnabled(False)
        self.init_view()

    def init_view(self):
        base_url = QUrl(
            f"http://localhost:{self._mw.mediaServer.getPort()}/"
            f"_addons/{self.package_name}/web/visualization/graph.html"
        )

        html_path = os.path.join(
            parent_dir, "web", "visualization", "graph.html"
        )
        with open(html_path, "r", encoding='utf-8') as f:
            html = f.read()

        QWebEngineView.setHtml(self, html, baseUrl=base_url)

    def visualizeData(self, data_type, data):
        if data_type == WORD_CLOUD:
            function = "createWordCloud"
        elif data_type == ANSWERED_CARDS_CLOCK:
            function = "createAnswersClock"
        else:
            function = "console.log"

        cmd = f"{function}({json.dumps(data)})"
        self._run_javascript(cmd)

    def _run_javascript(self, script: str):
        self.setEnabled(False)
        self.evalWithCallback(script, self._on_javascript_evaluated)

    def _on_javascript_evaluated(self, *args):
        self.setEnabled(True)


class GraphDialog(Ui_Dialog, QDialog):
    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.setupUi(self)
        self.webview = ChartWebView()
        self.horizontalLayout.addWidget(self.webview)
        self.webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.webview.loadFinished.connect(self.display_data)

    def display_data(self):
        self.webview.visualizeData(
            WORD_CLOUD,
            [
                # {"x": "English", "value": 983000000, "category": None},
                # {"x": "Hindustani", "value": 544000000, "category": None},
                # {"x": "Spanish", "value": 527000000, "category": None},
                # {"x": "Arabic", "value": 422000000, "category": None},
                # {"x": "Malay", "value": 281000000, "category": None},
                # {"x": "Russian", "value": 267000000, "category": None},
                # {"x": "Bengali", "value": 261000000, "category": None},
                # {"x": "Portuguese", "value": 229000000, "category": None},
                # {"x": "French", "value": 229000000, "category": None},
                # {"x": "Hausa", "value": 150000000, "category": None},
                # {"x": "Punjabi", "value": 148000000, "category": None},
                # {"x": "Japanese", "value": 129000000, "category": None},
                # {"x": "German", "value": 129000000, "category": None},
                # {"x": "Persian", "value": 121000000, "category": None},

                {"x": "English", "value": 983000000},
                {"x": "Hindustani", "value": 544000000},
                {"x": "Spanish", "value": 527000000},
                {"x": "Arabic", "value": 422000000},
                {"x": "Malay", "value": 281000000},
                {"x": "Russian", "value": 267000000},
                {"x": "Bengali", "value": 261000000},
                {"x": "Portuguese", "value": 229000000},
                {"x": "French", "value": 229000000},
                {"x": "Hausa", "value": 150000000},
                {"x": "Punjabi", "value": 148000000},
                {"x": "Japanese", "value": 129000000},
                {"x": "German", "value": 129000000},
                {"x": "Persian", "value": 121000000}
            ]
        )
        self.webview.visualizeData(
            ANSWERED_CARDS_CLOCK,
            {
                'labels': list(range(0, 24)),
                'label': "Learning clock",
                'data': [random.randrange(0, 40) for _ in range(0, 24)]

            }
        )


def show_graph_dialog():
    dialog = GraphDialog()
    dialog.exec_()
