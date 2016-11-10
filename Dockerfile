# Set the base image to Ubuntu
FROM continuumio/miniconda3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

RUN conda install -q -y pandas=0.19.1 requests=2.11.1 networkx=1.11 #sqlalchemy psycopg2

ADD ./pyaddepar /pyaddepar/pyaddepar
ADD ./scripts   /pyaddepar

WORKDIR /pyaddepar

