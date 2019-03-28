# Set the base image to beakerx
FROM lobnek/jupyter:v2.8

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# copy the notebooks into the image
COPY --chown=beakerx:beakerx ./work $WORK

COPY --chown=beakerx:beakerx . /tmp/pyaddepar

RUN pip install --no-cache-dir /tmp/pyaddepar && \
    rm -r /tmp/pyaddepar
