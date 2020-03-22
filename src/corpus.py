class Lexicon(object):

    def __init__(self, corpus=None):
        self.lexicon = None
        self.frequencies = None

        if corpus:
            self.create(corpus)

    def __eq__(self, other):
        return self.lexicon == other

    def __iter__(self):
        for token in sorted(list(self.lexicon)):
            yield token

    def __set__(self, instance, value):
        self.instance = value

    def __get__(self, instance, owner):
        return self.instance

    def __len__(self):
        return len(self.lexicon)

    def __str__(self):
        return "\n".join(sorted(list(self.lexicon)))

    def create(self, corpus):
        """
        compute lexicon of a corpus
        :param corpus: corpus as list-of-lists
        """
        self.lexicon = set([word for sent in corpus for word in sent])
        self.compute_frequency_list(corpus)

    def compute_frequency_list(self, corpus):
        """
        create frequency list for a corpus
        :param corpus: corpus as list of lists
        """
        frequencies = {}
        for sent in corpus:
            for token in sent:
                frequencies[token] = frequencies.setdefault(token, 0) + 1
        self.frequencies = frequencies

    def add(self, token):
        self.lexicon.add(token)

    def rm(self, token):
        if token in self.lexicon:
            self.lexicon.remove(token)

    def read(self, lexicon_file):
        """
        read lexicon into a list
        :param lexicon_file: lexicon file in token-per-line format
        """
        self.lexicon = set([line.strip() for line in open(lexicon_file, 'r')])

    def write(self, lexicon_file):
        """
        write lexicon into a list
        :param lexicon_file: lexicon file
        """
        with open(lexicon_file, 'w') as f:
            f.write("\n".join(sorted(list(self.lexicon))) + "\n")

    def cutoff(self, tf_min=1, tf_max=float('inf'), update=False):
        """
        apply min and max cutoffs to a frequency list

        :param tf_min: minimum token frequency for lexicon elements (below removed); default 1
        :param tf_max: maximum token frequency for lexicon elements (above removed); default infinity
        :param update: if to update lexicon (i.e. not to recreate it)
        """
        lexicon = set([token for token, frequency in self.frequencies.items() if tf_max >= frequency >= tf_min])
        self.lexicon = self.lexicon - (self.lexicon - lexicon) if update else lexicon

    def remove(self, stopwords=None):
        """
        remove stopwords from a lexicon
        :param stopwords: stopwords list
        """
        if stopwords:
            self.lexicon = self.lexicon - set(stopwords)


class Corpus(object):

    def __init__(self, corpus_file=None):
        self.corpus = None
        self.lexicon = None

        if corpus_file:
            self.read(corpus_file)
            self.lexicon = Lexicon(corpus=self.corpus)

    def __set__(self, instance, value):
        self.instance = value

    def __get__(self, instance, owner):
        return self.instance

    def __str__(self):
        out = ""
        for sent in self.corpus:
            out += " ".join(sent) + "\n"
        return out

    def __len__(self):
        return len(self.corpus)

    def __eq__(self, other):
        return self.corpus == other

    def __iter__(self):
        for sent in self.corpus:
            yield sent

    def read(self, corpus_file):
        """
        read corpus into a list-of-lists, splitting sentences into tokens by space (' ')
        :param corpus_file: corpus file in sentence-per-line format (tokenized)
        """
        self.corpus = [line.strip().split() for line in open(corpus_file, 'r')]
        self.lexicon = Lexicon(corpus=self.corpus)

    def write(self, corpus_file):
        """
        write corpus in a list-of-lists into a file
        :param corpus_file: corpus file for writing
        """
        with open(corpus_file, 'w') as f:
            for sent in self.corpus:
                f.write(" ".join(sent) + "\n")

    def pad(self, data=None, bos='<s>', eos='</s>', bosn=1, eosn=1):
        """
        add beginning-of-sentence (bos) or/and end-of-sentence (eos) tags

        :param data: corpus to process & return [optional]

        :param bos: beginning-of-sentence tag
        :param eos: end-of-sentence tag

        :param bosn: number of bos to add
        :param eosn: number of eos to add

        :return: processed corpus as list of lists
        """
        if data:
            return [[bos] * bosn + sent + [eos] * eosn for sent in data]
        else:
            self.corpus = [[bos] * bosn + sent + [eos] * eosn for sent in self.corpus]
            self.lexicon.add(bos)
            self.lexicon.add(eos)

    def oov(self, data=None,  unk='<unk>'):
        """
        replace all tokens that are not in lexicon with OOV symbol
        :param data: corpus to process & return (usually test)
        :param unk: OOV (unknown) symbol
        :return: processed corpus
        """
        if data:
            return [[token if token in self.lexicon else unk for token in sent] for sent in data]
        else:
            self.corpus = [[token if token in self.lexicon else unk for token in sent] for sent in self.corpus]
            self.lexicon.add(unk)


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
    lex = Lexicon(_corpus)

    # test creation/read
    assert lex == _lexicon
    assert lex.frequencies == _freq

    # __len__
    assert len(lex) == 13

    # Type checking
    assert type(lex.frequencies) == dict
    assert type(lex.lexicon) == set

    # Testing set add/rm operations
    assert _unk not in lex

    lex.add(_unk)
    assert _unk in lex

    lex.rm(_unk)
    assert _unk not in lex

    assert lex == _lexicon

    # testing remove
    lex.remove(_stopwords)
    assert lex == _lexicon - set(_stopwords)

    # testing cut-off
    lex.cutoff(tf_min=2)
    assert lex == {'the', 'cat', 'is'}

    lex.cutoff(tf_max=3)
    assert lex == {'an', 'mat', 'in', 'dog', 'elephant', 'a', 'closet', 'cat', 'not', 'on', 'fat'}

    lex.cutoff(tf_min=2, tf_max=3)
    assert lex == {'cat'}

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
