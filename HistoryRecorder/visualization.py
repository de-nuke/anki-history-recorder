import json
import os
import re
from collections import defaultdict, Counter
from csv import DictReader
from operator import itemgetter
from typing import Dict, List

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QSizePolicy, QMessageBox

from aqt.webview import AnkiWebView
from aqt import mw

from .utils import get_config
from . import stopwords
from .storage import get_file_path
from .dialog_ui import Ui_Dialog

parent_dir = os.path.abspath(os.path.dirname(__file__))


WORD_CLOUD = "word_cloud"
ANSWERED_CARDS_CLOCK = "answered_cards_clock"


def show_message_box(
    text_main: str,
    text_info: str = None,
):
    """Show message box with "Close" button"""
    msg_box = QMessageBox()
    msg_box.setText(text_main)
    if text_info:
        msg_box.setInformativeText(text_info)
    msg_box.setStandardButtons(QMessageBox.Close)
    msg_box.exec_()


class ChartWebView(AnkiWebView):
    """
    Webview displaying graphs and some info.

    Handles rendering HTML and execution of Javascript code.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mw = mw
        self.package_name = mw.addonManager.addonFromModule(__name__)
        self.setEnabled(False)
        self.init_view()

    def init_view(self):
        """Read HTML file and set it on the page."""
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
        """
        Based on given graph type, run appropriate JS function to draw graphs.
        """
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
    """Main dialog window that is a container for webview.

    This class keeps all the logic for generating data
    """
    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.setupUi(self)
        self.webview = ChartWebView()
        self.horizontalLayout.addWidget(self.webview)
        self.webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.config = get_config()

        self.webview.loadFinished.connect(self.display_data)

    def display_data(self):
        """
        Callback run after webview is loaded. Displays generated data summary
        """
        data_file_is_valid = self.check_file()
        if not data_file_is_valid:
            return

        self.webview.visualizeData(WORD_CLOUD, self.get_word_cloud_data())
        self.webview.visualizeData(
            ANSWERED_CARDS_CLOCK, self.get_answered_cards_clock_data()
        )

    def get_word_cloud_data(self) -> List[Dict]:
        """Get most frequent words from answers"""
        data = self.get_data()
        answers = map(itemgetter('answer'), data)
        words = defaultdict(int)

        for answer in answers:
            for w in answer.split():
                clean = self.clean_word(w)
                if not clean:
                    continue

                words[clean] += 1

        return [
            {"x": key, "value": value, "category": None}
            for i, (key, value)
            in
            enumerate(sorted(words.items(), key=lambda x: -x[1]))
            if i < 50
        ]

    def clean_word(self, word: str) -> str:
        """
        Clean word by removing punctuation and stopwords and making it lowercase
        """
        kill_punctuation = str.maketrans('', '', r"-()\"#/@;:<>{}-=~|.?,*_")
        clean_word = word.translate(kill_punctuation).lower()
        hide_stopwords = self.config.get('hide-stopwords')
        if isinstance(hide_stopwords, list):
            excluded_words = stopwords.get_words(languages=hide_stopwords)
        else:
            if hide_stopwords:
                excluded_words = stopwords.get_words()
            else:
                excluded_words = {}
        if clean_word not in excluded_words:
            return clean_word
        else:
            return ''

    def get_answered_cards_clock_data(self) -> Dict:
        """Get how many cards were answered in total per each hour in a day"""
        answered_at_re = re.compile(
            r"\d{2}-\d{2}-\d{4}\ (?P<hour>\d{2}):\d{2}:\d{2}"
        )

        def get_hour(row):
            match = answered_at_re.match(row.get('answered_at', ''))
            if match:
                return int(match.groupdict()['hour'])
            return None

        data = self.get_data()
        hours = filter(lambda h: h is not None, map(get_hour, data))
        counted_hours = Counter(hours)

        for i in range(0, 24):
            if i not in counted_hours:
                counted_hours[i] = 0

        return {
            'labels': list(range(0, 24)),
            'label': "Learning clock",
            'data': [
                count
                for hour, count
                in sorted(counted_hours.items(), key=itemgetter(0))
            ]
        }

    def get_data(self):
        with open(get_file_path(), 'r', encoding='utf-8') as f:
            reader = DictReader(f)
            for row in reader:
                yield row

    def check_file(self) -> bool:
        """Check if file exists and if it contains data"""
        try:
            with open(get_file_path(), 'r', encoding='utf-8') as f:
                reader = DictReader(f)
                try:
                    next(reader)
                except StopIteration:
                    show_message_box(
                        "Your history is empty, there's no data to summarise",
                        "Answer some cards to generate new records"
                    )
                    self.close()
                    return False

        except FileNotFoundError:
            show_message_box(
                "History file doesn't exist for your profile",
                "Answer some cards (with saving records enabled) to generate "
                "the file."
            )
            self.close()
            return False
        else:
            return True


def show_graph_dialog():
    dialog = GraphDialog()
    dialog.exec_()
