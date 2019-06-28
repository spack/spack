FROM ubuntu:18.04
MAINTAINER Pramod Kumbhar <pramod.s.kumbhar@gmail.com>
MAINTAINER Matthias Wolf <matthias.wolf@epfl.ch>

ENV DEBIAN_FRONTEND noninteractive

# default software required
RUN apt-get update
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update
COPY sysconfig/ubuntu-18.04/packages /tmp/
RUN sed -e 's/#.*//g' /tmp/packages| \
        xargs -r apt-get --allow-downgrades \
                         --allow-remove-essential \
                         --allow-change-held-packages \
                         install -y

RUN git clone https://github.com/BlueBrain/spack.git /opt/spack
ENV SPACK_ROOT /opt/spack
ENV PATH $SPACK_ROOT/bin:$PATH

# see this: http://stackoverflow.com/questions/20635472/using-the-run-instruction-in-a-dockerfile-with-source-does-not-work
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN echo ". $SPACK_ROOT/share/spack/setup-env.sh" \
    > /etc/profile.d/spack.sh

RUN spack compiler find && spack compilers

RUN mkdir -p $SPACK_ROOT/etc/spack
COPY sysconfig/ubuntu-18.04/*.yaml $SPACK_ROOT/etc/spack/

WORKDIR "/opt/spack"

ARG pr
ARG revision=develop

RUN if [[ "x$pr" != "x" ]]; then \
            git fetch origin +refs/pull/$pr/head:refs/remotes/origin/pull/$pr \
            && git checkout pull/$pr; \
    else \
            git fetch \
            && git checkout $revision; \
    fi
