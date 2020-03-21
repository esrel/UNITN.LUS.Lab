class Node(object):

    def __init__(self, word=None):
        self.word = word
        self.children = {}
        self.count = 0

    def __set__(self, instance, value):
        self.instance = value

    def __get__(self, instance, owner):
        return self.instance


class Trie(object):

    def __init__(self):
        self.root = Node('*')  # trie root
        self.oov = Node()      # node for oov values
        self.size = 0          # depth of trie

    def __set__(self, instance, value):
        self.instance = value

    def __get__(self, instance, owner):
        return self.instance

    def add(self, sequence):
        node = self.root
        node.count += 1  # total word count
        for word in sequence:
            node.children[word] = node.children.setdefault(word, Node(word))
            node = node.children[word]
            node.count += 1

    def get(self, sequence):
        node = self.root
        for word in sequence:
            node = node.children.get(word, self.oov)
        return node

    def traverse(self, node=None, sequence=None, size=None):
        sequence = sequence if sequence else []
        node = self.root if not node else node

        if not node.children:
            yield sequence

        if size:
            if len(sequence) == size:
                yield sequence

        for word, n in node.children.items():
            sequence.append(word)
            yield from self.traverse(n, sequence, size=size)
            sequence.pop()

    def v(self, size=None):
        return len(list(self.traverse(size=size)))


class NgramModel(object):

    ZERO_LOG_PROB = -1000

    def __init__(self, corpus=None, n=2, smoothing=False, backoff=False):
        self.model = None
        if corpus:
            self.make(corpus, n=n, smoothing=smoothing, backoff=backoff)

    def __set__(self, instance, value):
        self.instance = value

    def __get__(self, instance, owner):
        return self.instance

    @staticmethod
    def ngrams(sequence, n=2):
        """
        returns ngrams as a list-of-lists of sequence elements
        :param sequence: list of elements
        :param n: ngram size to extract
        :return: list of ngrams
        """
        return [sequence[i:i + n] for i in range(len(sequence) - n + 1)]

    def count(self, corpus, n=2):
        """
        count ngrams in a corpus and stores in a Trie
        :param corpus: list-of-lists
        :param n: ngram size to count
        :return:
        """
        counts = Trie()
        for sequence in corpus:
            for ngram in self.ngrams(sequence, n=n):
                counts.add(ngram)
        return counts

    def make(self, corpus, n=2, smoothing=False, backoff=False):
        """
        compute ngram probabilities from frequency counts
        :param corpus: corpus to build ngram model for
        :param n: ngram size
        :param smoothing: additive smoothing on/ogg (only +1)
        :param backoff: deleted interpolation on/off (simplest form of back-off)
        :return: trie
        """
        from math import log

        # get ngram counts
        counts = self.count(corpus, n=n)

        # set meta-information
        counts.size = n               # meta-info: ngram-size
        counts.backoff = backoff      # meta-info: back-off  true|false
        counts.smoothing = smoothing  # meta-info: smoothing true|false

        # smoothing
        a, v = self.additive_smoothing(counts) if smoothing else (0, 0)
        # back-off weights
        counts.weights = self.deleted_interpolation(counts) if backoff else [0] * (n-1) + [1]

        # update oov probability:
        counts.oov.probability = log(a/v) if smoothing else self.ZERO_LOG_PROB

        # compute probabilities from counts for every ngram <= n
        for ngram in counts.traverse():
            for i in range(len(ngram)):
                n = counts.get(ngram[0:i+1])  # get ngram node
                p = counts.get(ngram[0:i])    # get parent node
                n.probability = log((n.count + a)/(p.count + v))

        self.model = counts

    @staticmethod
    def additive_smoothing(counts, a=1):
        """
        additive smoothing (laplace)
        :param counts: counts trie
        :param a: alpha to add; a = 1 --> +1 smoothing
        :return:
        """
        return a, (counts.v(size=counts.size - 1) * a)

    @staticmethod
    def deleted_interpolation(counts):
        """
        deleted interpolation
        :param counts: counts trie
        :return: interpolation weights for ngram models
        """
        w = [0] * counts.size
        for ngram in counts.traverse():
            # current ngram count
            v = counts.get(ngram).count
            # (n)-gram counts
            n = [counts.get(ngram[0:i+1]).count for i in range(len(ngram))]
            # (n-1)-gram counts -- parent node
            p = [counts.get(ngram[0:i]).count for i in range(len(ngram))]
            # - 1 from both counts & normalize
            d = [float((n[i]-1)/(p[i]-1)) if (p[i]-1 > 0) else 0.0 for i in range(len(n))]
            # increment weight of the max by raw ngram count
            k = d.index(max(d))
            w[k] += v
        return [float(v)/sum(w) for v in w]

    def score(self, sequence):
        """
        score a sequence using ngram model
        :param sequence: sentence as a list of tokens
        :return: value
        """
        probs = []
        for ngram in self.ngrams(sequence, self.model.size):
            n = self.model.get(ngram)
            p = n.probability

            # oov node check & back-off computation
            if n.word is None and self.model.backoff:
                p = sum([self.model.get(ngram[0:i + 1]).probability * self.model.weights[i] for i in range(len(ngram))])

            probs.append(p)
        return float(sum(probs))

    def generate(self, bos='<s>', eos='</s>'):
        """
        generate a random sequence from ngram model
        :param bos: beginning-of-sentence tag
        :param eos: end-of-sentence tag
        :return: sentence as list & log probability
        """
        import random
        word = bos
        sent = [bos] * (self.model.size - 1)
        while word != eos:
            node = self.model.get(sent[-(self.model.size - 1):])
            word = random.choice(list(node.children.keys()))
            sent.append(word)
        return sent


def log2p(value):
    from math import exp
    return exp(value) if value else 0.0


def nbest(d, n=1):
    """
    get n max values from a dict
    :param d: input dict (values are numbers, keys are stings)
    :param n: number of values to get (int)
    :return: dict of top n key-value pairs
    """
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:n])


def test_ngram():
    corpus = [
        ['the', 'cat', 'is', 'fat'],
        ['the', 'dog', 'is', 'not'],
        ['a', 'cat', 'is', 'on', 'the', 'mat'],
        ['an', 'elephant', 'is', 'in', 'the', 'closet']
    ]
    seqs = [['the', 'cat'], ['my', 'cat']]
    ngrams = NgramModel(corpus=corpus, n=2, smoothing=True)

    # test shorter ngrams (should be 0.0)
    assert ngrams.score(['cat']) == 0.0

    # test log prop and prob ranges
    for s in seqs:
        assert ngrams.score(s) <= 0.0
        assert 0.0 <= log2p(ngrams.score(s)) <= 1.0

    # test back-off computation
    assert ngrams.model.get(['is']).probability != ngrams.ZERO_LOG_PROB


def test_generation():
    corpus = [
        ['<s>', 'the', 'cat', 'is', 'fat', '</s>'],
        ['<s>', 'the', 'dog', 'is', 'not', '</s>'],
        ['<s>', 'a', 'cat', 'is', 'on', 'the', 'mat', '</s>'],
        ['<s>', 'an', 'elephant', 'is', 'in', 'the', 'closet', '</s>']
    ]
    ngrams = NgramModel(corpus=corpus, n=2, smoothing=True, backoff=True)
    for i in range(5):
        assert len(ngrams.generate()) > 2


if __name__ == '__main__':
    print("Testing Only...")
    test_ngram()
    test_generation()
    print("Done!")
