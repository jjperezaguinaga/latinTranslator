import csv

def getEndings():
  
  idxMappings = {"nom":0, "gen":1, "gender":2}

  reader = csv.reader(open(filePath + file, 'r'))
  for row in reader:
    nominativeCase = row[idxMappings["nom"]]
    if row[idxMappings["gen"]] == "ae":
      // first declension sg
      baseNoun = nominativeCase[:-1]
    elif row[idxMappings["gen"]] == "i":
      // second declension sg
      // check gender
      if row[idxMappings["gender"]] == "N":
        baseNoun = nominativeCase[:-2]
        endingList = generateEndings(baseNoun, 4)

      elif row[idxMappings["gender"]] == "M":
        // check for -er vs -us noun
        // todo: check for nouns like "vir"
        baseNoun = nominativeCase[:-2]
        if nominativeCase[len(str)-2:] == "er":
          endingList = generateEndings(baseNoun, 3)
        else:
          endingList = generateEndings(baseNoun, 2)

    elif row[idxMappings["gen"]] == "is":
      // third declension sg

    elif row[idxMappings["gen"]] == "us":
      // fourth declension sg

    elif row[idxMappings["gen"]] == "es":
      // fifth declension sg