# Set the base image to Ubuntu
FROM continuumio/miniconda3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

RUN conda install -q -y pandas=0.18.1 requests=2.9.1 networkx=1.11 nose sqlalchemy psycopg2

ADD . /pyaddepar

WORKDIR /pyaddepar

