import sys
import re


#Finds which grid a given position is located in.
def findPos(grids,x,y):
    for i in range(1,columns*rows):
        if(x>grids[i]["minX"] and y>grids[i]["minY"] and x<=grids[i]["maxX"] and y<=grids[i]["maxY"]):
            return i

#Populates the given group's dictionary by traversing the data received from the file.
def populateDict(grids,fileString,groupType):
    for i in range(1, len(fileString)):
        currentLine = re.split(",", re.sub("\s", "", fileString[i]))
        index = findPos(grids, int(currentLine[1]), int(currentLine[2]))
        if (currentLine[0] == "0"):  # Increase no of people
            grids[index][groupType]["noOfPeople"] += 1
        grids[index][groupType]["timeViewed"] += int(currentLine[3])
        grids[index][groupType]["noOfFixations"] += 1

#Reads the given file and calls populate method for it.
def interpretFiles (fileName,grids):
    try:
        file = open(fileName, "r")
    except IOError:
        exit(1)
    fileString=file.readlines()
    file.close()
    if(fileName=="asd.txt"):
        populateDict(grids,fileString,"ASD")
    elif(fileName=="control.txt"):
        populateDict(grids, fileString, "Control")


testFileName=sys.argv[1]
controlFileName=sys.argv[2]
resolutionX=int(re.split("x",sys.argv[3])[0])
resolutionY=int(re.split("x",sys.argv[3])[1])
rows=int(re.split("x",sys.argv[4])[0])
columns=int(re.split("x",sys.argv[4])[1])
segmentIntervals=[int(resolutionX)/int(columns),int(resolutionY)/int(rows)] #To find the x and y intervals for grids.
grids = {}
currentRow = 1


#Populate dictionary with grid information   Bunu ayrı function yapsak iyi olr
#Olur
for i in range(rows*columns):
    grids[i+1] = {
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

    #Placing the grid boundary coordinates in each grid.
    if((i+1)%columns != 0):
        grids[i + 1]["maxX"] = segmentIntervals[0]*((i+1)%columns)               #Using the modulo operator calculate max X using the intervals.
        grids[i + 1]["minX"] = grids[i+1]["maxX"] - segmentIntervals[0]
        grids[i + 1]["maxY"] = segmentIntervals[1] * currentRow
        grids[i + 1]["minY"] = grids[i + 1]["maxY"] - segmentIntervals[1]
    else:                                                                           #Since modulo operator is used in if condition. Code can't access last column without this else.
        grids[i + 1]["maxX"] = resolutionX
        grids[i + 1]["minX"] = resolutionX - segmentIntervals[0]
        grids[i + 1]["maxY"] = segmentIntervals[1] * currentRow
        grids[i + 1]["minY"] = grids[i + 1]["maxY"] - segmentIntervals[1]
        currentRow += 1


interpretFiles(testFileName,grids)
interpretFiles(controlFileName,grids)

print(grids.values())
