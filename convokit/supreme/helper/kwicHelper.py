from functools import reduce
from convokit.phrasing_motifs import QuestionSentences
from convokit.supreme.text_processing.modalSentences import ModalSentences
from convokit.text_processing import TextParser, TextToArcs
from convokit.text_processing import TextProcessor


class KwicHelper:
    """
    Object with functionality for modal searches in sentences.
    """

    def __init__(self, corpus, separator, resultfile):
        print("Started processing")
        self.corpus = corpus
        self.loadcorpus()
        self.modalkwic(separator, resultfile)
        print("Finished processing")

    """
    Basic cleanup function for raw sentences
    :param text: 
    :return: cleaned text
    """

    def prep_text(self, text):
        text = text.replace(' --', '... ')
        text = text.replace('--', '... ')
        text = text.replace('\n', ' ')
        return text

    """
    Loads corpus by sentence and prepares model for modal search. 
    Todo: Change this to pipeline.
    """

    def loadcorpus(self):

        print("========================================================================")
        print("Cleaning sentences")
        # Clean sentence text
        textprep = TextProcessor(proc_fn=self.prep_text, output_field='clean_text')
        self.corpus = textprep.transform(self.corpus)

        print("Tokenizing sentences")
        # Tokenize
        texttagger = TextParser(output_field='parsed', input_field='clean_text', mode='parse')
        self.corpus = texttagger.transform(self.corpus)

        print("Filtering question sentences")
        # Filter questions
        transformer = QuestionSentences(input_field='parsed', output_field='questions', use_caps=True)
        self.corpus = transformer.transform(self.corpus)

        print("Filtering modal sentences")
        # Filter questions
        transformer = ModalSentences(input_field='parsed', output_field='ismodal')
        self.corpus = transformer.transform(self.corpus)

    """
    Searches for modals and main verbs and generates excel file for KWIC analysis. 
    """

    def modalkwic(self, separator, resultfile):
        print("Creating KWIC")
        ft = open(resultfile, "w")
        # header row
        ft.write(
            "Year" + separator + "Sentence ID" + separator + "Before" + separator + "Mod" + separator + "After" + separator + "Main Verb" + separator + "Passive" + separator + "Speaker" + separator + "Role" + "\n")
        print("========================================================================")
        # assuming utterance file is sorted by year, iterate. Skip all non questions and non modals.
        for u in self.corpus.iter_utterances(lambda u: u.meta["ismodal"] == 1 and u.meta["questions"] != []):

            parsedsents = u.meta["parsed"]
            cleantext = u.meta["clean_text"]

            for parsedsent in parsedsents:
                # Find first main verb after modal in the sentence, skipping passive auxiliaries
                if len(parsedsent):
                    fileline = mod = first = last = ""
                    unmatchedmodal = passive = i = 0
                    # sentence
                    for tokenized in parsedsent["toks"]:
                        # word
                        if tokenized["tag"] == "MD":
                            mod = tokenized["tok"]
                            toks = list(map(lambda x: x['tok'], parsedsent["toks"]))
                            # tags = list(map(lambda x: x['tag'], parsedsent[0]["toks"]))
                            first = "" if i == 0 else reduce((lambda x, y: x + " " + y), toks[0:i])
                            last = "" if i == len(toks) - 1 else reduce((lambda x, y: x + " " + y),
                                                                        toks[i + 1:len(toks)])
                            unmatchedmodal = 1

                        # Skip aux passive verb
                        if tokenized["tag"] == "VB" and tokenized["dep"] == "auxpass":
                            passive = 1
                            print("Passive detected:", cleantext)

                        # Find modal main verb
                        if ((tokenized["tag"] == "VB" and passive == 0) or
                            ((passive == 1) and (tokenized["tag"] == "VBN"))) and unmatchedmodal == 1:
                            vb = tokenized["tok"]
                            fileline = u.meta[
                                           "year"] + separator + u.id + separator + first + separator + mod.lower() + separator + last + separator + vb.lower() + separator + str(
                                passive) + separator + \
                                       u.speaker.meta['name'] + separator + u.speaker.meta['type'] + "\n"
                            ft.write(fileline)
                            fileline = mod = first = last = ""
                            passive = 0
                            unmatchedmodal = 0

                        i = i + 1
        print("========================================================================")
        print("Result file saved in supreme/results folder.")
        print("========================================================================")
        ft.close()
