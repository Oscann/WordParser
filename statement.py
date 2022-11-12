import re
from utils import convertTxtToList
from word import SubObj, Word, Noun, Adjective

WORD = "[a-z-]+"


class Reader:
    def __init__(self):
        self.statement = StatementManager()
        self.command = CommandManager()

    def read(self, text):
        text = text.lower().strip()

        pattern = None

        # Compare patterns
        for (key, info) in self.statement.syntax.items():
            if re.fullmatch(info[0], text):
                pattern = key
                manager = "statement"

        for (key, info) in self.command.syntax.items():
            if re.fullmatch(info[0], text):
                pattern = key
                manager = "command"

        # If no pattern matched
        if pattern == None:
            print("Incoehrent, inexistent or incomplete syntax")
            return

        self.__dict__[manager].process(text, pattern)

# Abstract class for the managers


class Manager:

    syntax = dict()

    _objs = []

    def process(self, text: str, pattern: str):

        # Prepare Process
        func = self.syntax[pattern][1]
        args = self._tokenize(pattern, text)

        # "Error handling" :P
        if args == -1:
            print("Something was wrong with the tokens")
            return
        if args == -2:
            print("Incoehrent, inexistent or incomplete syntax")
            return

        func(self, *args)

    def _tokenize(self, pattern, text):
        pass

    def getSubObj(self, value: str):
        for i in Manager._objs:
            if i.getValue() == value:
                return i

        return None

    def getObjs(self):
        return [str(x) for x in Manager._objs]


class StatementManager(Manager):

    def __processExistence(self, noun: str):
        self.createWord(noun, "noun")
        self.createObj(noun)

    def __processDeclaration(self, subject: str, adjective: str):
        if subject not in self.getObjs():
            print(f"The subject '{subject}' does not exist")
            return

        if adjective not in Adjective.lexic:
            print("Such adjective doesn't exist")
            self.createWord(adjective, "adjective")

        subobj = self.getSubObj(subject)

        subobj.addTrait(adjective)

    def __processInterrogation(self, subject, adjective):
        result = False

        if subject not in self.getObjs():
            print(f"The subject '{subject}' does not exist")
            return

        if adjective not in Adjective.lexic:
            print("Such adjective doesn't exist")
            self.createWord(adjective, "adjective")

        subobj = self.getSubObj(subject)

        if adjective in subobj.getTraits():
            result = True
        else:
            for trait in subobj.getTraits():
                if adjective in Adjective.lexic[trait].synonyms:
                    result = True

        if result:
            print("Yes, it is")
        else:
            print("No, it isn't")

    syntax: dict = {
        "existence": (f"there\sis\sa\s{WORD}", __processExistence),
        "declaration": (f"{WORD}\sis\s{WORD}", __processDeclaration),
        "interrogation": (f"is\s{WORD}\s{WORD}\?", __processInterrogation)
    }

    def _tokenize(self, pattern: str, text: str):
        args = -1
        match (pattern):
            case "existence":
                wordTokens = convertTxtToList(text[11:])
                if len(wordTokens) == 1:
                    args = tuple(wordTokens)
            case "declaration":
                wordTokens = convertTxtToList(" ".join(re.split(" is ", text)))
                if len(wordTokens) == 2:
                    args = tuple(wordTokens)
            case "interrogation":
                wordTokens = convertTxtToList(text[3:-1])
                if len(wordTokens) == 2:
                    args = tuple(wordTokens)
            case _:
                args = -2
        return args

    def createWord(self, word: str, morphologicalClass: str):
        Word.createWord(word, morphologicalClass)

    def createObj(self, value: str):
        Manager._objs.append(SubObj(value))


class CommandManager(Manager):

    def __processGetField(self, wordClass: str, word: str, field: str):
        data = None

        if wordClass == "subject":
            if word not in self.getObjs():
                print("There's no subject named that way")
                return
            subject = self.getSubObj(word)

            if field in subject.__dict__.keys():
                data = subject.__dict__[field]

        elif wordClass in Word.lexic.keys():
            if word not in Word.lexic[wordClass]:
                print("Word not found")
                return

            wordObj = Word.lexic[wordClass][word]

            if field in wordObj.__dict__.keys():
                data = wordObj.__dict__[field]

        else:
            print("Invalid word-class")
            return

        if data == None:
            print("No data found")
            return

        print(f"{word}'s {field}: {data}")

    syntax: dict = {
        "get_field": (f"/get\s{WORD}\s{WORD}\s{WORD}", __processGetField)
    }

    def _tokenize(self, pattern: str, text: str):
        args = -1

        match(pattern):
            case "get_field":
                argumentTokens = convertTxtToList(text[4:])
                if len(argumentTokens) == 3:
                    args = tuple(argumentTokens)
            case _:
                args = -2

        return args
