from itertools import product

def _identifiers():
    """
    Enumerates identifiers for use in generated code.
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    length = 1
    while True:
        for i in product(letters, repeat=length):
            yield "".join(i)
        length += 1

identifier = _identifiers()