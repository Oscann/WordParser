from word import Word, Noun, Adjective
from statement import Reader, StatementManager

x = Reader()

x.read("there is a car")
x.read("car is red")
x.read("is car red?")
x.read("/get subject car traits")
