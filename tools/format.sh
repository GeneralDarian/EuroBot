#!/bin/sh

cd `dirname "$0"` && cd ..

find . -name '*.py' -printf 'ISORT\t%f\n' -exec isort -q -j8 {} +
find . -name '*.py' -printf 'BLACK\t%f\n' -exec black -q     {} +
