from itertools import product

def _identifiers():
    """
    Enumerates identifiers for use in generated code.
    """

    # List of reserved keywords, from
    # https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html
    reserved = {
        "associatedtype", "class", "deinit", "enum", "extension", "fileprivate", "func",
        "import", "init", "inout", "internal", "let", "open", "operator", "private",
        "protocol", "public", "rethrows", "static", "struct", "subscript", "typealias",
        "var", "break", "case", "continue", "default", "defer", "do", "else",
        "fallthrough", "for", "guard", "if", "in", "repeat", "return", "switch",
        "where", "while", "as", "Any", "catch", "false", "is", "nil", "super", "self",
        "Self", "throw", "throws", "true", "try", "_"
    }
    letters = "abcdefghijklmnopqrstuvwxyz"
    length = 1
    while True:
        for i in product(letters, repeat=length):
            i = "".join(i)
            if i not in reserved:
                yield "".join(i)
        length += 1

identifier = _identifiers()