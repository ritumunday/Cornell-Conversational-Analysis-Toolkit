# helper function to plot two coordination scores against each other as a chart,
#   on aggregate and by coordination marker
# a is a tuple (speakers, targets)
# b is a tuple (speakers, targets)
import convokit
import nltk
from convokit.model import corpusHelper
from convokit import Utterance, Corpus, Coordination, download
from convokit.text_processing import TextProcessor
import json
from convokit.text_processing import TextParser
# ROOT_DIR = download("supreme-2019")
ROOT_DIR = "/Users/rmundhe/.convokit/downloads/supreme-2019"
# corpus = convokit.Corpus(ROOT_DIR,utterance_end_index=100)
corpus = convokit.Corpus(ROOT_DIR)
# nltk.download('punkt')


def preprocess_text(text):
    text = text.replace('--', ' ')
    text = text.replace('\n', ' ')
    return text

# corpus = Corpus(filename=download("supreme-2019"))
prep = TextProcessor(proc_fn=preprocess_text, output_field='clean_text')
corpus = prep.transform(corpus)
# parser = TextParser(input_field='clean_text', verbosity=50)
# corpus = parser.transform(corpus)

utt = corpus.random_utterance()
print(utt.meta)
print(utt.retrieve_meta('clean_text'))
sp = utt.get_speaker().meta
print(sp["name"])
# test_parse = utt.retrieve_meta('parsed')
# print(test_parse[2])

# texttagger = TextParser(output_field='tagged', input_field='clean_text', mode='tag')
# corpus = texttagger.transform(corpus)
# print(utt.retrieve_meta('tagged')[0])

for u in corpus.iter_utterances():
  filename="raw"+u.meta["case_id"]+".txt"
  f = open(filename, "a")
  f.write("\n")
  sp = u.get_speaker().meta
  if sp["name"] != "":
    name = sp["name"].replace('.', '')
    f.write(name)
    f.write(": ")
  f.write(u.retrieve_meta('clean_text'))


f.close()
