#!/bin/sh

#toolsdir=~/work/fonts/dinish/tools
toolsdir=.

# docker build . -t specimen-builder

rm -f src/fonts/*.woff2

find ../dinish/fonts -name '*.woff2' -exec cp -p {} src/fonts/ \;

for font in DINish-Bold DINishCondensed-Bold DINishCondensed-Italic DINishCondensed-Regular DINishExpanded-Bold DINishExpanded-Italic DINishExpanded-Regular DINish-Italic DINish-Regular
do
	$toolsdir/woff2css src/fonts/$font.woff2 src/css/$font.css
done

docker run --rm -v `pwd`/src:/app/src -v `pwd`/out:/out specimen-builder

(
	cd out/_site
	python3 ../../standalone_html.py index.html /tmp/compact.html
)
