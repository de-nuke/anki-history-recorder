import random
import time
from copy import copy
from dataclasses import dataclass, fields
from typing import Optional

from anki.cards import Card
from aqt.reviewer import Reviewer
from aqt import mw

from .const import ANSWERED_AT_FMT
from .features import FeatureExtractor
from .gui import GUIManager
from .storage import RemoteStorage, LocalStorage
from .utils import get_config


config = get_config()


@dataclass
class Recorder:
    answer_shown_at: float = 0
    answered_at: float = 0
    last_duration: float = 0
    sid: Optional[int] = None
    start_time: Optional[float] = None
    local_storage: LocalStorage = None
    remote_storage: RemoteStorage = None
    gui: GUIManager = None
    prev_card_version: Card = None
    enabled: bool = True

    exclude_reset = {
        'local_storage', 'sid', 'remote_storage', 'gui', 'enabled'
    }

    def start(self):
        self.reset()
        self.start_time = time.time()
        self.local_storage.init_storage()
        self.remote_storage.init_storage()
        self.remote_storage.on_started(self.gui.record_sending_started)
        self.remote_storage.on_finished(self.gui.record_sending_finished)

    def setup_gui(self):
        self.gui.setup(recorder=self)

    def toggle_on_off(self):
        self.enabled = not self.enabled
        return self.enabled

    def reset(self):
        for field in fields(self):
            if field.name not in self.exclude_reset:
                setattr(self, field.name, field.default)

    def stop(self):
        self.last_duration = time.time() - self.start_time
        self.start_time = None

    def save_answer_shown(self, card):
        self.answer_shown_at = time.time()

    def save_answer(self, reviewer: Reviewer, card: Card, ease: int):
        if self.enabled:
            self.answered_at = time.time()
            features = self.get_answer_features(card, ease)
            self.local_storage.save(features)
            if bool(config.get("live-sync")):
                self.remote_storage.save(features)

    def before_card_show(self, text: str, card: Card, kind: str) -> str:
        self.prev_card_version = copy(card)
        return text

    def get_answer_features(self, card: Card, ease: int):
        features = FeatureExtractor(card, self.prev_card_version)
        return {
            # 'uid': mw.pm.meta.get('id'),
            'sid': self.sid,
            'timestamp': time.time(),
            # 'card_id': card.id,
            # 'deck_id': card.did,
            'deck_name': features.get_deck_name(),
            'question': features.get_question_text(),
            'answer': features.get_answer_text(),
            'question_fields': features.get_question_fields(),
            'answer_fields': features.get_answer_fields(),
            'note_type': features.get_note_type(),
            'model_type': features.model_type(),
            'question_has_cloze': features.has_cloze(),
            'question_has_type_in': features.has_type_in(),
            'question_has_type_in_cloze': features.has_type_in_cloze(),
            'question_has_sound': features.question_has_sound(),
            'answer_has_sound': features.answer_has_sound(),
            'question_has_video': features.question_has_video(),
            'answer_has_video': features.answer_has_video(),
            'question_has_image': features.question_has_image(),
            'answer_has_image': features.answer_has_image(),
            'ease': ease,
            'type': features.get_prev_card_type(),
            'new_type': features.get_card_type(),
            'queue': features.get_prev_card_queue(),
            'new_queue': features.get_card_queue(),
            'due': card.due,
            'last_interval': features.get_last_interval(),
            'reps': card.reps,
            'answered_at': time.strftime(
                ANSWERED_AT_FMT,
                time.localtime(self.answered_at)
            ),
            'time_taken': card.timeTaken(),
            'grade_time': self.answered_at - self.answer_shown_at,
            'total_study_time': self.answered_at - self.start_time,
            'ESTIMATED_INTERVAL': features.get_estimated_interval()
        }


# Init global session object
recorder = Recorder(
    local_storage=LocalStorage(),
    remote_storage=RemoteStorage(),
    gui=GUIManager(),
    sid=random.random(),
    enabled=bool(config.get("enabled-by-default", False))
)
