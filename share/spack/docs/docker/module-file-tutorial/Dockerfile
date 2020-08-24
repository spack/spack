FROM ubuntu:16.04

# General environment for docker
ENV DEBIAN_FRONTEND=noninteractive \
    SPACK_ROOT=/usr/local

# Install system packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       autoconf \
       build-essential \
       ca-certificates \
       coreutils \
       curl man less \
       emacs-nox vim nano \
       git \
       openmpi-bin openmpi-common libopenmpi-dev \
       python \
       unzip \
    &&  rm -rf /var/lib/apt/lists/*

# Load spack environment on login
COPY spack.sh /etc/profile

# Install spack
RUN curl -s -L https://api.github.com/repos/spack/spack/tarball/develop \
    | tar xzC $SPACK_ROOT --strip 1

# Copy configuration for external packages
COPY packages.yaml $SPACK_ROOT/etc/spack/

# Build lmod
RUN spack install lmod && spack clean -a

# Build a compiler
RUN spack install gcc@7.2.0 && spack clean -a
RUN /bin/bash -l -c ' \
    spack compiler add $(spack location -i gcc@7.2.0)/bin'

# Build the software on top of the compiler
RUN spack install netlib-scalapack ^openmpi ^openblas %gcc@7.2.0 \
    && spack install netlib-scalapack ^mpich ^openblas %gcc@7.2.0 \
    && spack install netlib-scalapack ^openmpi ^netlib-lapack %gcc@7.2.0 \
    && spack install netlib-scalapack ^mpich ^netlib-lapack %gcc@7.2.0 \
    && spack install py-scipy ^openblas \
    && spack clean -a

# image run hook: the -l will make sure /etc/profile environments are loaded
CMD /bin/bash -l
