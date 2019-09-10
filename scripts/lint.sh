#!/bin/bash

function fail_lint(){
    FAIL_CODE=$?
    echo Lint failed. See above output...
    exit $FAIL_CODE
}

echo [Step 1] Linting src/main
pylint src/main/ || fail_lint

DOCSTRING_REQUIREMENT=C0111

# This can create a problem when we don't use self.assert() in a unit test (Mocking, ext..)
METHOD_COULD_BE_FUNCTION=R0201

echo [Step 2] Linting src/test
pylint --disable=$DOCSTRING_REQUIREMENT,$METHOD_COULD_BE_FUNCTION src/test || fail_lint

