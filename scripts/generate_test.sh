# Note: expected to be invoked from project root directory.

SEED=$1

python3 -m swiftsmith ${SEED} -mr unnecessary-addition -o generated/module

sh scripts/generate_module.sh ModuleA -Onone
sh scripts/generate_module.sh ModuleB -Osize

python3 scripts/generate_harness.py > generated/harness.swift
swiftc generated/harness.swift -I generated -L generated -lModuleA -lModuleB -o generated/test

install_name_tool -change libModuleA.dylib $(pwd)/generated/libModuleA.dylib generated/test
install_name_tool -change libModuleB.dylib $(pwd)/generated/libModuleB.dylib generated/test
