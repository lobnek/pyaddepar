# Set the base image to beakerx
FROM jupyter/scipy-notebook:1386e2046833 as jupyter

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

USER root

# copy the config.ini file
COPY /binder/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

COPY /binder/config.ini  /home/jovyan/work/config.ini
COPY /binder/example.ipynb /home/jovyan/work/example.ipynb

COPY . /tmp/addepar

RUN pip install --no-cache-dir /tmp/addepar && \
    rm -rf /tmp/addepar
