# Is it better convention to use a size object or a tuple?
class Size(object):
    def __init__(self, rows, columns):
        self.rows = rows
        self.rows = columns

class Row(object):
    def __init__(self, values):
        self.values = values

class Matrix(object):
    def __init__(self, size, lines):
        self.size = size
        self.rows = getRows(lines)

    def getRows(lines):
        # Use an array of Rows or use a 2D array?
        matrixRows = []
        updatedLines = [newLine.replace(" ", "") for newLine in lines]
        for line in lines:
            rowElements = []
            elements = line.split(",")
            for index in range(0, len(elements)):
                rowElements[index] = int(elements[index])

    def toString(self):
        if not isValid(self):
            return "Not valid matrix"
        for row in rows:
            print row.values

    def isValid(self):
        pass


def printSpacers():
    print " " * 3

def isValidRowString(rowString):
    if "," not in rowString:
        return False
    elements = rowString.split(",")
    try:
        for index in range(0, len(elements)):
            int(elements[index])
    except:
            return False
    return True

printSpacers()
print "Please type a rectangular matrix row by row."
print "If the first row contains a [1, 2, 3] (left-to-right), then type 1,2,3"
print "Once you type the last line, press enter twice!"
printSpacers()

currentLine = 0;
lines = []
while(True):
    line = raw_input("Row %d> " %(currentLine + 1)
    if isValidRowString(line):
        lines.append(line)
        currentLine += 1
    else:
        print "Please type row %d correctly, or double press enter to finish typing the matrix"
                     

