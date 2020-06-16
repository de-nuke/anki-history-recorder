import re

from anki.cards import Card
from anki.media import MediaManager
from anki.sound import SoundOrVideoTag

from .const import AUDIO_FORMATS, VIDEO_FORMATS, CARD_TYPES, TYPE_MAP, \
    QUEUE_MAP
from .html2text import HTML2Text


CLOZE = """<span class=cloze>[...]</span>"""


def is_sound(tag: SoundOrVideoTag):
    return tag.filename.rsplit(".", 1)[-1] in AUDIO_FORMATS


def is_video(tag: SoundOrVideoTag):
    return tag.filename.rsplit(".", 1)[-1] in VIDEO_FORMATS


def has_cloze(text):
    return CLOZE in text


class CardTextProcessor:
    def __init__(self, card: Card):
        self.card = card
        self.card_output = self.card.render_output()
        self.h = HTML2Text()
        self.h.unicode_snob = True
        self.h.ignore_images = True

        self.clean_question_text = None
        self.clean_answer_text = None

    def get_clean_question_text(self):
        if self.clean_question_text is None:
            self.clean_question_text = self._get_clean_text(
                self.card_output.question_text
            )
        return self.clean_question_text

    def get_clean_answer_text(self):
        if self.clean_answer_text is None:
            self.clean_answer_text = self.strip_out_question_text(
                self._get_clean_text(
                    self.card_output.answer_text
                )
            )
        return self.clean_answer_text

    def get_question_noise(self):
        original = len(self.card_output.question_text)
        clean = len(self.get_clean_question_text()) or 1
        return original / clean

    def get_answer_noise(self):
        original = len(self.card_output.answer_text)
        clean = len(self.get_clean_answer_text()) or 1
        return original / clean

    def _get_clean_text(self, text):
        text = self.h.handle(text)
        text = re.sub(r"(?i)<(br ?/?|div|p)>", " ", text)
        text = re.sub(r"\[sound:[^]]+\]", "", text)
        text = re.sub(r"\[anki:[^]]+\]", "", text)
        text = re.sub(r"\[\[type:[^]]+\]\]", "", text)
        text = re.sub(r"[ \n\t]+", " ", text)
        text = text.replace("\t", " " * 8)
        text = text.replace("\n", " ")
        text = re.sub("(?i)<style>.*?</style>", "", text)
        if '"' in text:
            text = '"' + text.replace('"', '""') + '"'
        text = re.sub(r"!\[\]\(.*\)", "", text)
        text = text.replace("* * *", "")
        text = self.strip_out_deck_name(text)
        text = text.strip()
        return text

    def strip_out_deck_name(self, text):
        deck = self.card.col.decks.get(self.card.did, default=False)
        if deck:
            deck_name = deck.get('name')
            if deck_name:
                if deck_name in text:
                    text = text.replace(deck_name, "")
                root_deck_name = deck_name.split("::")[0]
                if root_deck_name:
                    text = text.replace(root_deck_name, "")
        return text

    def strip_out_question_text(self, text):
        """Use only for answer text!"""
        clean_question = self.remove_cloze(self.get_clean_question_text())
        if clean_question in text:
            return text.replace(clean_question, "")

        # If clean question wasn't found, try to find original text
        if self.card_output.question_text in text:
            return text.replace(self.card_output.question_text, "")

        return text

    def remove_cloze(self, text):
        if has_cloze(self.card_output.question_text):
            if CLOZE in text:
                return text.replace(CLOZE, "")
            elif "[...]" in text:
                return text.replace("[...]", "")
        return text


class FeatureExtractor:
    def __init__(self, card: Card, prev_card_version: Card):
        self.card = card
        self.prev_card_version = prev_card_version
        self.card_output = self.card.render_output()
        self.note = self.card.note()
        self.card_text_processor = CardTextProcessor(self.card)

    def get_deck_name(self):
        deck = self.card.col.decks.get(self.card.did)
        if deck:
            return deck.get("name", "")
        return ""

    def card_was_new(self):
        return getattr(self.card, 'wasNew', "")

    def get_question_text(self):
        return self.card_text_processor.get_clean_question_text()

    def get_answer_text(self):
        return self.card_text_processor.get_clean_answer_text()

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
            re.compile(regexp).search(self.card_output.question_text)
            for regexp in MediaManager.imgRegexps
        )

    def answer_has_image(self):
        return any(
            re.compile(regexp).search(self.card_output.answer_text)
            for regexp in MediaManager.imgRegexps
        )

    def get_card_type(self):
        return TYPE_MAP.get(self.card.type)

    def get_prev_card_type(self):
        return TYPE_MAP.get(self.card.type)

    def get_prev_card_queue(self):
        return QUEUE_MAP.get(self.prev_card_version.queue)

    def get_card_queue(self):
        return QUEUE_MAP.get(self.card.queue)
