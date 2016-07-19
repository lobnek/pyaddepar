FROM lobnek/pyutil

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

ADD . /pyaddepar

WORKDIR /pyaddepar

RUN conda install -q -y --file production.txt
