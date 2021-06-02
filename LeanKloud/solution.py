"""
Objective

1. Find the topper in each subject.

2. Find the top 3 students in the class, based on their marks in all subjects.

3. The results should be printed on the console upon running the program with the

csv file as the argument, and look as below:

Topper in Maths is (name of student)

Topper in Biology is (name of student)

...

Best students in the class are (student first rank, student second rank,

student third rank)

Here, the actual student names should be output. Also state complexity of your

algorithm in the Big-O asymptotic notation.

"""
import sys
import csv
import heapq
import numpy
# FileName from argument
fileName = sys.argv[1]

namelist = []
mathsTopperlist = []
biologyTopperlist =  []
englishTopperlist = []
physicsTopperlist =  []
chemistryTopperlist = []
hindiTopperlist = []
totalMarksList = []
# Open csv file containing all the details
try:
    with open(fileName, 'r') as file:
        fileContents = csv.reader(file, delimiter = ",")
        next(fileContents, None)
        # Complexity O(n)
        for studentDetailsRows in fileContents:
            namelist.append(studentDetailsRows[0])
            mathsTopperlist.append(float(studentDetailsRows[1]))
            biologyTopperlist.append(float(studentDetailsRows[2]))
            englishTopperlist.append(float(studentDetailsRows[3]))
            physicsTopperlist.append(float(studentDetailsRows[4]))
            chemistryTopperlist.append(float(studentDetailsRows[5]))
            hindiTopperlist.append(float(studentDetailsRows[6]))
            totalMarksList.append(float(studentDetailsRows[1])+float(studentDetailsRows[2])+float(studentDetailsRows[3])+ float(studentDetailsRows[4])+float(studentDetailsRows[5])+float(studentDetailsRows[6]))
except OSError:
    print("Cannot open file. Error!! Please Check!")
    sys.exit()

def findMaxValues(subjectMarksList, subjectName):
    bestStudents = []
    maxVal = 0
    maxVal = max(subjectMarksList)
    # Complexity O(n)
    for i, marks in enumerate(subjectMarksList):
        # Complexity O(1)
        if(marks == maxVal):
            bestStudents.append(namelist[i])
    print("\nTopper of " + subjectName + " is/are: ")
    # Complexity O(n)
    for students in bestStudents:
        print(" " + students, end=" ")

def findTopthreeStudents(subjectMarksList):
    totalList = numpy.array(subjectMarksList)
    # Complexity O(n * log(n))
    indexPositionsOfToppers = heapq.nlargest(3, range(len(totalList)), totalList.__getitem__)
    print("\nBest students in the class are : ")
    # Complexity O(n)
    for i,items in enumerate(indexPositionsOfToppers):
        print(namelist[items] + " " + str(i+1)+" " + "rank")

findMaxValues(physicsTopperlist, "Physics")
findMaxValues(mathsTopperlist, "Maths")
findMaxValues(biologyTopperlist, "Biology")
findMaxValues(englishTopperlist, "English")
findMaxValues(chemistryTopperlist, "Chemistry")
findMaxValues(hindiTopperlist, "Hindi")
findTopthreeStudents(totalMarksList)


"""
    **Complexity of my Program**

    O(nlong(n))

"""