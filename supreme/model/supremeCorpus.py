from convokit.model import *
from typing import List, Optional
import json
from nltk.tokenize import sent_tokenize


class SupremeCorpus(Corpus):
    """
    This initializer overrides default initializer to load specific year from full corpus.
    This only processes json lines which contain year in the range in the case-id,
    and avoids processing the whole file before filtering by year.
    This can also be done by downloading year specific supreme-corpus from Cornell repo.
    This constructor can also accept path to any smaller utterance json file taken from
    the larger corpus.

    :param uttfile: Path to the file containing utterance json
    :param minyear: Year of utterance to begin corpus with
    :param maxyear: Year of utterance to end corpus with
    :param filename: Path to a folder containing a Corpus or to an utterances.jsonl / utterances.json file to load
    :param utterances: list of utterances to initialize Corpus from
    :param preload_vectors: list of names of vectors to be preloaded from directory; by default,
        no vectors are loaded but can be loaded any time after corpus initialization (i.e. vectors are lazy-loaded).
    :param utterance_start_index: if loading from directory and the corpus folder contains utterances.jsonl, specify the
        line number (zero-indexed) to begin parsing utterances from
    :param utterance_end_index: if loading from directory and the corpus folder contains utterances.jsonl, specify the
        line number (zero-indexed) of the last utterance to be parsed.
    :param merge_lines: whether to merge adjacent lines from same speaker if multiple consecutive utterances belong to
        the same conversation.
    :param exclude_utterance_meta: utterance metadata to be ignored
    :param exclude_conversation_meta: conversation metadata to be ignored
    :param exclude_speaker_meta: speaker metadata to be ignored
    :param exclude_overall_meta: overall metadata to be ignored

    :ivar meta_index: index of Corpus metadata
    :ivar vectors: the vectors stored in the Corpus
    :ivar corpus_dirpath: path to the directory the corpus was loaded from
    """

    def __init__(self, dirname: str, uttfile: Optional[str] = None,
                 minyear: int = None, maxyear: int = None,
                 utterances: Optional[List[Utterance]] = None,
                 preload_vectors: List[str] = None,
                 utterance_start_index: int = None,
                 utterance_end_index: int = None, merge_lines: bool = False,
                 exclude_utterance_meta: Optional[List[str]] = None,
                 exclude_conversation_meta: Optional[List[str]] = None,
                 exclude_speaker_meta: Optional[List[str]] = None,
                 exclude_overall_meta: Optional[List[str]] = None,
                 disable_type_check=True):

        minyear = 0 if (minyear is None) else minyear
        maxyear = float('inf') if (maxyear is None) else maxyear
        self.meta_index = ConvoKitIndex(self)
        self.meta = ConvoKitMeta(self.meta_index, 'corpus')

        # private storage
        self._vector_matrices = dict()
        if exclude_utterance_meta is None: exclude_utterance_meta = []
        if exclude_conversation_meta is None: exclude_conversation_meta = []
        if exclude_speaker_meta is None: exclude_speaker_meta = []
        if exclude_overall_meta is None: exclude_overall_meta = []
        if utterance_start_index is None: utterance_start_index = 0
        if utterance_end_index is None: utterance_end_index = float('inf')

        with open(uttfile, "r") as f:
            utterances = []
            idx = 0

            for line in f:
                if idx >= utterance_end_index:
                    break
                if idx < utterance_start_index:
                    continue

                utjson = json.loads(line)
                utyear = int(utjson["meta"]["case_id"][0:4])
                if utyear < minyear:
                    continue
                if utyear > maxyear:
                    break
                i = 0
                utid = utjson["id"]
                for s in sent_tokenize(utjson["text"]):
                    ids = utid + "_" + str(i)
                    utjson["id"] = ids
                    utjson["text"] = s
                    utjson["meta"]["year"] = str(utyear)
                    utterances.append(utjson)

                    i = i + 0
                idx = idx + 1

        speakers_data = load_speakers_data_from_dir(dirname, exclude_speaker_meta)
        convos_data = load_convos_data_from_dir(dirname, exclude_conversation_meta)
        load_corpus_meta_from_dir(dirname, self.meta, exclude_overall_meta)

        self.utterances = dict()
        self.speakers = dict()

        initialize_speakers_and_utterances_objects(self, self.utterances, utterances, self.speakers, speakers_data)
        # skipping this for performancee
        # self.meta_index.enable_type_check()

        with open(os.path.join(dirname + "/index.json"), "r") as f:
            idx_dict = json.load(f)
            self.meta_index.update_from_dict(idx_dict)

        unpack_binary_data_for_utts(utterances, dirname, self.meta_index.utterances_index,
                                    exclude_utterance_meta, KeyMeta)
        # unpack binary data for speakers
        unpack_binary_data(dirname, speakers_data, self.meta_index.speakers_index, "speaker",
                           exclude_speaker_meta)

        # unpack binary data for conversations
        unpack_binary_data(dirname, convos_data, self.meta_index.conversations_index, "convo",
                           exclude_conversation_meta)

        # unpack binary data for overall corpus
        unpack_binary_data(dirname, self.meta, self.meta_index.overall_index, "overall", exclude_overall_meta)

        self.conversations = initialize_conversations(self, self.utterances, convos_data)
        self.meta_index.enable_type_check()
        self.update_speakers_data()
