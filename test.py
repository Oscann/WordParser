import re

WORD = "[a-z-]+"

x = fr"(?<=there\sis\sa\s){WORD}"

c = re.fullmatch(x, "there is a car")
print(c)
