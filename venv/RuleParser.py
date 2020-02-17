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

#access a
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

#handy-dandy function to get all of the sub keys of a key (e.g. get "good","bad","average" in the "driving" dictioanry
def getSubKeys(upperKey):
    output = []
    dics = list(fuzzyDictionary[upperKey])
    for dic in dics:
        output.append(list(dic.keys())[0])

    return output


#testing getSet function:
#print(getSet('driving','bad'))
#print(values)

#functions to calculate the fuzzy values when the points are in the ascension or descension of a range of a fuzzy value
def calcAsc(a, alpha, value):
    return (alpha - a  + value) / alpha

def calcDesc(b, beta, value):
    return (b + beta - value) / beta

#a function that strips the strings containing the values into variables we can work with
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

#a function to calculate the membership values of given real values
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

# calculate the value of each tule
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
    # print(setOfRules)

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

#def calcNewTriagValues():

# create a dictionary of the membership values and their respective keys
membershipValues = dict()
for value in values:
    tempDict = dict()
    valuesList = calculate_fuzzy(valueToVars(value))
    labels = getSubKeys(valueToVars(value)[0])

    for x in range(len(labels)):
        tempDict[labels[x]] = valuesList[x]

    membershipValues[valueToVars(value)[0]] = tempDict

print(membershipValues)
print(calculateRules(rules))

