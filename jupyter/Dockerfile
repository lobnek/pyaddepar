# Set the base image to beakerx
FROM lobnek/jupyter:v2.5

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# copy the actual package
COPY ./work /home/$NB_USER/work

USER root
# INSTALL pyaddepar in docker image
COPY pyaddepar /tmp/pyaddepar/pyaddepar
COPY setup.py  /tmp/pyaddepar

RUN pip install --no-cache-dir -e /tmp/pyaddepar
USER $NB_USER

