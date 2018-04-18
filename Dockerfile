# Set the base image to Ubuntu
FROM continuumio/miniconda3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

RUN conda install -q -y nomkl pandas=0.21 requests && conda clean -y -all

COPY ./pyaddepar /pyaddepar/pyaddepar

WORKDIR /pyaddepar

