import re
from string import punctuation
import pandas as pd



def clean_text(text):
  
  
  text = re.sub("[%s]"% re.escape(punctuation), "", text)
  text = text.lower()
  text = re.sub(r"\w*\d\w*", "",text)
  #text = re.sub(r"[åäö]", "", text)
 

  stopword = [stopword.strip() for stopword in open("./stopwords/stop_words_sve.txt")]
  return " ".join([word for word in text.split()if word not in stopword])

#text = "Jag är en sträng, OCH NI SKriver jag med STORA BOKSTÄVER 1987, honom som jag han!!! sommaren är kort. det regnar bort  "

#new_text = clean_text(text)
#print(new_text)
