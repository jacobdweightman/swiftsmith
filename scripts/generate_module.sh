# Note: expected to be invoked from project root directory.

SEED=$1
NAME=$2
ARGS=$3

function finish {
    python3 -m swiftsmith ${SEED} > generated/${NAME}.swift
    swiftc -emit-module -emit-library generated/${NAME}.swift ${ARGS} -suppress-warnings

    # swiftc output goes to the running directory by default. specifying with -o changes
    # the names of the output files, so we move them as a workaround.
    mv lib${NAME}.dylib generated
    mv ${NAME}.swiftdoc generated
    mv ${NAME}.swiftmodule generated
}
trap finish EXIT
