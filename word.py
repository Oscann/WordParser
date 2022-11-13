from utils import clampPositivemeter, convertTxtToList

print


class Word:

    lexic: dict = {
        "noun": {

        },

        "adjective": {

        },
    }

    def __init__(self, value: str):
        self.setValue(value)

    def createWord(word: str, morphologicalClass: str):
        """
            Receives a word and returns a boolean indicating the success
        """

        print("Starting word creation for {} as {}".format(
            word, morphologicalClass))
        match morphologicalClass:
            case "noun":
                Noun.lexic[word] = Noun(word)

            case "adjective":
                synonyms = convertTxtToList(input(
                    "Inform some synonyms (if there are any) in the format \"abc def ghi\":\n").lower().strip())
                antonyms = convertTxtToList(input(
                    "Inform some antonyms (if there are any) in the format \"abc def ghi\":\n").lower().strip())
                positivemeter = clampPositivemeter(
                    int(input("Inform the adjective positivemeter:\n")))

                Adjective.lexic[word] = Adjective(
                    word, positivemeter, synonyms=synonyms, antonyms=antonyms)

            case _:
                print("There is no such classification: {}".format(
                    morphologicalClass))
                return False

        print("Word created")
        return True

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value


class Adjective(Word):

    lexic: dict = Word.lexic["adjective"]

    def __init__(self, value: str, positivemeter: int, quick: bool = False, synonyms: list = [], antonyms: list = []):
        """
            PositiveMeter:
            1 - Good;
            0 - Neutral;
            -1 - Bad;
        """
        Word.__init__(self, value)
        self.positivemeter = positivemeter
        if not quick:
            self.__startSynonyms(synonyms, antonyms)
        else:
            self.synonyms = set(synonyms)
            self.antonyms = set(antonyms)
            Adjective.lexic[value] = self
            print(f"Quick creation done for {value}")

    def __startSynonyms(self, synonyms: list, antonyms: list):
        print("Starting word synonyms/antonyms")
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
            Adjective.lexic[synonym] = Adjective(value=synonym, positivemeter=self.positivemeter,
                                                 quick=True, antonyms=self.antonyms)

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
            Adjective.lexic[antonym] = Adjective(value=antonym, positivemeter=-self.positivemeter,
                                                 quick=True, synonyms=self.synonyms)

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

    def patch(self, trait: str):
        if trait not in Adjective.lexic.keys():
            print("There is no such adjective in the lexic")
            return

        traitAdjective = Adjective.lexic[trait]

        for i in traitAdjective.antonyms:
            if i in self.traits:
                self.remove(i)

        self.traits.append(trait)

        print("Trait patched")

    def remove(self, trait: str):
        if trait not in Adjective.lexic.keys():
            print("There is no such adjective in the lexic")
            return
        elif trait not in self.traits:
            print(f"This subject is not '{trait}'")
            return

        traitAdjective = Adjective.lexic[trait]

        self.traits.remove(trait)

        for i in traitAdjective.synonyms:
            if i in self.traits:
                self.traits.remove(i)

        print(f"Removed {trait} and it's synonyms")

    def addTrait(self, trait: str):

        # Check if trait is contraditory

        for i in self.traits:
            if trait in Adjective.lexic[i].antonyms:
                print(
                    f"It is impossible for {self.getValue()} be {trait} because {self.getValue()} has an antonym of such trait.")
                return
        if trait in self.traits:
            print(f"{self.getValue()} already is {trait}")
            return

        self.traits.append(trait)

    def getTraits(self):
        return self.traits
