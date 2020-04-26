import time
from dataclasses import dataclass, fields
from typing import Optional

from anki.cards import Card
from aqt.reviewer import Reviewer
from aqt import mw

from HistoryRecorder.features import FeatureExtractor


@dataclass
class Session:
    answer_shown_at: float = 0
    last_answer: float = 0
    last_duration: float = 0
    sid: Optional[int] = None
    start_time: Optional[float] = None

    def start(self):
        self.reset()
        self.start_time = time.time()

    def reset(self):
        for field in fields(self):
            print(field)

    def stop(self):
        self.last_duration = time.time() - self.start_time
        self.start_time = None

    def save_answer_shown(self):
        self.answer_shown_at = time.time()

    def save_answer(self, reviewer: Reviewer, card: Card, ease: int):
        self.last_answer = time.time()
        features = self.get_answer_features(card, ease)

    def get_answer_features(self, card: Card, ease: int):
        HEADERS = ['uid', 'sid', 'card_id', 'deck_id', 'card_cat', 'deck_cat',
                   'question', 'answer', 'ease', 'maturity', 'last_shown',
                   'answered_at', 'think_time', 'grade_time', 'has_image',
                   'has_sound',
                   'total_study_time', 'ESTIMATED_INTERVAL']
        features = FeatureExtractor(card)
        return {
            'uid': mw.pm.meta.get('id'),
            'sid': self.sid,
            'card_id': card.id,
            'deck_id': card.did,
            'card_cat': features.get_category(),
            'deck_cat': features.get_deck_category(),
            'question': features.get_question_text(),
            'answer': features.get_answer_text(),
            'ease': ease,
            'type': card.type,
            'queue': card.queue,
            'due': card.due,
            'interval': card.ivl,
            'last_shown': ...,
            'answered_at': self.last_answer,
            'think_time': card.timeTaken(),
            'grade_time': self.last_answer - self.answer_shown_at,
        }


# Init global session object
session = Session()
