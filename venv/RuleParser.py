from collections import defaultdict
import os

rules = []
values = []
fuzzyDictionary = defaultdict(list)

fileName = "example.txt"
filepath = os.getcwd() + "\\" + fileName
file = open(filepath, 'r')

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

lines = file.read().splitlines()

#removnig the first line - the title
lines = lines[1:len(lines)]

#removing empty lines
#https://kite.com/python/answers/how-to-remove-empty-strings-from-a-list-of-strings-in-python
lines = [string for string in lines if string != ""]

#extracting values and rules from the file
for x in range(0, len(lines)):
    if "=" in lines[x]:
        values.append(lines[x])
    elif "Rule " in lines[x]:
        rules.append(lines[x])

#removing values from lines
lines = [x for x in lines if x not in values]

#remove rules from lines
lines = [x for x in lines if x not in rules]

#print(lines)
#print(values)
#print(rules)

upperName = ""
for  x in range(0, len(lines)):
    if hasNumbers(lines[x]) is False:
        upperName = lines[x].strip()
    else:
        tempdict = dict()
        words = lines[x].split(" ")
        #removing empty strings, if any
        #https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
        words = list(filter(None, words))
        name = ""
        numbers = []
        for word in words:
            if hasNumbers(word) is False:
                name = word
            else:
                numbers.append(int(word))

        tempdict[name] = numbers
        fuzzyDictionary[upperName].append(tempdict)

print(fuzzyDictionary)

def getSet(upperName, name):
    tempList = fuzzyDictionary[upperName]
    for dic in tempList:
        if name in dic:
            #dict.values() returns a view obj so we need to cast it
            #after that it returns a list of lists, so we need to access the 1st (0th) item
            return list(dic.values())[0]
        else:
            print("error!")
            return

#testing getSet function:
#print(getSet('driving','bad'))

def calcAsc(a, alpha, value):
    return (alpha - a  + value) / alpha

def calcDesc(b, beta, value):
    return (b + beta - value) / beta

print(values)

def valueToVars(str):
    name = ""
    value = 0

    #getting the words from the statement and stripping white space
    words = str.split(" ")
    words = list(filter(None, words))

    for word in words:
        word = word.strip()
        if hasNumbers(word) is False and word is not "=":
            name = word
        elif (hasNumbers(word)):
            value = word

    return name,value

def calculate_fuzzy(inputTuple):
    name = inputTuple[0]
    value = int(inputTuple[1])
    fuzzyDict = fuzzyDictionary[name]
    output = []

    # for each area in fuzzy values
    for dic in fuzzyDict:
        ranges = list(dic.values())[0]
        a = ranges[0]
        b = ranges[1]
        alpha = ranges[2]
        beta = ranges[3]

        #if fuzzines of value is 1
        if (value > a and value < b) or (value == a or value == b):
            output.append(1)
        #if fuziness is within alpha - a
        elif (value > (a - alpha) and value < a):
            output.append(calcAsc(a, alpha, value))
        #if fuziness is within b - beta
        elif (value > b and value < (beta + b)):
            output.append(calcDesc(b, beta, value))
        #all other cases - a few of them - fuziness is 0
        else:
            output.append(0)

    return output

fuzzyValues = []
for value in values:
    fuzzyValues.append(calculate_fuzzy(valueToVars(value)))

print(fuzzyValues)


