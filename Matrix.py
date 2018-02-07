# Is it better convention to use a size object or a tuple?
class Size(object):
    def __init__(self, rows, columns):
        self.rows = rows
        self.rows = columns

class Row(object):
    def __init__(self, values):
        self.values = values
        self.size = len(self.values)
        self.isEmpty = self.isEmpty()

    def isEmpty(self):
        for value in self.values:
            if value != 0:
                return False
        return True

class Matrix(object):
    def __init__(self, lines):
        self.rows = self.getRows(lines)
        self.toReducedRowEchelonMatrix()

    def toReducedRowEchelonMatrix(self):
        self.normalizeAll()
        pivotDictionary = self.getPivotColDictionary()
        if self.arePivotColumnsRepeated(pivotDictionary):
            self.rows = self.getRowsWithUniquePivots(pivotDictionary)
            self.toReducedRowEchelonMatrix()
        else:
            self.fromRowEchelonToReducedRowEchelon()
        
            

    def getRows(self, lines):
        # Use an array of Rows or use a 2D array?
        matrixRows = []
        updatedLines = [newLine.replace(" ", "") for newLine in lines]
        for line in lines:
            rowElements = []
            elements = line.split(",")
            for index in range(0, len(elements)):
                rowElements.append(int(elements[index]))
            matrixRows.append(Row(rowElements))
        return matrixRows

    def printMatrix(self):
        print "Matrix result:"
        for row in self.rows:
            print row.values
        print "\n"
    
    # Returns true if matrix is rectangular
    # Returns true if all rows are of the same length (rectangular)
    def isRectangular(self):
        for rowIndex in range(1, len(self.rows)):
            if row[rowIndex].size != row[rowIndex].size:
                return False
        return True

    def arePivotColumnsRepeated(self, pivotDictionary):
        for pivotCol in pivotDictionary.keys():
            if pivotCol == -1:
                continue
            if len(pivotDictionary[pivotCol]) > 1:
                return True
        return False

    def findLeadingColumn(self, row):
        for index in range(0, len(row.values)):
            if row.values[index] != 0:
                return index
        return -1

    def findLeadingNumber(self, row):
        leadingCol = self.findLeadingColumn(row)
        return row.values[leadingCol]

    def normalizeAll(self):
        for rowIndex in range(0, len(self.rows)):
            if self.rows[rowIndex].isEmpty:
                continue
            self.normalize(rowIndex)

    def normalize(self, rowIndex):
        normalizedRowValues = []
        currentRow = self.rows[rowIndex]
        multiplicationFactor = (1.0) / (self.findLeadingNumber(currentRow))
        for valueIndex in range(0, len(currentRow.values)):
            if currentRow.values[valueIndex] == 0.0:
                normalizedRowValues.append(0.0)
                continue
            normalizedRowValues.append(round(currentRow.values[valueIndex] * multiplicationFactor, 10))
        self.rows[rowIndex] = Row(normalizedRowValues)

    def getPivotColDictionary(self):
        pivotDictionary = {}
        for row in self.rows:
            pivotCol = self.findLeadingColumn(row)
            if not pivotCol in pivotDictionary:
                pivotDictionary[pivotCol] = []
            pivotDictionary[pivotCol].append(row)
        return pivotDictionary

    def sortLeastToGreatest(self, intArray):
        sorted = intArray[:]
        for i in range(0, len(sorted)):
            for j in range(i + 1, len(sorted)):
                if (sorted[i] > sorted[j] and i != j) or sorted[j] < 0:
                    temp = sorted[j]
                    sorted[j] = sorted[i]
                    sorted[i] = temp
        return sorted

    def sortByPivotColumns(self, pivotDictionary):
        sortedIndexes = sortLeastToGreatest(pivotDictionary.keys())
        sortedRows = []
        for index in sortedIndexes:
            for row in pivotDictionary[index]:
                sortedRows.append(row)

    def getRowsWithUniquePivots(self, pivotDictionary):
        updatedRows = []
        for pivotCol in pivotDictionary.keys():
            rowArray = pivotDictionary[pivotCol]
            mainRow = rowArray[0]
            updatedRows.append(mainRow)
            for rowIndex in range(1, len(rowArray)):
                currentRowValues = rowArray[rowIndex].values
                updatedRow = []
                for colIndex in range(0, len(rowArray[rowIndex].values)):
                    updatedRow.append(currentRowValues[colIndex] - mainRow.values[colIndex])
                updatedRows.append(Row(updatedRow))
        return updatedRows

    def fromRowEchelonToReducedRowEchelon(self):
        for rowIndex in range(1,len(self.rows)):
            if self.rows[rowIndex].isEmpty:
                continue
            leadingCol = self.findLeadingColumn(self.rows[rowIndex])
            for i in range((rowIndex - 1),-1,-1):
                if self.rows[i].values[leadingCol] != 0:
                    self.rows[i] = self.zerofy(self.rows[i], self.rows[rowIndex], leadingCol)

    def zerofy(self, targetRow, toolRow, targetCol):
        targetRowValues = targetRow.values
        toolRowValues = toolRow.values
        zerofiedRow = []
        factor = targetRowValues[targetCol]
        for col in range(0, len(targetRowValues)):
            zerofiedRow.append(round(float(targetRowValues[col]) - (float(factor) * toolRowValues[col]), 5))
        return Row(zerofiedRow)

# Main program methods

def printSpacers():
    for i in range(0,3):
        print " "

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

def isEmpty(rowString):
    if len(rowString) <= 0:
        return True
    return False;

def getReducedRowEchelonMatrix(lines):
    return Matrix(lines)



# Start the program
# User will be asked to input a matrix

def askUserForMatrix():
    printSpacers()
    print "Please type a rectangular matrix row by row."
    print "If the first row contains a [1, 2, 3] (left-to-right), then type 1,2,3"
    print "Once you type the last line, press enter twice!"
    printSpacers()

    currentLine = 0;
    emptyLines = 0;
    lines = []
    
    while(True):
        line = raw_input("Row %d> " %(currentLine + 1))
        if isEmpty(line):
            
            # The player has pressed double entered and finished typing his matrix
            if emptyLines >= 1:
                getReducedRowEchelonMatrix(lines).printMatrix()
                break
            
            emptyLines += 1
            continue
        
        if isValidRowString(line):
            lines.append(line)
            currentLine += 1
            emptyLines = 0
        else:
            print "Please type row %d correctly, or double press enter to finish typing the matrix"
                     
askUserForMatrix()
