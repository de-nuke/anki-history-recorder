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
        print(features)
        print(features.keys())

    def get_answer_features(self, card: Card, ease: int):
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
            'question_has_sound': features.question_has_sound(),
            'answer_has_sound': features.answer_has_sound(),
            'question_has_video': features.question_has_video(),
            'answer_has_video': features.answer_has_video(),
            'question_has_image': features.question_has_image(),
            'answer_has_image': features.answer_has_image(),
            'ease': ease,
            'type': card.type,
            'queue': card.queue,
            'due': card.due,
            'interval': card.ivl,
            'answered_at': self.last_answer,
            'think_time': card.timeTaken(),
            'grade_time': self.last_answer - self.answer_shown_at,
            'total_study_time': self.last_answer - self.start_time,
            'ESTIMATED_INTERVAL': None  # Don't know how to get it
        }


# Init global session object
session = Session()
