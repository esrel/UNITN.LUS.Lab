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
