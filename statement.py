import re
from word import SubObj, Word, Noun, Adjective


class StatementManager:

    objs = []

    syntax: dict = {
        "existence": "there\sis\s[a-z\s]+",

    }

    def read(self, text: str):
        text = text.lower()

        statement = None

        for (key, pattern) in StatementManager.syntax.items():
            if re.fullmatch(pattern, text):
                statement = key

        match (statement):
            case "existence":
                self.__processExistence(text)

            case _:
                print("Incoehrent, inexistent or incomplete syntax")

    def createWord(self, word: str, lexicalClass: str):
        word = word.lower()

        Word.createWord(word, lexicalClass)

    def createObj(self, )

    def __tokenize(self):
        pass

    def __processExistence(self, noun: str):
        self.createWord(noun, "noun")


class Statement:
    statements: dict = {
        "declarations": list(),
        "existence": list(),
        "questions": list()
    }
