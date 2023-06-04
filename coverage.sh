#!/bin/bash
poetry run coverage run --source=pyaddepar/. -m pytest
poetry run coverage report -m
poetry run coverage html
if [[ $OSTYPE == 'darwin'* ]]; then
    open htmlcov/index.html
fi
if [[ $OSTYPE == 'linux'* ]]; then
    xdg-open htmlcov/index.html
fi
