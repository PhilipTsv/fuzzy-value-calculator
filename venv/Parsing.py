from collections import defaultdict

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def parseLines(lines):
    rules = []
    values = []

    # removnig the first line - the title
    lines = lines[1:len(lines)]

    # removing empty lines
    # https://kite.com/python/answers/how-to-remove-empty-strings-from-a-list-of-strings-in-python
    lines = [string for string in lines if string != ""]

    # extracting values and rules from the file
    for x in range(0, len(lines)):
        if "=" in lines[x]:
            values.append(lines[x])
        elif "Rule " in lines[x]:
            rules.append(lines[x])

    # removing values from lines
    lines = [x for x in lines if x not in values]

    # remove rules from lines
    lines = [x for x in lines if x not in rules]

    # print(lines)
    # print(values)
    # print(rules)

    return lines, values, rules

def generateDict(linesList):
    dic = defaultdict(list)
    upperName = ""
    for  x in range(0, len(linesList)):
        if hasNumbers(linesList[x]) is False:
            upperName = linesList[x].strip()
        else:
            tempdict = dict()
            words = linesList[x].split(" ")
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
            dic[upperName].append(tempdict)

    #print(dic)
    return dic

# a function that strips the strings containing the values into variables we can work with
# example: driving = 85 to 'driving','85'
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