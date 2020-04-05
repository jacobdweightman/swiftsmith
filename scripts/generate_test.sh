# Note: expected to be invoked from project root directory.

DIR=$1
SEED=$2

python3 -m swiftsmith \
    ${SEED} \
    -mr unnecessary-multiplication \
    -o ${DIR}/Module \
    --tests ${DIR}/test.swift

mkdir -p ${DIR}
cd ${DIR}

swiftc -emit-module -emit-library ModuleA.swift -suppress-warnings
swiftc -emit-module -emit-library ModuleB.swift -suppress-warnings

swiftc test.swift -I . -L . -lModuleA -lModuleB -o test

install_name_tool -change libModuleA.dylib $(pwd)/libModuleA.dylib test
install_name_tool -change libModuleB.dylib $(pwd)/libModuleB.dylib test
