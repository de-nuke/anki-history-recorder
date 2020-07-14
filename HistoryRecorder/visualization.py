import json
import os
from collections import OrderedDict
from typing import Dict, List, Union

from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLabel, QListWidgetItem

from aqt.webview import AnkiWebView
from aqt import mw

from HistoryRecorder.dialog_ui import Ui_Dialog
from HistoryRecorder.storage import read_user_data

parent_dir = os.path.abspath(os.path.dirname(__file__))


class ChartWebView(AnkiWebView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mw = mw
        self.package_name = mw.addonManager.addonFromModule(__name__)
        # self.setEnabled(False)
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

    # def addDataSet(self, label: str, data_set: List[Dict[str, Union[str, int]]]):
    #     self._runJavascript(
    #         "newDataSet({})".format(json.dumps(json.dumps([label, data_set])))
    #     )
    #
    # def clearLastDataset(self):
    #     self._runJavascript("clearLastDataset()")
    #
    # def _runJavascript(self, script: str):
    #     # workaround for widget focus stealing issues
    #     self.setEnabled(False)
    #     self.evalWithCallback(script, self.__onJavascriptEvaluated)
    #
    # def __onJavascriptEvaluated(self, *args):
    #     self.setEnabled(True)


class GraphDialog(Ui_Dialog, QDialog):
    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.setupUi(self)

        self._load_user_sessions()

    def _load_user_sessions(self):
        user_data = read_user_data()
        for data in user_data:
            print(data)
        self.session_list_widget.itemClicked.connect(self.change_session)

    def change_session(self, item):
        print(item)


def show_graph_dialog():
    dialog = GraphDialog()
    dialog.exec_()
