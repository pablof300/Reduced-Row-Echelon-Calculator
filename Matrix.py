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
    
    def __init__(self, lines):
        self.rows = self.getRows(lines)
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

    def getRows(self, lines):
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

    def printMatrix(self):
        """Prints the rows in the matrix"""
        print "Matrix result:"
        for row in self.rows:
            print row.values
        print "\n"

    # Can't remove len because starting from 1
    def isRectangular(self):
        """Returns true if matrix is rectangular (all rows of the same length)"""
        for row_index in range(1, len(self.rows)):
            if row[row_index].size != row[row_index - 1].size:
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

    # Can't remove len because return index
    def findLeadingColumn(self, row):
        """Returns the column at which the pivot variable is located"""
        for index in range(0, len(row.values)):
            if row.values[index] != 0:
                return index
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

    # Can't remove len because starting from 1 and comparing different arrays at a time
    def getRowsWithUniquePivots(self, pivot_dictionary):
        """Returns rows that have a pivot variable in a column with no other pivot variables"""
        updated_rows = []
        for pivot_col in pivot_dictionary.keys():
            row_array = pivot_dictionary[pivot_col]
            main_row = row_array[0]
            updated_rows.append(main_row)
            for row_index in range(1, len(row_array)):
                currentRowValues = row_array[row_index].values
                updated_row = []
                for col_index in range(0, len(row_array[row_index].values)):
                    updated_row.append(currentRowValues[col_index] - main_row.values[col_index])
                updated_rows.append(Row(updated_row))
        return updated_rows

    # Can't remove len because starting from 1
    def fromRowEchelonToReducedRowEchelon(self):
        """Converts matrix from row echelon form to reduced row echelon form"""
        for row_index in range(1,len(self.rows)):
            if self.rows[row_index].empty:
                continue
            leading_col = self.findLeadingColumn(self.rows[row_index])
            for i in range((row_index - 1),-1,-1):
                if self.rows[i].values[leading_col] != 0:
                    self.rows[i] = self.zerofy(self.rows[i], self.rows[row_index], leading_col)

    # Can't remove len because using two arrays at a time
    def zerofy(self, target_row, tool_row, targetCol):
        """It will subtract the target_row from the tool_row in an attempt to create 0's and different pivot columns"""
        target_row_values = target_row.values
        tool_row_values = tool_row.values
        zerofied_row = []
        factor = target_row_values[targetCol]
        for col in range(0, len(target_row_values)):
            zerofied_row.append(round(float(target_row_values[col]) - (float(factor) * tool_row_values[col]), 5))
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
