# Note: expected to be invoked from project root directory.

DIR=$1
SEED=$2

mkdir -p ${DIR}

python3 -m swiftsmith \
    ${SEED} \
    -mr failable-init \
    -o ${DIR}/Module \
    --tests ${DIR}/test.swift

cd ${DIR}

swiftc -emit-module -emit-library ModuleA.swift -suppress-warnings || exit 1
swiftc -emit-module -emit-library ModuleB.swift -suppress-warnings || exit 1

swiftc test.swift -I . -L . -lModuleA -lModuleB -o test

# Import shared libraries from the working directory. This is necessary prior to Swift
# 5.2, which is not yet available for ARM (and I don't want to build it myself).
LD_LIBRARY_PATH=. ./test
