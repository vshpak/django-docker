#!/bin/bash

# build .whl package and mv to 'docker' directory
python3 -m poetry build -f wheel
mv -f dist/*.whl docker/
rmdir dist/

