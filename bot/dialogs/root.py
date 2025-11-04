from .base import Dialog

class RootDialog(Dialog):
    name = "root"
    def enter(self, session):
        return "Olá! Diga 'voo' ou 'hotel' para começarmos."
