import argparse
import string


def fst_write(fst, fname, fs=" "):
    # fst contains final state
    with open(fname, 'w') as f:
        for arc in fst:
            f.write(fs.join(map(str, arc)) + "\n")


def st_write(st, fname, fs="\t"):
    with open(fname, 'w') as f:
        for symbol, idx in st.items():
            f.write(fs.join([symbol, idx]) + "\n")


def fst_word2char(symbol_table, eps='<epsilon>'):
    """
    create a character-level lexicon from corpus in list of lists format
    from OpenFST examples
    :param symbol_table: fst symbol table
    :param eps: epsilon transition symbol
    :return:
    """
    s = 0  # state
    arcs = []
    for line in open(symbol_table, 'r'):
        cols = line.split()
        if cols[1] == '0':
            continue  # epsilon
        word = cols[0]
        chars = list(word)

        for i in range(len(chars)):
            if i == 0:
                # first character of a word
                arcs.append([0, s + 1, chars[i], word])
            else:
                s += 1
                arcs.append([s, s + 1, chars[i], eps])
        s += 1  # final state
        arcs.append([s])
    return arcs


def fst_norm_digits(sym='<d>'):
    s = 0
    arcs = []
    for char in string.digits:
        arcs.append([s, s, char, sym])
    arcs.append([s])
    return arcs


def fst_norm_puncts(sym='<p>'):
    s = 0
    arcs = []
    for char in string.punctuation:
        arcs.append([s, s, char, sym])
    arcs.append([s])
    return arcs


def st_ascii():
    """
    create ascii symbol table
    """
    syms = {"<epsilon>": 0}
    for i in range(128):
        char_str = chr(i)
        if char_str in string.whitespace:
            syms['<space>'] = i
        elif char_str in string.ascii_letters:
            syms[char_str] = i
        elif char_str in string.punctuation:
            syms[char_str] = i
        elif char_str in string.digits:
            syms[char_str] = i
        else:
            # Assume others are control characters.
            syms['<ctrl>'] = i
    return syms


def txt2fsa(txt):
    """
    generate an fsa of the input text (whitespace tokenization)
    :param txt: input string to generate automata for
    :return: fsa specification as string
    """
    sent = txt.strip().split()
    arcs = []
    for i, word in enumerate(sent):
        arcs.append([i, i+1, word])
    # add final state
    arcs.append([len(arcs)])
    return arcs


def create_argument_parser():
    """
    Create generic argument parser
    :return:
    """
    parser = argparse.ArgumentParser(description="OpenFST Utility Functions", prog='PROG')

    parser.add_argument('-d', '--data', help="data (rules) file path")
    parser.add_argument('-t', '--task', choices=['charlex'])  #, default='run')

    return parser


if __name__ == '__main__':
    parser = create_argument_parser()
    args = parser.parse_args()

