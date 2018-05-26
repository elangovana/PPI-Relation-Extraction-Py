# Build an image that can do training and inference in SageMaker
# This is a Python 2 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

FROM ubuntu:16.04

MAINTAINER lanax

#Install base packages Python, Wgr & nginx
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python \
         bzip2 \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

#Install conda
RUN wget -nv https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
RUN bash Anaconda3-5.0.1-Linux-x86_64.sh -b -p  /opt/conda/
RUN rm Anaconda3-5.0.1-Linux-x86_64.sh
RUN ls -l /opt/conda/

#Copy source files
COPY ./* /opt/program/

# Here we get all python packages.
# There's substantial overlap between scipy and numpy that we eliminate by
# linking them together. Likewise, pip leaves the install caches populated which uses
# a significant amount of space. These optimizations save a fair amount of space in the
# image, which reduces start up time.
RUN conda install -q -r requirements.txt && \
        rm -rf /root/.cache

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

ENV PATH="/opt/program:/opt/conda/bin:${PATH}"

# Set up the program in the image
WORKDIR /opt/program

