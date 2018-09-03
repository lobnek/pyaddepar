#!/usr/bin/env bash

package='pyaddepar'

mkdir -p artifacts/graph

docker run --rm \
       --mount type=bind,source=$(pwd)/${package},target=/pyan/${package},readonly \
       tschm/pyan:latest \
       python pyan.py ${package}/*.py -V --uses --defines --colored --dot --nested-groups \
       > graph.dot   # this is the output of the docker run command. It's writtern directly to the host

# remove all the private nodes...
grep -vE "____" graph.dot > graph2.dot

docker run --rm \
       -v $(pwd)/graph2.dot:/pyan/graph.dot:ro \
       tschm/pyan:latest \
       dot -Tsvg /pyan/graph.dot \
       > artifacts/graph/graph.svg

rm graph.dot graph2.dot
