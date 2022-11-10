def convertTxtToList(text: str):
    """
    Receives a text in the format \"abc def ghi\";
    Returns a list: [\"abc\", \"def\", \"ghi\"]
    """
    try:
        return text.split(" ")
    except:
        print("Incorrect format")
        return None


def clampPositivemeter(i: int):
    if i > 1:
        i = 1
    if i < -1:
        i = -1

    return i
