# Set the base image to Ubuntu
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

RUN conda install -q -y nomkl pandas=0.21 requests && conda clean -y -all && \
    pip install --no-cache-dir requests-mock
COPY ./pyaddepar /pyaddepar/pyaddepar

WORKDIR /pyaddepar

FROM builder as test

# this is used to mock http for testing
RUN pip install httpretty pytest pytest-cov pytest-html sphinx requests-mock
COPY ./test   /pyaddepar/test
CMD py.test --cov=pyaddepar  --cov-report html:/html-coverage --cov-report term --html=/html-report/report.html test
