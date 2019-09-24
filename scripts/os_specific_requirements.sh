#!/bin/bash

echo Running OS setup....
echo OS: $OSTYPE
if [ "$OSTYPE" == "darwin" ]; then
  echo "Running Mac setup"
  brew install libgit2
fi