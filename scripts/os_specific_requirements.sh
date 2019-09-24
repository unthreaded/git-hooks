#!/bin/bash

if [ "$OSTYPE" == "darwin" ]; then
  echo "Running Mac setup"
  brew install libgit2
fi