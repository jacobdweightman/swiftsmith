import argparse
import random
import swiftsmith
import sys

from datetime import date
from swiftsmith.metamorphic import unnecessary_addition, unnecessary_multiplication

########################################
#   Argument Parsing                   #
########################################

def mr(name):
    if name is None:
        return None
    """Converts the name of a metamorphic relation to th MR itself."""
    if name == "unnecessary-addition":
        return unnecessary_addition
    elif name == "unnecessary-multiplication":
        return unnecessary_multiplication
    else:
        raise NotImplementedError(f"No MR named '{name}'")

parser = argparse.ArgumentParser(prog="SwiftSmith")
parser.add_argument("seed", type=str, default="AA==")
parser.add_argument("--output", "-o", type=str)
parser.add_argument("-mr", type=mr)
parser.add_argument('--version', action='version', version='%(prog)s 0.0.2')

args = parser.parse_args()

########################################
#   Program Generation                 #
########################################

random.seed(args.seed)

parsetree = swiftsmith.swift.randomtree()

# We play a game of musical chairs to ensure that the generated main function uses a
# function defined in the generated code instead of one imported from the standard
# library. Public symbols are visible from anywhere in the scope tree, so when the
# program is generated then the file scope and standard library scope must be in the
# same tree. When main is generated, they must be in different trees.

rootscope = swiftsmith.Scope()
rootscope.import_standard_library()
parsetree.annotate(scope=rootscope)


from swiftsmith.expression import FunctionCall
from swiftsmith.semantics import SemanticParseTree
from swiftsmith.standard_library import Int
from swiftsmith.names import identifier

# break the link between rootscope and the standard library scopes
rootscope.children = [rootscope.children[-1]]

argname = next(identifier)
rootscope.declare(argname, Int, False)
fname, ftype = rootscope.choose_function()
mainbody = SemanticParseTree(FunctionCall(fname, ftype))
mainbody.annotate(scope=rootscope)

mainfunc = f"""
public func main(_ {argname}: Int) -> {ftype.returntype.name} {{
    return {mainbody.string()}
}}"""

if args.mr:
    mtparsetree = args.mr(parsetree)

########################################
#   File I/O                           #
########################################

def openmodule(suffix):
    if args.output is None:
        return open("/dev/stdout", 'w')
    else:
        return open(args.output + f"{suffix}.swift", 'w')

def writemodule(suffix, code, main):
    with openmodule(suffix) as f:
        f.write(f"\n// Generated by Swiftsmith on {date.today().strftime('%B %d, %Y')}")
        f.write(code)
        f.write(main)

if args.mr:
    writemodule("A", parsetree.string(), mainfunc)
    writemodule("B", mtparsetree.string(), mainfunc)
else:
    writemodule("", parsetree.string(), mainfunc)
