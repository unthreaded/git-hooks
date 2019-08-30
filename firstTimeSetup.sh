#!/bin/bash

# Create hooks directory if user does not already have it.
mkdir -p ../.git/hooks

# Clean out hooks directory for existing dirs. No output if there are no .sample files.
rm ../.git/hooks/*.sample &>/dev/null

# Give proper permissions to hooks before copying.
chmod 755 commit-msg

# Copy proper files into the hooks directory.
cp commit-msg* .git/hooks/
