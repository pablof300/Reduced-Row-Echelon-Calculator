from collections import defaultdict

class Row(object):
    def __init__(self, values):
        """Holds an array of integers that represent a row in a matrix"""
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
        """Represents a rectangular matrix to be solved using reduced row echelon"""
        self.rows = self.getRows(lines)
        self.toReducedRowEchelonMatrix()

    def toReducedRowEchelonMatrix(self):
        """Transforms the matrix into a matrix in reduced row echelon form"""
        self.normalize()
        pivotDictionary = self.getPivotColDictionary()
        if self.arePivotColumnsRepeated(pivotDictionary):
            self.rows = self.getRowsWithUniquePivots(pivotDictionary)
            self.toReducedRowEchelonMatrix()
        else:
            self.fromRowEchelonToReducedRowEchelon()

    def getRows(self, lines):
        """Transforms an array of Strings (which hold the rows inputted by user) into Row objects"""
        matrixRows = []
        updatedLines = [newLine.replace(" ", "") for newLine in lines]
        for line in updatedLines:
            rowElements = []
            elements = line.split(",")
            for element in elements:
                rowElements.append(int(element))
            matrixRows.append(Row(rowElements))
        return matrixRows

    def printMatrix(self):
        """Prints the rows in the matrix"""
        print "Matrix result:"
        for row in self.rows:
            print row.values
        print "\n"

# Can't remove len because starting from 1
    def isRectangular(self):
        """Returns true if matrix is rectangular (all rows of the same length)"""
        for rowIndex in range(1, len(self.rows)):
            if row[rowIndex].size != row[rowIndex - 1].size:
                return False
        return True

    def arePivotColumnsRepeated(self, pivotDictionary):
        """Return true if there is another pivot variable in the same column"""
        for pivotCol in pivotDictionary.keys():
            if pivotCol == -1:
                continue
            if len(pivotDictionary[pivotCol]) > 1:
                return True
        return False

# Can't remove len because return index
    def findLeadingColumn(self, row):
        """Returns the column at which the pivot variable is located"""
        for index in range(0, len(row.values)):
            if row.values[index] != 0:
                return index
        return -1

    def findLeadingNumber(self, row):
        """Returns the first non-zero number in a row"""
        leadingCol = self.findLeadingColumn(row)
        return row.values[leadingCol]

    def normalize(self):
        """Normalizes all rows in the matrix object"""
        for row in self.rows:
            if row.isEmpty:
                continue
            self.normalize_row(row)

    def normalize_row(self, row):
        """Multiplies a row by a constant in order to obtain a leading 1. For example [3,9,9] -> [1,3,3]"""
        normalized_row_values = []
        multiplication_factor = (1.0) / (self.findLeadingNumber(row))
        for element in row.values:
            if element == 0.0:
                normalized_row_values.append(0.0)
                continue
            normalized_row_values.append(round(element * multiplication_factor, 10))
        row.values = normalized_row_values

    def getPivotColDictionary(self):
        """Returns a dictionary of pivot variables along with the column where they are located"""
        pivotDictionary = {}
        for row in self.rows:
            pivotCol = self.findLeadingColumn(row)
            if not pivotCol in pivotDictionary:
                pivotDictionary[pivotCol] = []
            pivotDictionary[pivotCol].append(row)
        return pivotDictionary

    def sortLeastToGreatest(self, intArray):
        """Sorts an int array from least to greatest"""
        sorted = intArray[:]
        for i in range(0, len(sorted)):
            for j in range(i + 1, len(sorted)):
                if (sorted[i] > sorted[j] and i != j) or sorted[j] < 0:
                    temp = sorted[j]
                    sorted[j] = sorted[i]
                    sorted[i] = temp
        return sorted

    def sortByPivotColumns(self, pivotDictionary):
        """Sorts columns using the location of their pivot columns"""
        sortedIndexes = sortLeastToGreatest(pivotDictionary.keys())
        sortedRows = []
        for index in sortedIndexes:
            for row in pivotDictionary[index]:
                sortedRows.append(row)

    def getRowsWithUniquePivots(self, pivotDictionary):
        """Returns rows that have a pivot variable in a column with no other pivot variables"""
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
        """Converts matrix from row echelon form to reduced row echelon form"""
        for rowIndex in range(1,len(self.rows)):
            if self.rows[rowIndex].isEmpty:
                continue
            leadingCol = self.findLeadingColumn(self.rows[rowIndex])
            for i in range((rowIndex - 1),-1,-1):
                if self.rows[i].values[leadingCol] != 0:
                    self.rows[i] = self.zerofy(self.rows[i], self.rows[rowIndex], leadingCol)

    def zerofy(self, targetRow, toolRow, targetCol):
        """to-do"""
        targetRowValues = targetRow.values
        toolRowValues = toolRow.values
        zerofiedRow = []
        factor = targetRowValues[targetCol]
        for col in range(0, len(targetRowValues)):
            zerofiedRow.append(round(float(targetRowValues[col]) - (float(factor) * toolRowValues[col]), 5))
        return Row(zerofiedRow)

def printSpacers():
    """Prints three empty lines"""
    for i in range(0,3):
        print " "

def isValidRowString(rowString):
    """Return if a String is a valid row input of a matrix (ex: '4,3,4,5'). The input 'cat' would return false"""
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
    """Returns if the inputed String is empty"""
    if len(rowString) <= 0:
        return True
    return False;

def getReducedRowEchelonMatrix(lines):
    """Returns a Matrix object from the rows given by the array lines"""
    return Matrix(lines)



# Start the program
# User will be asked to input a matrix

def askUserForMatrix():
    """Asks for user input of valid matrix rows (ex: [1,2,3,4]) and then performs reduced row echelon operations on the matrix and prints its result"""
    
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

def getCommand():
    pass



askUserForMatrix()
