from .types import AccessLevel, DataType, EnumType, FunctionType, Struct, CallSyntax

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

_Wrapped = DataType("Wrapped", access=AccessLevel.private)
Optional = EnumType(
    "Optional",
    access=AccessLevel.public,
    generic_types={_Wrapped: None}
)
Optional.add_case("some", [_Wrapped])
Optional.add_case("none", [])

Bool.static_methods[">"] = FunctionType({"left": Int, "right": Int}, Bool, syntax=CallSyntax.infix)
Bool.static_methods["=="] = FunctionType({"left": Int, "right": Int}, Bool, syntax=CallSyntax.infix)

Int.static_methods["&+"] = FunctionType({"left": Int, "right": Int}, Int, syntax=CallSyntax.infix)
Int.static_methods["&*"] = FunctionType({"left": Int, "right": Int}, Int, syntax=CallSyntax.infix)
