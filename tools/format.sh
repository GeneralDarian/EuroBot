#!/bin/sh

cd `dirname "$0"` && cd ..

find src/ -name '*.py' -printf 'ISORT\t%f\n' -exec isort -q -j8 {} +
find src/ -name '*.py' -printf 'BLACK\t%f\n' -exec black -q     {} +
