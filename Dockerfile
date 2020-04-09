# Set the base image to beakerx
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# install the pyaddepar package
COPY . /tmp/addepar

# install the package
RUN conda install -y -c conda-forge pandas=0.25.3 flask=1.1.1 && \
    conda clean -y --all && \
    pip install --no-cache-dir /tmp/addepar && \
    rm -r /tmp/addepar


########################################################################################################################
FROM builder as test

COPY ./test  /addepar/test

# this is used to mock http for testing
RUN pip install httpretty pytest pytest-cov pytest-html sphinx requests-mock
CMD py.test --cov=pyaddepar  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html /addepar/test
