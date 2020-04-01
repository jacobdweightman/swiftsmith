# Note: expected to be invoked from project root directory.

NAME=$1
ARGS=$2

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

trap finish EXIT
swiftc -emit-module -emit-library generated/${NAME}.swift ${ARGS} -suppress-warnings
