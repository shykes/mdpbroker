#!/bin/bash

set -x

rm -fr ~/* ~/.env

# Create virtualenv
virtualenv --no-site-packages ~/.env

./extend
