FROM python:3.7.7-slim-stretch as builder

# install the pyaddepar package
COPY . /tmp/addepar

RUN pip install --no-cache-dir /tmp/addepar && \
    rm -r /tmp/addepar

########################################################################################################################
FROM builder as test

COPY ./test  /addepar/test
# this is used to mock http for testing
RUN pip install --no-cache-dir -r /addepar/test/requirements.txt
