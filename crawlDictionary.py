import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re

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


for character in letters:
  http = httplib2.Http()
  status, response = http.request('http://latin-dictionary.net/list/letter/' + character)
  for word in BeautifulSoup(response, parseOnlyThese=SoupStrainer('li', {'class': 'word'})):  
    tmp = word.contents
    print len(tmp)
    if len(tmp) == 2:
      words = re.split('\s+', tmp[0].get_text().strip())
      wordType = tmp[1].strip()

      # handle nouns
      if wordType == 'n':
        print words
        nomCase = words[0]
        genCase = words[1]
        
        # handle first declension
        if nomCase.endswith('a') and genCase.endswith('ae'):
            # first declension unknown gender
            stem = nomCase[:-1]
            for i in range(0,6):
              tmpWordSg = stem + firstDeclensionEndingsSg[i]
              tmpWordPl = stem + firstDeclensionEndingsPl[i]
              print tmpWordSg
              print tmpWordPl              
        # handle second declension
        else if nomCase.endswith('us') and genCase.endswith('i'):
            # second declension nominative
            stem = nomCase[:-2]
            for i in range(0,6):
              tmpWordSg = stem + seconDeclensionEndingsMFSg[i]
              tmpWordPl = stem + secondDeclensionEndingsMFPl[i]
        else if nomCase.endswith('um') and genCase.endswith('i'):
            stem = nomCase[:-2]
            for i in range(0,6): 
              tmpWordSg = stem + secondDeclensionEndingsNSg[i]
              tmpWordPl = stem + secondDeclensionEndingsNPl[i]
        else if nomCase.endswith('r') and genCase.endswith('i'):
            stem = genCae[:-1]
            for i in range(0,6):
              if secondDeclensionEndingsMFSg[i] == '-':
                tmpWordSg = nomCase
              else:
                tmpWordSg = stem + secondDeclensionEndingsMFSg[i]
              tmpWordPl = stem + secondDeclensionEndingsMFPl[i]
  
        # handle third declension
        else if genCase.endswith('is'):
            # look up what gender it is
            print "third declension"
        
        # handle fourth declension
        else if nomCase.endswith('us') and genCase.endswith('us'):
          stem = genCase[:-2]
          for i in range(0,6):
            tmpWordSg = stem + fourthDeclensionEndingsMFSg[i]
            tmpWordPl = stem + fourthDeclensionEndingsMFPl[i]
        else if nomCase.endswith('u') and genCase.endswith('us'):
          stem = genCase[:-2]
          for i in range(0,6):
            tmpWordSg = stem + fourthDeclensionEndingsNSg[i]
            tmpWordPl = stem + fourthDeclensionEndingsNPl[i]
        
        # handle the fifth declension
        else if nomCase.endswith('es') and genCase.endswith('ei'):
          stem = genCase[:-2]
          for i in range(0,6):
            tmpWordSg = stem + fifthDeclensionEndingsMFSg[i]
            tmpWordPl = stem + fifthDeclensionEndingsMFPl[i]

    else:
      print tmp[0]
      # add this to list of words
