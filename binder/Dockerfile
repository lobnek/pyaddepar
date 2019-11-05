# Set the base image to beakerx
FROM jupyter/base-notebook:1386e2046833 as jupyter

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# copy the config.ini file
COPY /binder/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

# hardcoded parameters!? see https://github.com/moby/moby/issues/35018
COPY --chown=jovyan:users /binder/files $HOME/work

# copy the package over and install it
COPY --chown=jovyan:users . /tmp/addepar

RUN pip install --no-cache-dir /tmp/addepar && \
    rm -rf /tmp/addepar


