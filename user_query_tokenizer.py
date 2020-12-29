import nltk
import string

def tokenize(query):
   """
   1. receives a user query or more
   2. tokenizes query
   3. identifies boolean AND
   4. returns a list of lists containing tokens per query
   """
   STOP = open("stopwords","r")
   STOP = STOP.read().strip()
   PORTER = nltk.PorterStemmer()
   #queryTokens = [] # return this

   query = query.split()
   querylist = []
   for x in query:
      candidate = ""
      for i in x:
         if (i in string.ascii_letters):
            candidate += i.lower()
         elif (i not in string.printable):
            pass
      if (candidate not in STOP) and (candidate != ""):
         querylist.append(PORTER.stem(candidate))
   #queryTokens.append(querylist)


   return querylist
