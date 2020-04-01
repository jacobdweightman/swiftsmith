from .expression import Expression
from .semantics import SemanticParseTree
from .standard_library import Int

import copy
import random

# A metamorphic relation describes the relationship between inputs and outputs of a
# program. This allows a program to be tested without knowing what its exact output
# should be (the oracle problem), or can be used to create new tests from existing
# ones.

# In SwiftSmith, a metamorphic relation is a semantics-preserving transformation on
# a Swift program. That is, given one Swift program, it produces another one with
# slightly different source code that should behave identically. In this way, we're
# able to detect potential miscompilations where these tranformations actually do
# change program behavior.

def unnecessary_addition(parsetree: SemanticParseTree) -> SemanticParseTree:
    """
    Given an `Int` expression `e`:

    `e` can be replaced in a program with `(e) + 0`
    """
    parsetree = copy.deepcopy(parsetree)
    intexpr = Expression(Int)
    candidates = [node for node in parsetree if node == intexpr]
    target = random.choice(candidates)
    expressiontree = target.annotations["subtree"]
    expressiontree = SemanticParseTree(intexpr, ["(", expressiontree, ") + 0"])
    target.annotations["subtree"] = expressiontree
    return parsetree


def unnecessary_multiplication(parsetree: SemanticParseTree) -> SemanticParseTree:
    """
    Given an `Int` expression `e`:

    `e` can be replaced in a program with `(e) * 1`
    """
    parsetree = copy.deepcopy(parsetree)
    intexpr = Expression(Int)
    candidates = [node for node in parsetree if node == intexpr]
    target = random.choice(candidates)
    expressiontree = target.annotations["subtree"]
    expressiontree = SemanticParseTree(intexpr, ["(", expressiontree, ") * 1"])
    target.annotations["subtree"] = expressiontree
    return parsetree
