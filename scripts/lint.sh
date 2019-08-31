#!/bin/bash

function fail_lint(){
    FAIL_CODE=$?
    echo Lint failed. See above output...
    exit $FAIL_CODE
}

echo [Step 1] Linting src/main
pylint src/main/ || fail_lint

DOCSTRING_REQUIREMENT=C0111
echo [Step 2] Linting src/test
pylint --disable=$DOCSTRING_REQUIREMENT src/test || fail_lint

