from utils import clampPositivemeter, convertTxtToList


class Word:

    lexic: dict = {
        "noun": {

        },

        "adjective": {

        },

        "verb": {

        }
    }

    def __init__(self, value: str):
        self.setValue(value)

    def createWord(word: str, lexicalClass: str):
        """
            Receives a word and returns a boolean indicating the success
        """

        print("Starting word creation for {} as {}".format(word, lexicalClass))
        match lexicalClass:
            case "noun":
                Noun.lexic[word] = Noun(word)

            case "adjective":
                synonyms = convertTxtToList(input(
                    "Inform some synonyms (if there are any) in the format \"abc def ghi\":\n"))
                antonyms = convertTxtToList(input(
                    "Inform some antonyms (if there are any) in the format \"abc def ghi\":\n"))
                positivemeter = clampPositivemeter(
                    int(input("Inform the adjective positivemeter:\n")))

                Adjective.lexic[word] = Adjective(
                    word, positivemeter, synonyms, antonyms)

            case _:
                print("There is no such classification: {}".format(lexicalClass))
                return False

        print("Word created")
        return True

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value


class Noun(Word):
    lexic: dict = Word.lexic["noun"]

    def __init__(self, value: str):
        value = value.lower()
        super().__init__(value)


class SubObj(Noun):
    def __init__(self, value):
        value = value.lower()
        super().__init__(value)
        self.traits = list()

    def __str__(self):
        return self.getValue()

    def addTrait(self, trait: str):
        
        # Check if trait is contraditory

        for i in self.traits:
            if 


class Adjective(Word):

    lexic: dict = Word.lexic["adjective"]

    def __init__(self, value: str, positivemeter: int, synonyms: list = [], antonyms: list = []):
        """
            PositiveMeter:
            1 - Good;
            0 - Neutral;
            -1 - Bad;
        """
        value = value.lower()
        Word.__init__(self, value)
        self.positivemeter = positivemeter
        self.__startSynonyms(synonyms, antonyms)

    def __startSynonyms(self, synonyms: list, antonyms: list):
        print("Starting word Synonyms")
        self.synonyms = set()
        self.antonyms = set()

        for synonym in synonyms:
            self.addSynonym(synonym)

        for antonym in antonyms:
            self.addAntonym(antonym)

    def addSynonym(self, synonym: str):

        synonym = synonym.lower()  # Remove after dev

        if synonym not in Adjective.lexic.keys():
            print(f"{synonym} doesn't exist in our lexic")
            print("Starting quick creation")
            Adjective(
                value=synonym,
                positivemeter=self.positivemeter,
                antonyms=self.antonyms
            )

        synonym: Adjective = Adjective.lexic[synonym]

        if self.positivemeter != synonym.positivemeter:
            print(self.getValue() + " and " +
                  synonym.getValue() + " cannot be synonyms.")
            return

        ownSynonyms = list(self.synonyms)
        wordSynonyms = list(synonym.synonyms)

        # ownSynonyms.extend(wordSynonyms)
        # wordSynonyms.extend(ownSynonyms)
        ownSynonyms.append(synonym.getValue())
        wordSynonyms.append(self.getValue())

        self.synonyms = set(ownSynonyms)
        synonym.synonyms = set(wordSynonyms)

    def addAntonym(self, antonym: str):

        antonym = antonym.lower()  # Remove after dev

        if antonym not in Adjective.lexic.keys():
            print(f"{antonym} doesn't exist in our lexic")
            print("Starting quick creation")
            Adjective(
                value=antonym,
                positivemeter=-self.positivemeter,
                antonyms=self.synonyms
            )

        antonym: Adjective = Adjective.lexic[antonym]

        if self.positivemeter == antonym.positivemeter:
            print(self.getValue() + " and " +
                  antonym.getValue() + " cannot be antonyms.")
            return

        ownAntonyms = list(self.antonyms)
        wordAntonyms = list(antonym.antonyms)

        # ownantonyms.extend(wordantonyms)
        # wordantonyms.extend(ownantonyms)
        ownAntonyms.append(antonym.getValue())
        wordAntonyms.append(self.getValue())

        self.antonyms = set(ownAntonyms)
        antonym.antonyms = set(wordAntonyms)

    def getSynonyms(self):
        return self.synonyms

    def getAntonyms(self):
        return self.antonyms


class Verb(Word):
    lexic: dict = Word.lexic["verb"]
