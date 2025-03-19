#!/bin/bash

set -e

# Run program with -d argument
../bin/main -d

# If all went well, print "All right", otherwise set -e will exit the script
echo "All right" 