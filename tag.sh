#!/usr/bin/env bash
git tag -a $(./setup.py --version) -m "new tag"
git push --tags