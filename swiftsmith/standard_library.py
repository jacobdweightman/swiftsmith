from .types import AccessLevel, FunctionType, Struct, CallSyntax

import random

Bool = Struct(
    "Bool",
    access=AccessLevel.public,
    newvaluefactory=lambda: random.choice(["true", "false"])
)
Int = Struct(
    "Int",
    access=AccessLevel.public,
    newvaluefactory=lambda: str(random.randint(0, 5))
)

Bool.static_methods[">"] = FunctionType({"left": Int, "right": Int}, Bool, syntax=CallSyntax.infix)
Bool.static_methods["=="] = FunctionType({"left": Int, "right": Int}, Bool, syntax=CallSyntax.infix)

Int.static_methods["&+"] = FunctionType({"left": Int, "right": Int}, Int, syntax=CallSyntax.infix)
Int.static_methods["&*"] = FunctionType({"left": Int, "right": Int}, Int, syntax=CallSyntax.infix)
