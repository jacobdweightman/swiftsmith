# SwiftSmith

SwiftSmith is a tool for generating random, valid programs in the Swift programming language. It is part of an ongoing research project in testing the Swift compiler. It attempts to make a few guarantees about the behavior of the generated programs:

1. Generated programs are "finite" and program generation halts.
2. Programs are valid in the sense that they compile successfully, though may (and probably do) contain warnings.
3. All functions exposed by the generated programs can run on any inputs of the correct types, and will halt.

## Supported Language Features

SwiftSmith generates programs that use a subset of Swift language features. This makes it easier to control the structure of generated programs and ensure that the above requirements are met.

Features that are currently supported are:
* function declarations
* variable declarations
* enum type declarations without raw values
* enum case declarations without associated values
* if/else statements

## How to use it

SwiftSmith's only dependency is Python 3. It was developed on Python 3.7, so it should work on any subsequent versions but is untested on previous versions.

It exposes a simple command line interface, and may be used "out of the box" by simply running
```
python3 -m swiftsmith
```
from the project's root directory, which will write the generated program to standard output.

The program that is generated is determined by a seed for the random number generator, which is given as a base64-encoded string which may be specified as the first (and only) command line argument. SwiftSmith guarantees that programs generated using the same seed are identical.
```
python3 -m swiftsmith YOUR_SEED_HERE
```

Currently, the easiest way to save the generated program is to redirect the output of swiftsmith to a file or another program:
```
python3 -m swiftsmith YOUR_SEED_HERE >> randomprogram.swift
```

## How it works

SwiftSmith generates programs in three phases. The first phase takes a random walk on the productions of a context free grammar that describes the syntax of Swift. This is part of the program is largely based on the [official summary of the grammar](https://docs.swift.org/swift-book/ReferenceManual/zzSummaryOfTheGrammar.html). Ultimately, this phase produces an abstract syntax tree, where the leaves are strings or one of several token types.

The second phase traverses this parse tree and annotate tokens in the syntax tree with context-depdendent information according to the semantics of Swift. For instance, variables cannot be used before they are declared and initialized, and variables and functions can only be used within their scope.

The third phase produces the actual text of the program from the annotated parse tree.

## Bits and Pieces

Support for working with context-free grammars is provided by the `swiftsmith.grammar` submodule [here](https://github.com/jacobdweightman/swiftsmith/tree/master/swiftsmith/grammar). This exposes the following classes:

* `CFG` which represents a context free grammar
* `Nonterminal` which represents a nonterminal symbol in a grammar
* `Production` which represents a rule for expanding/rewriting a nonterminal in a  grammar
* `ParseTree` which represents a tree of symbols produced by a grammar

As well as counterparts for probabalistic context-free grammars, which are context-free grammars where productions have an associated probability:

* `PProduction` is a probabilitic production, which extends `Production` with a probability value
* `PCFG` which extends `CFG` with a method to create random parse trees.

SwiftSmith uses the grammar submodule extensively, but extends some of its functionality for handling the context-dependent parts of Swift. In particular, "semantic" counterparts of the types from `grammar` are defined in `semantics.py` [here](https://github.com/jacobdweightman/swiftsmith/blob/master/swiftsmith/semantics.py), including:

* `SemanticParseTree` which supports working with nodes that require annotation with context-dependent information
* The `Annotatable` interface for parse tree nodes that depend on context
* The `SemanticNonterminal` and `Token` classes which implement `Annotatable` for internal and leaf parse tree nodes, respectively
* `SemanticPCFG` which is a PCFG but which works with `SemanticParseTree`s instead of "ordinary" `ParseTree`s.

## Hacking with SwiftSmith

I've tried to design SwiftSmith to be relatively modular and extensible, and I encourage you to try extending or borrowing internals from SwiftSmith. Some ideas to get you started:
* Experiment with new metamorphic relations
* Use the `grammar` submodule or `semantics.py` to generate programs in a different programming language
* Generate random test data for a non-compiler program—for instance, JSON is readily described by a CFG
* Build a simple translator based on parse tree transformations