# Set the base image to Ubuntu
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

RUN conda install -q -y nomkl pandas=0.24.1 requests=2.21.0 && \
    conda clean -y -all


########################################################################################################################
FROM builder as test

COPY ./pyaddepar /pyaddepar/pyaddepar
COPY ./test   /pyaddepar/test

WORKDIR /pyaddepar

# this is used to mock http for testing
RUN pip install httpretty pytest pytest-cov pytest-html sphinx requests-mock
CMD py.test --cov=pyaddepar  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html test