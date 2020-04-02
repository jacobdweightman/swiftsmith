from .expression import Expression
from .semantics import SemanticParseTree
from .standard_library import Int

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

def unnecessary_addition(parsetree: SemanticParseTree):
    """
    Given an `Int` expression `e`:

    `e` can be replaced in a program with `(e) + 0`
    
    Note: this function mutates the given parse tree.
    """
    intexpr = Expression(Int)
    candidates = [node for node in parsetree if node == intexpr]
    target = random.choice(candidates)
    tree = target.annotations["subtree"]
    newtree = SemanticParseTree(intexpr, ["(", tree, ") + 0"])
    target.annotations["subtree"] = newtree


def unnecessary_multiplication(parsetree: SemanticParseTree):
    """
    Given an `Int` expression `e`:

    `e` can be replaced in a program with `(e) * 1`

    Note: this function mutates the given parse tree.
    """
    intexpr = Expression(Int)
    candidates = [node for node in parsetree if node == intexpr]
    target = random.choice(candidates)
    tree = target.annotations["subtree"]
    newtree = SemanticParseTree(intexpr, ["(", tree, ") * 1"])
    target.annotations["subtree"] = newtree
