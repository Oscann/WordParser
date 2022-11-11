import re
from word import SubObj, Word, Noun, Adjective


class StatementManager:

    __objs = []

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
        

    syntax: dict = {
        "existence": ("there\sis\s[a-z\s]+", __processExistence),

    }

    def getObjs(self):
        return [str(x) for x in self.__objs]

    def read(self, text: str):
        text = text.lower()

        statement = None

        for (key, info) in StatementManager.syntax.items():
            if re.fullmatch(info[0], text):
                statement = key

        if statement == None:
            print("Incoehrent, inexistent or incomplete syntax")
            return

        args, func = self.__tokenize(statement, text)
        func(self, *args)

    def createWord(self, word: str, lexicalClass: str):
        word = word.lower()

        Word.createWord(word, lexicalClass)

    def createObj(self, value: str):
        self.__objs.append(SubObj(value))

    def __tokenize(self, statement: str, text: str):
        func = self.syntax[statement][1]
        args = None
        match (statement):
            case "existence":
                args = (text[9:],)
            case _:
                print("Incoehrent, inexistent or incomplete syntax")
                return
        
        return args, func

    def getSubObj(self, value: str):
        for i in self.__objs:
            if i.getValue() == value:
                return i
        
        return None



class Statement:
    statements: dict = {
        "declarations": list(),
        "existence": list(),
        "questions": list()
    }
