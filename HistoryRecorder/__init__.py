from anki.cards import Card
from anki.hooks import wrap
from aqt.reviewer import Reviewer
from aqt import gui_hooks

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


Reviewer.show = wrap(Reviewer.show, start_session)
gui_hooks.reviewer_will_end.append(stop_session)
gui_hooks.reviewer_did_answer_card.append(did_answer_card)
gui_hooks.card_will_show.append(card_will_show)
gui_hooks.reviewer_did_show_answer.append(did_show_answer)
