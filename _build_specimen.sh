#!/bin/sh

#toolsdir=~/work/fonts/dinish/tools
toolsdir=.

docker build --progress=plain . -t specimen-builder

rm -f src/fonts/*.woff2

cp ../dinish/fonts/woff2/variable/*.woff2 src/fonts/

docker run --rm -v `pwd`/src:/app/src -v `pwd`/out:/out specimen-builder

(
	cd out/_site
	python3 ../../standalone_html.py index.html /tmp/compact.html
)