#!/usr/bin/env bash

package='pyaddepar'

docker run \
       --mount type=bind,source=$(pwd)/${package},target=/pyan/${package},readonly \
       tschm/pyan:latest \
       python pyan.py ${package}/*.py -V --uses --defines --colored --dot --nested-groups \
       > graph/graph.dot   # this is the output of the docker run command. It's writtern directly to the host

docker run \
       --mount type=bind,source=$(pwd)/graph,target=/pyan/graph \
       tschm/pyan:latest \
       dot -Tsvg /pyan/graph/graph.dot \
       > graph/graph.svg

