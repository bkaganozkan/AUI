from PyQt5.QtGui import QColor


command = {
}
for color in QColor.colorNames():
    command[color] = color
def colr(blue):
    clr = ""
    try:
        if command[blue]:
            return command[blue]
    except:
        clr = "black"
        return clr



def findMath(text):
    text += " "
    items = []
    it = ""
    for item in text:
        if item == " ":
            items.append(it)
            it = ""
        else:
            it += item
    return items

def calculateMath(items):
    result = 0
    try:
        items[0] = int(items[0])
        items[2] = int(items[2])
    except: "We need integers"
    if items [1] == "+":
        result = items[0] + items[2]
    elif items[1] == "-":
        result = items[0] - items[2]
    elif items[1] == "*":
        result = items[0] * items[2]
    elif items[1] == "/":
        result = items[0] / items[2]
    return result




