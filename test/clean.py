import convokit
from convokit.text_processing import TextProcessor
import json
from convokit.text_processing import TextParser

# Your convokit home
CONVOKIT_HOME= "/Users/rmundhe/.convokit"
ROOT_DIR = CONVOKIT_HOME + "/downloads/supreme-corpus"

# basic cleanup for raw text file
def preprocess_text(text):
    text = text.replace('--', ' ')
    text = text.replace('\n', ' ')
    return text

textprep = TextProcessor(proc_fn=preprocess_text, output_field='clean_text')
texttagger = TextParser(output_field='tagged', input_field='clean_text', mode='tag')

uttfile = ROOT_DIR + "/utterances.jsonl"

# print("initializing corpus. this may take a minute.")
# corpus = convokit.Corpus(ROOT_DIR)
print("initializing sample corpus.")
corpus = convokit.Corpus(ROOT_DIR, utterance_end_index=500)
print("corpus initialized")

count = 0
y = 1955
# assuming utterance file sorted by year
for u in corpus.iter_utterances():
  count = count + 1
  year = u.meta["case_id"][0:4]
  # clean and tag utterance
  u = textprep.transform_utterance(u)
  u = texttagger.transform_utterance(u)
  print("utterance ", year, " ", u.id)

  # save json
  jsonfile = "data/tagged"+ year +".json"
  ft=open(jsonfile, "a")
  ft.write(",")
  ft.write(json.dumps(u.meta))

  # save text
  filename="data/raw"+ year +".txt"
  f = open(filename, "a")
  f.write("\n")
  sp = u.get_speaker().meta
  if sp["name"] != "":
    name = sp["name"].replace('.', '')
    f.write(name)
    f.write(": ")
  f.write(u.retrieve_meta('clean_text'))
  if y < int(year):
    print("finished year ", year)
    f.close()
    ft.close()
    y = year

print("utterances processed ", count)
