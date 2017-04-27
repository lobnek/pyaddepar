# Set the base image to Ubuntu
FROM continuumio/miniconda3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

RUN conda install -q -y pandas=0.19.1 requests networkx

ADD ./pyaddepar /pyaddepar/pyaddepar
ADD ./scripts   /pyaddepar/scripts

WORKDIR /pyaddepar

