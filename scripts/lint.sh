#!/bin/bash

function fail_lint(){
    FAIL_CODE=$?
    echo Lint failed. See above output...
    exit $FAIL_CODE
}

DOCSTRING_REQUIREMENT=C0111

# This can create a problem when we don't use self.assert() in a unit test (Mocking, ext..)
METHOD_COULD_BE_FUNCTION=R0201

TOO_FEW_PUBLIC_METHODS=R0903

echo [Step 1] Linting src/main
pylint --disable=$TOO_FEW_PUBLIC_METHODS src/main/ || fail_lint

echo [Step 2] Linting src/test
pylint --disable=$DOCSTRING_REQUIREMENT,$METHOD_COULD_BE_FUNCTION src/test || fail_lint

