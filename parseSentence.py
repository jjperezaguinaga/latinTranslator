import re
from pymongo import MongoClient

def setup():
  client = MongoClient()
  db = client.LATIN_DICT
  #db.words.find({"puella": {'$exists':True}})
  parseSentence(db, "puella amat puellam")

def parseSentence(db, sentence):
  potentialSubjects = identifySubjects(db, sentence)

def identifySubjects(db, sentence):
  words = re.split('\s+', sentence)
  potentialSubjects = []
  for word in words:
    result = db.words.find({'word': word})
    for result_object in result:
      if result_object['usage'] == "nom":
        potentialSubjects.append(result_object)
      #print result_object
    #print result

if __name__ == "__main__":
  setup()
