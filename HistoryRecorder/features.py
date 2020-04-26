from anki.cards import Card

from .html2text import HTML2Text


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
