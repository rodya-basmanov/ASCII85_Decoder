#!/bin/bash

set -e

# Run program with -e argument
../bin/main -e

# If all went well, print "All right", otherwise set -e will exit the script
echo "All right" 