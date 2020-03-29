# Note: expected to be invoked from project root directory.

SEED=$1
NAME=$2
ARGS=$3

function finish {
    # This program must finish cleaning up. Disable keyboard interrupts.
    trap "echo 'Shutting down...'; err=$?" SIGINT

    # swiftc output goes to the running directory by default. specifying with -o changes
    # the names of the output files, so we move them as a workaround.
    mv lib${NAME}.dylib generated 2> /dev/null
    mv ${NAME}.swiftdoc generated 2> /dev/null
    mv ${NAME}.swiftmodule generated 2> /dev/null
    rm ${NAME}.swiftsourceinfo

    exit $err
}

python3 -m swiftsmith ${SEED} > generated/${NAME}.swift
trap finish EXIT
swiftc -emit-module -emit-library generated/${NAME}.swift ${ARGS} -suppress-warnings
