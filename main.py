import sys
import re
import matplotlib.pyplot as plt


def barChart(title, label, autistic, nonAutistic):
    groups = ["People with Autism", "People Without Autism"]
    values = [autistic, nonAutistic]
    plt.bar(groups, values)
    plt.xlabel('Groups')
    plt.ylabel(label)
    plt.title(title)
    plt.show()


# Finds which grid a given position is located in.
def findPos(grids, x, y):
    for i in range(1, columns * rows):
        if grids[i]["minX"] < x <= grids[i]["maxX"] and grids[i]["minY"] < y <= grids[i]["maxY"]:
            return i


# Populates the given group's dictionary by traversing the data received from the file.
def populateDict(grids, fileString, groupType):
    for i in range(1, len(fileString)):
        currentLine = re.split(",", re.sub("\s", "", fileString[i]))
        index = findPos(grids, int(currentLine[1]), int(currentLine[2]))
        if (currentLine[0] == "0"):  # Increase no of people
            grids[index][groupType]["noOfPeople"] += 1
        grids[index][groupType]["timeViewed"] += int(currentLine[3])
        grids[index][groupType]["noOfFixations"] += 1


# Reads the given file and calls populate method for it.
def interpretFiles(fileName, grids):
    try:
        file = open(fileName, "r")
    except IOError:
        exit(1)
    fileString = file.readlines()
    file.close()
    if fileName == "asd.txt":
        populateDict(grids, fileString, "ASD")
    elif fileName == "control.txt":
        populateDict(grids, fileString, "Control")


testFileName = sys.argv[1]
controlFileName = sys.argv[2]
resolutionX = int(re.split("x", sys.argv[3])[0])
resolutionY = int(re.split("x", sys.argv[3])[1])
rows = int(re.split("x", sys.argv[4])[0])
columns = int(re.split("x", sys.argv[4])[1])
segmentIntervals = [int(resolutionX) / int(columns),
                    int(resolutionY) / int(rows)]  # To find the x and y intervals for grids.
grids = {}
currentRow = 1

# Populate dictionary with grid information   Bunu ayrı function yapsak iyi olr
# Olur
for i in range(rows * columns):
    grids[i + 1] = {
        "ASD": {
            "noOfPeople": 0,
            "timeViewed": 0,
            "noOfFixations": 0
        },
        "Control": {
            "noOfPeople": 0,
            "timeViewed": 0,
            "noOfFixations": 0
        }
    }

    # Placing the grid boundary coordinates in each grid.
    if ((i + 1) % columns != 0):
        grids[i + 1]["maxX"] = segmentIntervals[0] * ((i + 1) % columns)
        # Using the modulo operator calculate max X using the intervals.
        grids[i + 1]["minX"] = grids[i + 1]["maxX"] - segmentIntervals[0]
        grids[i + 1]["maxY"] = segmentIntervals[1] * currentRow
        grids[i + 1]["minY"] = grids[i + 1]["maxY"] - segmentIntervals[1]
    else:  # Since modulo operator is used in if condition. Code can't access last column without this else.
        grids[i + 1]["maxX"] = resolutionX
        grids[i + 1]["minX"] = resolutionX - segmentIntervals[0]
        grids[i + 1]["maxY"] = segmentIntervals[1] * currentRow
        grids[i + 1]["minY"] = grids[i + 1]["maxY"] - segmentIntervals[1]
        currentRow += 1

interpretFiles(testFileName, grids)
interpretFiles(controlFileName, grids)

totalNumbersASD = [0] * 3
totalNumbersControl = [0] * 3


def totalNumbers():
    for x in range(rows * columns):
        totalNumbersASD[0] += grids[x + 1]["ASD"]["noOfPeople"]
        totalNumbersASD[1] += grids[x + 1]["ASD"]["timeViewed"]
        totalNumbersASD[2] += grids[x + 1]["ASD"]["noOfFixations"]

        totalNumbersControl[0] += grids[x + 1]["Control"]["noOfPeople"]
        totalNumbersControl[1] += grids[x + 1]["Control"]["timeViewed"]
        totalNumbersControl[2] += grids[x + 1]["Control"]["noOfFixations"]


def totalNumbersbyElement(element):
    totalNumbersASD[0] += grids[element]["ASD"]["noOfPeople"]
    totalNumbersASD[1] += grids[element]["ASD"]["timeViewed"]
    totalNumbersASD[2] += grids[element]["ASD"]["noOfFixations"]

    totalNumbersControl[0] += grids[element]["Control"]["noOfPeople"]
    totalNumbersControl[1] += grids[element]["Control"]["timeViewed"]
    totalNumbersControl[2] += grids[element]["Control"]["noOfFixations"]


select = 0
while select != 3:
    print('1. Compare the total number of people, the total time viewed, and the total number of fixations for '
          'people with and without autism for a particular element on an image')
    print('2. Compare the total number of people, the total time viewed, and the total number of fixations for people '
          'with and without autism on an image')
    print('3. Exit')
    select = int(input())

    title = 'Comparison Between People With & Without Autism'

    match select:
        case 1:
            print('Available Elements: ')
            for x in range(rows * columns):
                print(chr(64 + x + 1) + " ", end=' ')
            element = input('\nPlease select an element: ')
            elementNum = ord(element) - 64

            totalNumbersbyElement(elementNum)
            barChart(title + ' for Element ' + element, 'Total Number of People', totalNumbersASD[0],
                     totalNumbersControl[0])
            barChart(title + ' for Element ' + element, 'Total Time Viewed', totalNumbersASD[1], totalNumbersControl[1])
            barChart(title + ' for Element ' + element, 'Total Number of Fixation', totalNumbersASD[2],
                     totalNumbersControl[2])
        case 2:
            totalNumbers()
            barChart(title, 'Total Number of People', totalNumbersASD[0], totalNumbersControl[0])
            barChart(title, 'Total Time Viewed', totalNumbersASD[1], totalNumbersControl[1])
            barChart(title, 'Total Number of Fixation', totalNumbersASD[2], totalNumbersControl[2])
