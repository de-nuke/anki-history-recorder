from PyQt5 import QtWidgets
from anki.cards import Card
from anki.hooks import wrap
from aqt.reviewer import Reviewer, ReviewerBottomBar
from aqt import gui_hooks, mw, qconnect
from aqt.webview import WebContent

from .contrib import open_files_folder, show_files_choice_window, \
    open_upload_page
from .gui import RecorderMenu
from .recorder import recorder
from .utils import get_config

mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")


def did_answer_card(reviewer, card, ease):
    recorder.save_answer(reviewer, card, ease)


def did_show_answer(card):
    recorder.save_answer_shown(card)


def card_will_show(text: str, card: Card, kind: str) -> str:
    return recorder.before_card_show(text, card, kind)


def start_recorder(self):
    recorder.start()


def stop_recorder():
    recorder.stop()


def will_set_content(web_content: WebContent, context):
    config = get_config()
    if isinstance(context, ReviewerBottomBar) and config.get("display-status"):
        status_indicator = recorder.gui.status_indicator
        web_content.js.extend(status_indicator.get_js())
        web_content.css.extend(status_indicator.get_css())
        web_content.body += status_indicator.get_body()


def webhook_did_receive_js_message(handled, message, context):
    if message == "recorder_status_changed":
        recorder.gui.toggle_recorder_enabled()
        return True, None
    return handled


recorder.setup_gui()

Reviewer.show = wrap(Reviewer.show, start_recorder)
gui_hooks.reviewer_will_end.append(stop_recorder)
gui_hooks.reviewer_did_answer_card.append(did_answer_card)
gui_hooks.card_will_show.append(card_will_show)
gui_hooks.reviewer_did_show_answer.append(did_show_answer)
gui_hooks.webview_will_set_content.append(will_set_content)
gui_hooks.webview_did_receive_js_message.append(webhook_did_receive_js_message)
