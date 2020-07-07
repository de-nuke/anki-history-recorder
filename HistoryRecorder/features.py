import re
from typing import Iterable, OrderedDict

from anki.cards import Card
from anki.media import MediaManager
from anki.sound import SoundOrVideoTag

from .const import AUDIO_FORMATS, VIDEO_FORMATS, TYPE_MAP, \
    QUEUE_MAP, MODEL_TYPES_MAP
from .html2text import HTML2Text


CLOZE = """<span class=cloze>[...]</span>"""
field_name_regex = re.compile(r"\{\{(?P<field_name>[^}]+)}}")


def is_sound(tag: SoundOrVideoTag) -> bool:
    return tag.filename.rsplit(".", 1)[-1] in AUDIO_FORMATS


def is_video(tag: SoundOrVideoTag) -> bool:
    return tag.filename.rsplit(".", 1)[-1] in VIDEO_FORMATS


def has_cloze(text: str) -> bool:
    return CLOZE in text


def remove_duplicates(sequence: Iterable) -> list:
    return list(OrderedDict.fromkeys(sequence))


class CardTextProcessor:
    def __init__(self, card: Card):
        self.card = card
        self.card_output = self.card.render_output()
        self.h = HTML2Text()
        self.h.unicode_snob = True
        self.h.ignore_images = True

        self._clean_texts = None

    def get_clean_question_text(self):
        if self._clean_texts is None:
            self._clean_texts = self._get_clean_texts()
        return self._clean_texts[0]

    def get_clean_answer_text(self):
        if self._clean_texts is None:
            self._clean_texts = self._get_clean_texts()
        return self._clean_texts[1]

    def _get_clean_texts(self):
        card_note = self.card.note()
        items = dict(card_note.items())
        qfmt = self.card.template().get('qfmt')
        afmt = self.card.template().get('afmt')
        field_names_q = remove_duplicates(field_name_regex.findall(qfmt))
        field_names_a = remove_duplicates(field_name_regex.findall(afmt))

        field_names_a = [
            fn for fn in field_names_a if fn not in set(field_names_q)
        ]
        items_q = [
            self._clean_text(items[field_name])
            for field_name in field_names_q
            if field_name in items
        ]
        items_a = [
            self._clean_text(items[field_name])
            for field_name in field_names_a
            if field_name in items
        ]

        items_q = list(filter(len, items_q))
        items_a = list(filter(len, items_a))

        return " ".join(items_q), " ".join(items_a)

    def _clean_text(self, text):
        text = self.h.handle(text)
        # text = re.sub(r"(?i)<(br ?/?|div|p)>", " ", text)
        text = re.sub(r"\[sound:[^]]+\]", "", text)
        text = re.sub(r"\[anki:[^]]+\]", "", text)
        text = re.sub(r"\[\[type:[^]]+\]\]", "", text)
        text = re.sub(r"[ \n\t]+", " ", text)
        text = text.replace("\t", " " * 8)
        text = text.replace("\n", " ")
        # text = re.sub("(?i)<style>.*?</style>", "", text)
        if '"' in text:
            text = '"' + text.replace('"', '""') + '"'
        text = re.sub(r"!\[\]\(.*\)", "", text)
        text = text.replace("* * *", "")
        text = text.strip()
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

    def get_question_text(self):
        return self.card_text_processor.get_clean_question_text()

    def get_answer_text(self):
        return self.card_text_processor.get_clean_answer_text()

    def get_question_fields(self):
        q_fields = field_name_regex.findall(
            self.card.template().get('qfmt', "")
        )
        return ", ".join(set(q_fields))

    def get_answer_fields(self):
        a_fields = field_name_regex.findall(
            self.card.template().get('afmt', "")
        )
        return ", ".join(set(a_fields))

    def get_note_type(self):
        note_type = self.card.note_type()
        if not note_type:
            return ""

        model_name = note_type.get("name", "")
        match = re.match(r"^(?P<name>.+)-[\w\d]+$", model_name)
        if match:
            return match.groupdict()['name']
        else:
            return model_name

    def model_type(self):
        note_type = self.card.note_type()
        if note_type:
            return MODEL_TYPES_MAP.get(note_type.get("type")) or ""
        return ""

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
        return TYPE_MAP.get(self.card.type, self.card.type)

    def get_prev_card_type(self):
        return TYPE_MAP.get(self.prev_card_version.type,
                            self.prev_card_version.type)

    def get_prev_card_queue(self):
        return QUEUE_MAP.get(self.prev_card_version.queue)

    def get_card_queue(self):
        return QUEUE_MAP.get(self.card.queue)

    def get_last_interval(self):
        return self._get_row_from_revlog("lastIvl")

    def get_estimated_interval(self):
        return self.card.ivl

    def _get_row_from_revlog(self, column_name: str):
        rows = self.card.col.db.execute(
            f"""select {column_name}
                from revlog
                where cid = ? 
                order by id desc
                limit 1
            """,
            self.card.id
        )
        if rows:
            if isinstance(rows, list):  # Linux - "rows" is a list
                row = rows[0]
            else:  # Windows - "rows" is a sqlite.Cursor object.
                row = rows.fetchone()
            return row[0] if row else ""
        else:
            return ""

    def has_cloze(self):
        return has_cloze(self.card_output.question_text)

    def has_type_in(self):
        return bool(
            re.findall(r"\[\[type:.+]]", self.card_output.question_text)
        )

    def has_type_in_cloze(self):
        return bool(
            re.findall(r"\[\[type:cloze:.+]]", self.card_output.question_text)
        )
