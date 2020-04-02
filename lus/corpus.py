class Lexicon(object):

    @staticmethod
    def read(lexicon_file):
        """
        read lexicon into a list
        :param lexicon_file: lexicon file in token-per-line format
        :return: lexicon
        """
        return set([line.strip() for line in open(lexicon_file, 'r')])

    @staticmethod
    def write(lexicon, lexicon_file):
        """
        write lexicon into a list
        :param lexicon: lexicon
        :param lexicon_file: lexicon file
        """
        with open(lexicon_file, 'w') as f:
            f.write("\n".join(sorted(list(lexicon))) + "\n")

    @staticmethod
    def create(corpus):
        """
        compute lexicon of a corpus
        :param corpus: corpus as list-of-lists
        :return:
        """
        return set([word for sent in corpus for word in sent])

    @staticmethod
    def compute_frequency_list(corpus):
        """
        create frequency list for a corpus
        :param corpus: corpus as list of lists
        :return:
        """
        frequencies = {}
        for sent in corpus:
            for token in sent:
                frequencies[token] = frequencies.setdefault(token, 0) + 1
        return frequencies

    @staticmethod
    def remove(lexicon, stopwords=None):
        """
        remove stopwords from a lexicon
        :param lexicon: lexicon as set
        :param stopwords: stopwords list
        """
        return lexicon - set(stopwords) if stopwords else lexicon

    @staticmethod
    def cutoff(corpus, lexicon=None, tf_min=1, tf_max=float('inf')):
        """
        apply min and max cutoffs to a frequency list
        :param corpus: corpus to use for computing frequencies
        :param lexicon: lexicon to operate on
        :param tf_min: minimum token frequency for lexicon elements (below removed); default 1
        :param tf_max: maximum token frequency for lexicon elements (above removed); default infinity
        """
        frequencies = Lexicon.compute_frequency_list(corpus)
        new_lexicon = set([token for token, frequency in frequencies.items() if tf_max >= frequency >= tf_min])
        return set(lexicon) - (new_lexicon - set(lexicon)) if lexicon else new_lexicon


class Corpus(object):

    @staticmethod
    def read(corpus_file):
        """
        read corpus into a list-of-lists, splitting sentences into tokens by space (' ')
        :param corpus_file: corpus file in sentence-per-line format (tokenized)
        """
        return [line.strip().split() for line in open(corpus_file, 'r')]

    @staticmethod
    def write(corpus, corpus_file):
        """
        write corpus in a list-of-lists into a file
        :param corpus: corpus to write
        :param corpus_file: corpus file for writing
        """
        with open(corpus_file, 'w') as f:
            for sent in corpus:
                f.write(" ".join(sent) + "\n")

    @staticmethod
    def pad(corpus, bos='<s>', eos='</s>', bosn=1, eosn=1):
        """
        add beginning-of-sentence (bos) or/and end-of-sentence (eos) tags

        :param corpus: corpus to process & return [optional]

        :param bos: beginning-of-sentence tag
        :param eos: end-of-sentence tag

        :param bosn: number of bos to add
        :param eosn: number of eos to add

        :return: processed corpus as list of lists
        """
        return [[bos] * bosn + sent + [eos] * eosn for sent in corpus]

    @staticmethod
    def oov(corpus, lexicon, unk='<unk>'):
        """
        replace all tokens that are not in lexicon with OOV symbol
        :param corpus: corpus to process & return (usually test)
        :param lexicon: lexicon to keep
        :param unk: OOV (unknown) symbol
        :return: processed corpus
        """
        return [[token if token in lexicon else unk for token in sent] for sent in corpus]


_corpus = [
    ['the', 'cat', 'is', 'fat'],
    ['the', 'dog', 'is', 'not'],
    ['a', 'cat', 'is', 'on', 'the', 'mat'],
    ['an', 'elephant', 'is', 'in', 'the', 'closet']
]

_lexicon = {'a', 'an', 'cat', 'closet', 'dog', 'elephant', 'fat', 'in', 'is', 'mat', 'not', 'on', 'the'}
_freq = {'the': 4, 'cat': 2, 'is': 4, 'fat': 1,
         'dog': 1, 'not': 1, 'a': 1, 'on': 1, 'mat': 1,
         'an': 1, 'elephant': 1, 'in': 1, 'closet': 1}


_stopwords = ['the', 'a', 'an', 'is', 'in', 'on', 'not']

_unk = '<unk>'


def test_lexicon():
    lex = Lexicon()
    lexicon = lex.create(_corpus)
    freqlst = lex.compute_frequency_list(_corpus)

    # test creation/read
    assert lexicon == _lexicon
    assert freqlst == _freq

    assert len(lexicon) == 13

    # Type checking
    assert type(freqlst) == dict
    assert type(lexicon) == set

    # testing remove
    lexicon_sw = lex.remove(lexicon, _stopwords)
    assert lexicon_sw == _lexicon - set(_stopwords)

    # testing cut-off
    assert lex.cutoff(_corpus, tf_min=2) == {'the', 'cat', 'is'}
    assert lex.cutoff(_corpus, tf_max=3) == {'an', 'mat', 'in', 'dog', 'elephant', 'a',
                                             'closet', 'cat', 'not', 'on', 'fat'}
    assert lex.cutoff(_corpus, tf_min=2, tf_max=3) == {'cat'}

    # testing cutoff update
    lex.cutoff(tf_min=2)
    assert lex == {'the', 'cat', 'is'}
    lex.cutoff(tf_max=3, update=True)
    assert lex == {'cat'}


def test_corpus():
    corp = Corpus()
    corp.corpus = _corpus
    corp.lexicon = Lexicon(_corpus)

    assert isinstance(corp, Corpus)
    assert isinstance(corp.lexicon, Lexicon)

    assert corp == _corpus

    assert len(corp) == 4

    # testing oov
    corp.lexicon.remove(_stopwords)
    assert corp.lexicon == (_lexicon - set(_stopwords))
    corp.oov()
    assert _unk in corp.lexicon

    # testing padding
    bos = '<s>'
    eos = '</s>'
    corp.pad()
    assert bos in corp.lexicon and eos in corp.lexicon

    for sent in corp:
        assert sent[0] == bos and sent[-1] == eos

    corp.pad(bosn=2)
    for sent in corp:
        assert sent[0:3] == [bos] * 3 and sent[-1] == eos


def test_corpus_external():
    sent = [['my', 'cat']]
    corp = Corpus()
    corp.corpus = _corpus
    corp.lexicon = Lexicon(_corpus)

    sent_oov = corp.oov(data=sent)
    assert sent_oov == [['<unk>', 'cat']]

    sent_tag = corp.pad(data=sent)
    assert sent_tag == [['<s>', 'my', 'cat', '</s>']]

    sent_pro = corp.pad(data=corp.oov(data=sent))
    assert sent_pro == [['<s>', '<unk>', 'cat', '</s>']]


if __name__ == '__main__':
    print("Testing Only...")
    test_lexicon()
    test_corpus()
    test_corpus_external()
    print("Done!")
