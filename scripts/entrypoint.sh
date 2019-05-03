#!/bin/bash

echo entrypoint

source ./scripts/load-secrets.sh
"$@"