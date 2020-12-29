"""
This deals with the interface that users will interact with
"""
import user_query_tokenizer
import queryProcess
import time
from zipfile import ZipFile
import json

def main():
   developerzip = ZipFile("developer.zip", "r")

   while 1:
      query = input("Insert your query: ")
      print("")
      if query == "main.py QUIT":
         print("Goodbye")
         return 0

      start = time.process_time()      # start timer
      doclist = queryProcess.processQuery(user_query_tokenizer.tokenize(query)) # query is processed 1st

      for i in doclist: # doclist is simply formatted as the name of the document but unclickable in current state
         result = json.loads(developerzip.read(i))
         print(result['url'])

      print("{} ms\n".format( (time.process_time() - start)*1000) )  # end timer
   return 0 # no errors

main()
