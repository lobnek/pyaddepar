# Set the base image to beakerx
FROM lobnek/jupyter:v2.5

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# copy the notebooks into the image
COPY ./work $WORK

# needs to be root as we delete the /tmp/pyaddepar folder
USER root

COPY . /tmp/pyaddepar

RUN pip install --no-cache-dir /tmp/pyaddepar && \
    rm -r /tmp/pyaddepar

USER $NB_USER
