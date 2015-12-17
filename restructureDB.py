from pymongo import MongoClient

client = MongoClient()
db = client.LATIN_DICT
result = db.words.find({})
count = 0
for result_object in result:
  word = None
  tmpType = None
  usage = None
  nominative = None
  genitive = None
  singular = None
  tmpId = None
  incomplete = None
  count = count + 1
  for key, item in result_object.iteritems():
    if key != "_id" and key != "type":
      word = key
      try:
        usage = item['usage']
        nominative = item['nominative']
        genitive = item['genitive']
        singular = item['singular']
        incomplete = 0
      except:
        nominative = item['nominative']
        genitive = item['genitive']
        incomplete = 1
    elif key == "type":
      tmpType = key
    elif key == "_id":
      tmpId = item
  wordEntry = {'word': word, 'type': tmpType, 'usage': usage, 'nominative': nominative,
               'genitive': genitive, 'singular': singular, 'incomplete': incomplete}  
  db.words.remove({"_id":tmpId})
  db.words.insert_one(wordEntry)
  print count 
  #print result_object
