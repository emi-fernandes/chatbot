from .base import Dialog

class SmalltalkDialog(Dialog):
    name = "smalltalk"
    def enter(self, session):
        return "Posso ajudar com voo ✈️ ou hotel 🏨. O que você precisa?"
