from collections import defaultdict

class Row(object):
    def __init__(self, values):
        """Holds an array of integers that represent a row in a matrix"""
        self.values = values
        self.size = len(self.values)
        self.empty = self.isEmpty()

    def isEmpty(self):
        for value in self.values:
            if value != 0:
                return False
        return True

class Matrix(object):
    """Represents a rectangular matrix to be solved using reduced row echelon"""
    
    def __init__(self, rows):
        self.rows = rows
        self.toReducedRowEchelonMatrix()

    def toReducedRowEchelonMatrix(self):
        """Transforms the matrix into a matrix in reduced row echelon form"""
        self.normalize()
        pivot_dictionary = self.getPivotColDictionary()
        if self.arePivotColumnsRepeated(pivot_dictionary):
            self.rows = self.getRowsWithUniquePivots(pivot_dictionary)
            self.toReducedRowEchelonMatrix()
        else:
            self.fromRowEchelonToReducedRowEchelon()

    def printMatrix(self):
        """Prints the rows in the matrix"""
        print "Matrix result:"
        for row in self.rows:
            print row.values
        print "\n"

    def isRectangular(self):
        """Returns true if matrix is rectangular (all rows of the same length)"""
        for index, row in enumerate(self.rows[1:]):
            if row.size != self.rows[index - 1].size:
                return False
        return True

    def arePivotColumnsRepeated(self, pivot_dictionary):
        """Return true if there is another pivot variable in the same column"""
        for pivot_col in pivot_dictionary.keys():
            if pivot_col == -1:
                continue
            if len(pivot_dictionary[pivot_col]) > 1:
                return True
        return False

    def findLeadingColumn(self, row):
        """Returns the column at which the pivot variable is located"""
        for index, value in enumerate(row.values):
            if value != 0:
                return index;
        return -1

    def findLeadingNumber(self, row):
        """Returns the first non-zero number in a row"""
        leading_col = self.findLeadingColumn(row)
        return row.values[leading_col]

    def normalize(self):
        """Normalizes all rows in the matrix object"""
        for row in self.rows:
            if row.empty:
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
        pivot_dictionary = defaultdict(list)
        for row in self.rows:
            pivot_col = self.findLeadingColumn(row)
            pivot_dictionary[pivot_col].append(row)
        return pivot_dictionary

    def getRowsWithUniquePivots(self, pivot_dictionary):
        """Returns rows that have a pivot variable in a column with no other pivot variables"""
        updated_rows = []
        for pivot_col in pivot_dictionary.keys():
            row_array = pivot_dictionary[pivot_col]
            main_row = row_array[0]
            updated_rows.append(main_row)
            for row in row_array[1:]:
                currentRowValues = row.values
                updated_row = []
                for index, value in enumerate(row.values):
                    updated_row.append(value - main_row.values[index])
                updated_rows.append(Row(updated_row))
        return updated_rows

    def fromRowEchelonToReducedRowEchelon(self):
        """Converts matrix from row echelon form to reduced row echelon form"""
        for index, row in enumerate(self.rows[1:]):
            if row.empty:
                continue
            leading_col = self.findLeadingColumn(row)
            for i in range(index, -1, -1):
                if self.rows[i].values[leading_col] != 0:
                    self.rows[i] = self.zerofy(self.rows[i], row, leading_col)

    def zerofy(self, target_row, tool_row, targetCol):
        """It will subtract the target_row from the tool_row in an attempt to create 0's and different pivot columns"""
        target_row_values = target_row.values
        tool_row_values = tool_row.values
        zerofied_row = []
        factor = target_row_values[targetCol]
        for index, target_value in enumerate(target_row_values):
            zerofied_row.append(round(float(target_value) - (float(factor) * tool_row_values[index]), 5))
        
        return Row(zerofied_row)

def printSpacers():
    """Prints three empty lines"""
    print("\n\n\n")

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

def getRows(lines):
    """Transforms an array of Strings (which hold the rows inputted by user) into Row objects"""
    matrix_rows = []
    updated_lines = [newLine.replace(" ", "") for newLine in lines]
    for line in updated_lines:
        row_elements = []
        elements = line.split(",")
        for element in elements:
            row_elements.append(int(element))
        matrix_rows.append(Row(row_elements))
    return matrix_rows

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
            if emptyLines >= 1:
                Matrix(getRows(lines)).printMatrix()
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

if __name__ == "__main__":
    askUserForMatrix()
