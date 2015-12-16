import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re
#import sys
from pymongo import MongoClient

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']

# todo: fix locative for all nouns; it's only used in a small subset
# nom, gen, dat, acc, abl, voc, loc
endingOrder = ['nom', 'gen', 'dat', 'acc', 'abl', 'voc', 'loc']
firstDeclensionEndingsSg = ['a', 'ae', 'ae', 'am', 'a', 'a', 'ae']
firstDeclensionEndingsPl = [ 'ae', 'arum', 'is', 'as', 'is', 'ae', 'is']

secondDeclensionEndingsMFSg = ['us', 'i', 'o', 'um', 'o', 'e', 'i']
secondDeclensionEndingsMFPl = ['i', 'orum', 'is', 'os', 'is', 'i', 'is']
secondDeclensionEndingsNSg = ['um', 'i', 'o', 'um', 'o', 'um', 'i']
secondDeclensionEndingsNPl = ['a', 'orum', 'is', 'a', 'is', 'a', 'is']
secondDeclensionEndingsRSg = ['-', 'i', 'o', 'um', 'o', '-', 'i']

thirdDeclensionEndingsMFSg = ['-', 'is', 'i', 'em', 'e', '-', 'e']
thirdDeclensionEndingsMFPl = ['es', 'um', 'ibus', 'es', 'ibus', 'es', 'ibus']
thirdDeclensionEndingsNSg = ['-', 'is', 'i', '-', 'e', '-', 'i']
thirdDeclensionEndingsNPl = ['a', 'um', 'ibus', 'a', 'ibus', 'a', 'ibus']

fourthDeclensionEndingsMFSg = ['us', 'us', 'ui', 'um', 'u', 'us', 'u']
fourthDeclensionEndingsMFPl = ['us', 'uum', 'ibus', 'us', 'ibus', 'us', 'ibus']
fourthDeclensionEndingsNSg = ['u', 'us', 'u', 'u', 'u', 'u', 'u']
fourthDeclensionEndingsNPl = ['ua', 'uum', 'ibus', 'ua', 'ibus', 'ua', 'ibus']

fifthDeclensionEndingsMFSg = ['es', 'ei', 'ei', 'em', 'e', 'es', 'e']
fifthDeclensionEndingsMFPl = ['es', 'erum', 'ebus', 'es', 'ebus', 'es', 'ebus']

client = MongoClient()
db = client.LATIN_DICT
#db.words.delete_many({})
#result = db.words.insert_one({ "puella" :["puella, puellae F"]})

for character in letters:
  http = httplib2.Http()
  status, response = http.request('http://latin-dictionary.net/list/letter/' + character)
  for counter, word in enumerate(BeautifulSoup(response, parseOnlyThese=SoupStrainer('li', {'class': 'word'}))):  
    if counter % 200 == 0:
      print counter
    tmp = word.contents
    link = word.contents[0]['href']
    #print link
    if len(tmp) == 2:
      words = re.split('\s+', tmp[0].get_text().strip().replace(',', '').replace('(','').replace(')','').replace('.',''))
      wordType = tmp[1].strip()

      # handle nouns
      if wordType == 'n':
        if len(words) != 2:
          print words
          continue
        nomCase = words[0]
        genCase = words[1]
        # handle first declension
        if nomCase.endswith('a') and genCase.endswith('ae'):
            # first declension unknown gender
            stem = nomCase[:-1]
            for i in range(0,6):
              tmpWordSg = stem + firstDeclensionEndingsSg[i]
              tmpWordPl = stem + firstDeclensionEndingsPl[i]
              #wordEntrySg = [nomCase, genCase, endingOrder[i], 0]
              wordEntrySg = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 1}
              wordEntryPl = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 0}
              db.words.insert_one({tmpWordSg : wordEntrySg})
              db.words.insert_one({tmpWordPl : wordEntryPl})
        
        # handle second declension
        elif nomCase.endswith('us') and genCase.endswith('i'):
            # second declension nominative
            stem = nomCase[:-2]
            for i in range(0,6):
              tmpWordSg = stem + secondDeclensionEndingsMFSg[i]
              tmpWordPl = stem + secondDeclensionEndingsMFPl[i]
              wordEntrySg = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 1}
              wordEntryPl = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 0}
              db.words.insert_one({tmpWordSg : wordEntrySg})
              db.words.insert_one({tmpWordPl : wordEntryPl})
        elif nomCase.endswith('um') and genCase.endswith('i'):
            stem = nomCase[:-2]
            for i in range(0,6): 
              tmpWordSg = stem + secondDeclensionEndingsNSg[i]
              tmpWordPl = stem + secondDeclensionEndingsNPl[i]
              wordEntrySg = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 1}
              wordEntryPl = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 0}
              db.words.insert_one({tmpWordSg : wordEntrySg})
              db.words.insert_one({tmpWordPl : wordEntryPl})
        elif nomCase.endswith('r') and genCase.endswith('i'):
            stem = genCase[:-1]
            for i in range(0,6):
              if secondDeclensionEndingsMFSg[i] == '-':
                tmpWordSg = nomCase
              else:
                tmpWordSg = stem + secondDeclensionEndingsMFSg[i]
              tmpWordPl = stem + secondDeclensionEndingsMFPl[i]
              wordEntrySg = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 1}
              wordEntryPl = {"nominative": nomCase,
                             "genitive": genCase,
                             "usage": endingOrder[i],
                             "singular": 0}
              db.words.insert_one({tmpWordSg : wordEntrySg})
              db.words.insert_one({tmpWordPl : wordEntryPl})
        # handle third declension
        elif genCase.endswith('is'):
            # look up what gender it is
            subStatus, subResponse = http.request(link)
            #for counter, subWord in enumerate(BeautifulSoup(subResponse, parseOnlyThese=SoupStrainer('div', {'class': 'grammar'}))):  
            container = BeautifulSoup(subResponse, parseOnlyThese=SoupStrainer('div', {'class': 'grammar'}))   
            try:
              gender = container.findAll('span')[3].get_text()
            except:
              print 'error in ' + str(words) + ' unable to get gender info'
              wordEntry = {"nominative": nomCase,
                           "genitive": genCase,
                           "incomplete": 1}
              db.words.insert_one({nomCase : wordEntry})
              continue
            if gender == 'feminine' or gender == 'masculine':
              stem = genCase[:-2]
              for i in range(0,6):
                if thirdDeclensionEndingsMFSg[i] == '-':
                  tmpWordSg = nomCase
                else:
                  tmpWordSg = stem + thirdDeclensionEndingsMFSg[i]
                tmpWordPl = stem + thirdDeclensionEndingsMFPl[i]
                wordEntrySg = {"nominative": nomCase,
                             "genitive": genCase,
                             "gender": gender,
                             "usage": endingOrder[i],
                             "singular": 1}
                wordEntryPl = {"nominative": nomCase,
                             "genitive": genCase,
                             "gender": gender,
                             "usage": endingOrder[i],
                             "singular": 0}
                db.words.insert_one({tmpWordSg : wordEntrySg})
                db.words.insert_one({tmpWordPl : wordEntryPl})
 
            elif gender == 'neuter':
              stem = genCase[:-2]
              for i in range(0,6):
                if thirdDeclensionEndingsNSg[i] == '-':
                  tmpWordSg = nomCase
                else:
                  tmpWordSg = stem + thirdDeclensionEndingsNSg[i]
                tmpWordPl = stem + thirdDeclensionEndingsNPl[i]
                wordEntrySg = {"nominative": nomCase,
                             "genitive": genCase,
                             "gender": gender,
                             "usage": endingOrder[i],
                             "singular": 1}
                wordEntryPl = {"nominative": nomCase,
                             "genitive": genCase,
                             "gender": gender,
                             "usage": endingOrder[i],
                             "singular": 0}
                db.words.insert_one({tmpWordSg : wordEntrySg})
                db.words.insert_one({tmpWordPl : wordEntryPl})
              

        # handle fourth declension
        elif nomCase.endswith('us') and genCase.endswith('us'):
          stem = genCase[:-2]
          for i in range(0,6):
            tmpWordSg = stem + fourthDeclensionEndingsMFSg[i]
            tmpWordPl = stem + fourthDeclensionEndingsMFPl[i]
            wordEntrySg = {"nominative": nomCase,
                            "genitive": genCase,
                            "usage": endingOrder[i],
                            "singular": 1}
            wordEntryPl = {"nominative": nomCase,
                            "genitive": genCase,
                            "usage": endingOrder[i],
                            "singular": 0}
            db.words.insert_one({tmpWordSg : wordEntrySg})
            db.words.insert_one({tmpWordPl : wordEntryPl})
 
        elif nomCase.endswith('u') and genCase.endswith('us'):
          stem = genCase[:-2]
          for i in range(0,6):
            tmpWordSg = stem + fourthDeclensionEndingsNSg[i]
            tmpWordPl = stem + fourthDeclensionEndingsNPl[i]
            wordEntrySg = {"nominative": nomCase,
                            "genitive": genCase,
                            "usage": endingOrder[i],
                            "singular": 1}
            wordEntryPl = {"nominative": nomCase,
                            "genitive": genCase,
                            "usage": endingOrder[i],
                            "singular": 0}
            db.words.insert_one({tmpWordSg : wordEntrySg})
            db.words.insert_one({tmpWordPl : wordEntryPl})
        
        # handle the fifth declension
        elif nomCase.endswith('es') and genCase.endswith('ei'):
          stem = genCase[:-2]
          for i in range(0,6):
            tmpWordSg = stem + fifthDeclensionEndingsMFSg[i]
            tmpWordPl = stem + fifthDeclensionEndingsMFPl[i]
            wordEntrySg = {"nominative": nomCase,
                            "genitive": genCase,
                            "usage": endingOrder[i],
                            "singular": 1}
            wordEntryPl = {"nominative": nomCase,
                            "genitive": genCase,
                            "usage": endingOrder[i],
                            "singular": 0}
            db.words.insert_one({tmpWordSg : wordEntrySg})
            db.words.insert_one({tmpWordPl : wordEntryPl})
        else:
          print 'error in ' + str(words) + ' does not match endings'
          wordEntry = {"nominative": nomCase,
                       "genitive": genCase,
                       "incomplete": 1}
          db.words.insert_one({nomCase : wordEntry})
 
    else:
      print 'error in ' + tmp + ' length is not 2'
      #print tmp[0]
      # add this to list of words
