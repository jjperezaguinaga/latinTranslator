import csv

def getEndings():
  
  idxMappings = {"nom":0, "gen":1, "gender":2}

  reader = csv.reader(open(filePath + file, 'r'))
  for row in reader:
    nominativeCase = row[idxMappings["nom"]]
    if row[idxMappings["gen"]] == "ae":
      # first declension sg
      baseNoun = nominativeCase[:-1]
    elif row[idxMappings["gen"]] == "i":
      # second declension sg
      # check gender
      if row[idxMappings["gender"]] == "N":
        baseNoun = nominativeCase[:-2]
        formList = generateFormsList(baseNoun, nominativeCase, 4)

      elif row[idxMappings["gender"]] == "M":
        # check for -er vs -us noun
        # todo: check for nouns like "vir"
        baseNoun = nominativeCase[:-2]
        if nominativeCase[len(str)-2:] == "er":
          formList = generateFormsList(baseNoun, nominativeCase, 3)
        else:
          formList = generateFormsList(baseNoun, nominativeCase, 2)

    elif row[idxMappings["gen"]] == "is":
      # third declension sg

    elif row[idxMappings["gen"]] == "us":
      # fourth declension sg

    elif row[idxMappings["gen"]] == "es":
      # fifth declension sg

def generateFormsList(baseNoun, nominativeCase, caseNumber):
  endingList = getEndings(caseNumber)
  typeIndicies = { 1: "nominative singular",
    2: "genitive singular", 3: "dative singular",
    4: "accusative singluar", 5:"ablative singular",
    6: "vocative singular", 7: "locative singular",
    8: "nominative plural", 9: "genitive plural", 
    10: "dative plural", 11: "accusative plural",
    12:"ablative plural", 13: "vocative plural", 
    14: "locative plural"
    }
  wordMappings = {}
  for i, ending in enumerate(endingList):
    if ending == "-":
      tmpWord = nominativeCase
    else if ending.contains("/"):
      allEndings = ending.split("/")
      for tmp in allEndings:
        tmpWord = baseNoun + tmp


    else:
      tmpWord = baseNoun + ending
      if wordMappings


def getEndings(caseNumber):
  # listed in order:
  # sg: N G D A A V L
  # pl: N G D A A V L
  mappings = [
    # first declension
    "a ae ae am a a ae ae arum is as is ae is",
    # second declension M -us
    "us i o um o e/i i i orum is os is i is",
    # second declension M -er
    "- i o um o - i i orum is as os is i is",
    # second declension N
    "um i o um o um i a orum is as is a is",
    # third declension
    # todo: make endings work for third, fourth, fifth declensions


  ]
  return mappings[caseNumber].split()

















