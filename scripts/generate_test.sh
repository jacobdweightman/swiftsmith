# Note: expected to be invoked from project root directory.

SEED=$1

python3 -m swiftsmith \
    ${SEED} \
    -mr unnecessary-multiplication \
    -o generated/Module \
    --tests generated/test.swift

sh scripts/generate_module.sh ModuleA -Onone
sh scripts/generate_module.sh ModuleB -Osize

swiftc generated/test.swift -I generated -L generated -lModuleA -lModuleB -o generated/test

install_name_tool -change libModuleA.dylib $(pwd)/generated/libModuleA.dylib generated/test
install_name_tool -change libModuleB.dylib $(pwd)/generated/libModuleB.dylib generated/test
