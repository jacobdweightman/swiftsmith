# Note: expected to be invoked from project root directory.

import random

print("""
import ModuleA
import ModuleB
""")

for i in random.sample(range(-1000, 1000), 50):
    #print(f"print(\"\({i})\")")
    print(f"assert(ModuleA.main({i}) == ModuleB.main({i}))")
