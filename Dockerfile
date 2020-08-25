FROM python:3.7.7-slim-stretch as builder

# install the pyaddepar package
COPY . /tmp/addepar

# install the package
#RUN buildDeps='gcc g++' && \
#    apt-get update && apt-get install -y $buildDeps --no-install-recommends && \
# RUN pip install --no-cache-dir flask==1.1.2 && \
RUN pip install --no-cache-dir /tmp/addepar && \
    rm -r /tmp/addepar

    #&& \
    #apt-get purge -y --auto-remove $buildDeps


########################################################################################################################
FROM builder as test

COPY ./test  /addepar/test

# this is used to mock http for testing
RUN pip install --no-cache-dir -r /addepar/test/requriements.txt  httpretty pytest pytest-cov pytest-html sphinx requests-mock
CMD py.test --cov=pyaddepar  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html /addepar/test
