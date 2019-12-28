# Note: expected to be invoked from project root directory.

print("""
import ModuleA
import ModuleB

assert(ModuleA.main(5) == ModuleB.main(5))
""")