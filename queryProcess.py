"""
This will process queries
0. Read from indexes and hold them in memory ( global index dictionary )
1. Determine tf-idf scores
2. Compare the results for multiple queries
3. return a list of documents to return
"""
import linecache
import re
import math
from numpy import dot
from numpy.linalg import norm


def weightTerm(term, termtuples, weightTotal): # term, (doc, tf), dictionary
   """

   determines weight of individual term
   returns list of tuples [(doc, weight)]
   """
   TOTAL_DOCUMENTS = 55393 # Number of docterm lines
   df = len(termtuples)
   idf = math.log(TOTAL_DOCUMENTS/df)

   for i in termtuples:
      tf = float(i[1])
      tfidf = tf * idf
      if term not in weightTotal.keys():
         weightTotal[term] = {}
         weightTotal[term][i[0]] = tfidf
      else:
         weightTotal[term][i[0]] = tfidf
   return weightTotal



def rank(weightTerms, termtuples, querylist):
   """
   ranks documents based on cosine similarity
   {doc: [ tfidf vector ]}
   returned by processQuery
   """
   TOTAL_DOCUMENTS = 55393 # Number of docterm lines

   ranklist = {} # { doc: similarity }
   queryfreq = {}
   cosineVals = {} #{ document: [] }
   docset = set()

   for x in weightTerms.values(): # determines a set of documents, removing repeats
      for y in x:
         docset.add(y)

   for x in querylist: # determines tf for each term in query
         if x not in queryfreq.keys():
            queryfreq[x] = 1
         else:
            queryfreq[x] += 1

   for i in set(querylist): # determines tf-idf values for each in the query
      if i not in termtuples.keys():
         termtuples[i] = 1 ####
         if "MaliaQUERY" not in cosineVals.keys():
            cosineVals["MaliaQUERY"] = [0]
            pass
         else:
            cosineVals["MaliaQUERY"].append(0)
            pass

      elif "MaliaQUERY" not in cosineVals.keys():
         cosineVals['MaliaQUERY'] = [queryfreq[i] * math.log( TOTAL_DOCUMENTS/ termtuples[i])]
      else:
         cosineVals["MaliaQUERY"].append(queryfreq[i] * math.log( TOTAL_DOCUMENTS/ termtuples[i]))

   for i in set(querylist):
      for x in docset:
         if x not in cosineVals.keys():
            cosineVals[x] = []
         if i not in weightTerms.keys():
            cosineVals[x].append(0)
         elif x not in weightTerms[i].keys():
            cosineVals[x].append(0)
         else:
            cosineVals[x].append(weightTerms[i][x])


   ### COSINE SIMILARITY
   for i in cosineVals.keys():
      if i == "MaliaQUERY":
         pass
      else:
         ranklist[i] = dot(cosineVals[i], cosineVals["MaliaQUERY"])/(norm(cosineVals[i])*norm(cosineVals["MaliaQUERY"]))

   return ranklist



def retrive(maxindex):
   """
   prints the name of each document in list to specified index
   returned by processQuery
   """
   orderedDict = sorted(maxindex.items(), key=lambda x: x[1], reverse=True)

   orderedList = []
   for i in orderedDict:
      orderedList.append(linecache.getline('docterms', i[0]).split()[1])

   if len(orderedList) > 5:
      return orderedList[:5]

   return orderedList



def hash(term):
   """
   This is used to determine which indexfile (0-7) to search in order to find a term in the query
   """
   hashvalue = 0
   for i in term:
      hashvalue += ord(i)
   hashvalue = hashvalue % 8
   return hashvalue



def processQuery(QueryList: list):
   """
   Receives a list of queries
   for each list, determines the hash value of each term and compiles a set of doc tuples.
   {term: (documents, score) }
   """
   indexlistOpen = open("indexlist", "r")
   indexlist = indexlistOpen.readlines()
   indexlistOpen.close()

   QueryDict = {} # { term : indexfile line }

   for i in QueryList: #
      startSearch = int(indexlist[hash(i)].strip()) ####
      while startSearch < 78006: # last line of indexer
         check = linecache.getline("indexIndex", startSearch ).split() # starts at beginning of index i and checks for term
         if i+':' == check[0]:
            QueryDict[i] = check[1:] # adds line number term can be found on in respective index file
            break
         # else indexed term it moves onto next queried term
         startSearch += 1 # advances to next line

   if not QueryDict:
      print("No results found.")
      return []

   weightlist = {} # {term : {doc: weights} }
   df = {} # {term: document frequency}

   for i in QueryDict.keys():
      x = linecache.getline("index"+str(hash(i)), int(QueryDict[i][0]) + 1) # get term: ( doc : TF ) line from index
      # gets all the tuples for the term
      x = re.findall(r'(\(.*?,.*?\))', x)
      x = [eval(y) for y in x] # reads the x as tuples
      df[i] = len(x)
      weightlist = weightTerm(i , x, weightlist) # sends term, all docs associated, and dictionary

   return retrive(rank(weightlist, df, QueryList))
