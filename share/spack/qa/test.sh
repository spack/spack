teardown() {
    echo FAIL
    exit 1
}

trap teardown EXIT
