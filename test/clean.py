# helper function to plot two coordination scores against each other as a chart,
#   on aggregate and by coordination marker
# a is a tuple (speakers, targets)
# b is a tuple (speakers, targets)
import convokit
from convokit import Utterance, Corpus, Coordination, download
from convokit.text_processing import TextProcessor

from convokit.text_processing import TextParser
ROOT_DIR = "<Convokit-home>/.convokit/downloads/supreme-2019"
corpus = convokit.Corpus(ROOT_DIR,utterance_end_index=199)


test_utt_id = '24929__0_007'

def preprocess_text(text):
    text = text.replace(' -- ', ' ')
    return text

# corpus = Corpus(filename=download("supreme-2019"))
prep = TextProcessor(proc_fn=preprocess_text, output_field='clean_text')
corpus = prep.transform(corpus)
parser = TextParser(input_field='clean_text', verbosity=50)
corpus = parser.transform(corpus)

utt = corpus.get_utterance(test_utt_id)
print(utt.meta)
print(utt.retrieve_meta('clean_text'))

test_parse = utt.retrieve_meta('parsed')
print(test_parse[0])