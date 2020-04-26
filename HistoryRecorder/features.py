import re

from anki.cards import Card
from anki.media import MediaManager
from anki.sound import SoundOrVideoTag

from .const import AUDIO_FORMATS, VIDEO_FORMATS
from .html2text import HTML2Text


def is_sound(tag: SoundOrVideoTag):
    return tag.filename.rsplit(".", 1)[-1] in AUDIO_FORMATS


def is_video(tag: SoundOrVideoTag):
    return tag.filename.rsplit(".", 1)[-1] in VIDEO_FORMATS


class FeatureExtractor:
    def __init__(self, card: Card):
        self.card = card
        self.card_output = self.card.render_output()
        self.note = self.card.note()
        self.h = HTML2Text()
        self.h.unicode_snob = True

    def get_category(self):
        return ''

    def get_deck_category(self):
        return ''

    def get_question_text(self):
        return self.h.handle(self.card_output.question_text)

    def get_answer_text(self):
        return self.h.handle(self.card_output.answer_text)

    def question_has_sound(self):
        try:
            next(filter(is_sound, self.card.question_av_tags()))
        except StopIteration:
            # not found
            return False
        else:
            # found
            return True

    def answer_has_sound(self):
        try:
            next(filter(is_sound, self.card.answer_av_tags()))
        except StopIteration:
            # not found
            return False
        else:
            # found
            return True

    def question_has_video(self):
        try:
            next(filter(is_video, self.card.question_av_tags()))
        except StopIteration:
            # not found
            return False
        else:
            # found
            return True

    def answer_has_video(self):
        try:
            next(filter(is_video, self.card.answer_av_tags()))
        except StopIteration:
            # not found
            return False
        else:
            # found
            return True

    def question_has_image(self):
        return any(
            re.compile(regexp).match(self.card_output.question_text)
            for regexp in MediaManager.imgRegexps
        )

    def answer_has_image(self):
        return any(
            re.compile(regexp).match(self.card_output.answer_text)
            for regexp in MediaManager.imgRegexps
        )
