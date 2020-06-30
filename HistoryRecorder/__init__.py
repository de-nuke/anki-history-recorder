from PyQt5 import QtWidgets
from anki.cards import Card
from anki.hooks import wrap
from aqt.reviewer import Reviewer
from aqt import gui_hooks, mw, qconnect

from .contrib import open_files_folder, show_files_choice_window, \
    open_upload_page
from .session import session


def did_answer_card(reviewer, card, ease):
    session.save_answer(reviewer, card, ease)


def did_show_answer(card):
    session.save_answer_shown(card)


def card_will_show(text: str, card: Card, kind: str) -> str:
    return session.before_card_show(text, card, kind)


def start_session(self):
    session.start()


def stop_session():
    session.stop()


def add_menu_actions():
    open_dir_action = QtWidgets.QAction(mw)
    submit_history_action = QtWidgets.QAction(mw)
    open_browser_action = QtWidgets.QAction(mw)
    open_dir_action.setText("Open files folder")
    open_browser_action.setText("Open upload form in browser")
    submit_history_action.setText("Submit history...")
    submenu = mw.form.menuTools.addMenu("History recorder")
    submenu.addAction(open_dir_action)
    submenu.addAction(open_browser_action)
    submenu.addAction(submit_history_action)
    qconnect(open_dir_action.triggered, open_files_folder)
    qconnect(submit_history_action.triggered, show_files_choice_window)
    qconnect(open_browser_action.triggered, open_upload_page)


Reviewer.show = wrap(Reviewer.show, start_session)
gui_hooks.reviewer_will_end.append(stop_session)
gui_hooks.reviewer_did_answer_card.append(did_answer_card)
gui_hooks.card_will_show.append(card_will_show)
gui_hooks.reviewer_did_show_answer.append(did_show_answer)

add_menu_actions()
