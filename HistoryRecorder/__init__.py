from anki.hooks import wrap
from aqt.reviewer import Reviewer
from aqt import gui_hooks

from .session import session


def did_answer_card(reviewer, card, ease):
    session.save_answer(reviewer, card, ease)


def start_session(self):
    session.start()


def stop_session():
    session.stop()


Reviewer.show = wrap(Reviewer.show, start_session)
gui_hooks.reviewer_will_end.append(stop_session)
gui_hooks.reviewer_did_answer_card.append(did_answer_card)
