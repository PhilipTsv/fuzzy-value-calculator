from collections import defaultdict
import os
#local files
import Parsing

#rules = []
#statement = []

fileName = "example.txt"
filepath = os.getcwd() + "\\" + fileName
file = open(filepath, 'r')

# splitting the file into a list of lines
lines = file.read().splitlines()
# parsing the lines and etracting the rules and statements from them
lines, statements, rules = Parsing.parseLines(lines)
# creating a dictionary with all fuzzy sets
fuzzyDictionary = Parsing.generateDict(lines)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# access the fuzzy tuples in the dictionary by providing the names of the set and subset
def getSet(upperName, name):
    tempList = fuzzyDictionary[upperName]
    output = []
    for dic in tempList:
        if name in dic:
            #dict.values() returns a view obj so we need to cast it
            #after that it returns a list of lists, so we need to access the 1st (0th) item
            output = list(dic.values())[0]

    if (len(output) > 0):
        return output
    else:
        print("error! ", name, " is not a sub key of any dictionary!")
        return

#handy-dandy function to get all of the sub keys of a key (e.g. get "good","bad","average" in the "driving" dictioanry)
def getSubKeys(upperKey):
    output = []
    dics = list(fuzzyDictionary[upperKey])
    for dic in dics:
        output.append(list(dic.keys())[0])

    return output

#testing getSet function:
#print(getSet('driving','bad'))
#print(statement)

# a function to calculate the membership values of given real values
def calculateFuzzy(inputTuple):
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
            output.append((alpha - a  + value) / alpha)
        #if fuziness is within b - beta
        elif (value > b and value < (beta + b)):
            output.append((b + beta - value) / beta)
        #all other cases - a few of them - fuziness is 0
        else:
            output.append(0)

    return output

# calculate the value of each rule
def calculateRule(string):
    # for storing the values we get from the rule
    arguments = []
    conditions = []
    # getting the words from the statement and removing empty strings
    words = string.split(" ")

    for x in range(0, len(words)):
        #extracting arguments
        if (words[x] in list(fuzzyDictionary.keys())):
            #print(list(fuzzyDictionary[words[x]]), words[x+2])
            if (words[x+1] == "is" and words[x+2] in getSubKeys(words[x])):
                #print("args: ", words[x], words[x+1], words[x+2])
                #print(words[x+2], getSet(words[x], words[x+2]))

                for dic in membershipValues.values():
                    #print(list(dic.keys()))
                    #print(dic[words[x+2]])
                    if (words[x+2] in list(dic.keys())):
                        arguments.append(dic[words[x+2]])

        #extracting conditions
        if (words[x] == "or" or words[x] == "and"):
            conditions.append(words[x])

    #conditions should always be twice as less as the arguments
    if (len(conditions) == len(arguments) / 2):
        #for each condition - check its type and get its arguments, always n and n+1 for condition = n
        for x in range(len(conditions)):
            if conditions[x] == "and":
                return min(arguments[x],arguments[x+1])
            elif conditions[x] == "or":
                return max(arguments[x], arguments[x + 1])
            else:
                print("Error, no condition other than \"or\"  or \"and\" expected")
    else:
        print("Too or too few conditions in the rule!")
    return

# take a list with all the rules and calculate the answers for each, then unify their answers if there are more than 1 per option
def calculateRules(ruleList):
    setOfRules = set()
    dic = defaultdict(list)

    # generate all the options
    for rule in rules:
        words = rule.split(" ")
        setOfRules.add(words[len(words)-1])
    #print(setOfRules)

    # solve each rule using calculateRule(), put the answer in a dictionary, with the option for key
    for rule in rules:
        words = rule.split(" ")
        dic[words[len(words) - 1]].append(calculateRule(rule))
    #print(dic)

    # for each option, check if there are more than one rules
    for key in dic:
        if len(list(dic[key])) > 1:
            #if so, get their maximum
            valule = max(list(dic[key]))
            #print(dic[key])
            dic[key].clear()
            dic[key].append(valule)

    return dic

# calculate the area to exclude
def calcTriagValues(ratio, unknown):
    ratioToExclude = 1 - ratio
    a = unknown[0]
    b = unknown[1]
    alpha = unknown[2]
    beta = unknown[3]

    oldBase = (b + beta) - (a - alpha)
    newBase = ratioToExclude * oldBase
    #print(oldBase, newBase, ratioToExclude, (oldBase / 2) - ((ratioToExclude * newBase) / 2))
    # output 1: old area - the area to exclude
    # output 2: the average of (the beginning, the end and where the height falls) of the base
    return (oldBase / 2) - ((ratioToExclude * newBase) / 2), ((a - alpha) + a + (b+beta))/3

# create a dictionary of the membership values and their respective keys
membershipValues = dict()
for statementLine in statements:
    tempDict = dict()
    valuesList = calculateFuzzy(Parsing.statementToVars(statementLine))
    labels = getSubKeys(Parsing.statementToVars(statementLine)[0])

    for x in range(len(labels)):
        tempDict[labels[x]] = valuesList[x]

    membershipValues[Parsing.statementToVars(statementLine)[0]] = tempDict

#print(membershipValues)
#print(calculateRules(rules))

unknownSet = set(fuzzyDictionary.keys()).difference(set(membershipValues.keys()))
#quick fix - this should be for each
unknown = ''
if len(unknownSet) == 1:
    unknown = unknownSet.pop()

calculationsDic = calculateRules(rules)

outputList = list()
for key in calculationsDic.copy():
    ruleValue = calculationsDic[key][0]
    calculationsDic.pop(key)
    unknownTuple = getSet(unknown, key)
    #print(ruleValue, unknownTuple)

    if unknownTuple[0] == unknownTuple[1]:
        if ruleValue > 0:
            outputList.append(calcTriagValues(ruleValue, unknownTuple))
        #print(outputList)

    if len(calculationsDic) == 0:
        sum1 = 0
        sum2 = 0
        for outputTuple in outputList:
            sum1 += (outputTuple[0] * outputTuple[1])
            sum2 += outputTuple[0]

        print(sum1/sum2)