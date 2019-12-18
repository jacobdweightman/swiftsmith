# SwiftSmith

SwiftSmith is a tool for generating random, valid programs in the Swift programming language. It is part of an ongoing research project in testing the Swift compiler.

## How to use it

SwiftSmith's only dependency is Python 3. It was developed on Python 3.7, so it should work on any subsequent versions but is untested on previous versions.

It exposes a simple command line interface, and may be used "out of the box" by simply running
```
python3 -m swiftsmith
```
from the project's root directory, which will write the generated program to standard output.

The program that is generated is determined by a seed for the random number generator, which may be specified as the first (and only) command line argument:
```
python3 -m swiftsmith YOUR_SEED_HERE
```

Currently, the easiest way to save the generated program is to redirect the output of swiftsmith to a file or another program:
```
python3 -m swiftsmith YOUR_SEED_HERE >> randomprogram.swift
```

## How it works

SwiftSmith generates programs in two phases. The first phase takes a random walk on the productions of a context free grammar that describes the syntax of Swift. This is part of the program is largely based on the [official summary of the grammar](https://docs.swift.org/swift-book/ReferenceManual/zzSummaryOfTheGrammar.html). Ultimately, this phase produces a parse tree, where the leaves are one of several token types but without a specific string value.

The second phase traverses this parse tree and assigns specific string values to each token according to the semantics of Swift. For instance, variables cannot be used before they are declared and initialized, and variables and functions can only be used within their scope.
