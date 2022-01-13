FROM opensuse/leap:15.3
MAINTAINER Christian Goll <cgoll@suse.com>

ENV DOCKERFILE_BASE=opensuse          \
    DOCKERFILE_DISTRO=leap   \
    DOCKERFILE_DISTRO_VERSION=15.3    \
    SPACK_ROOT=/opt/spack      \
    DEBIAN_FRONTEND=noninteractive    \
    CURRENTLY_BUILDING_DOCKER_IMAGE=1 \
    container=docker

RUN zypper ref && \
    zypper up -y && \
    zypper in -y \
    bzip2\
    curl\
    file\
    gcc-c++\
    gcc-fortran\
    make\
    gzip\
    patch\
    patchelf\
    python3-base \
    python3-boto3\
    tar\
    xz\
&&  zypper clean

# clean up manpages
RUN	rm -rf /var/cache/zypp/*  \
	rm -rf /usr/share/doc/packages/* \ 
	rm -rf /usr/share/doc/manual/*

# copy spack into container
COPY bin   $SPACK_ROOT/bin
COPY etc   $SPACK_ROOT/etc
COPY lib   $SPACK_ROOT/lib
COPY share $SPACK_ROOT/share
COPY var   $SPACK_ROOT/var
RUN mkdir -p $SPACK_ROOT/opt/spack

RUN ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/docker-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/interactive-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/spack-env

RUN mkdir -p /root/.spack \
 && cp $SPACK_ROOT/share/spack/docker/modules.yaml \
        /root/.spack/modules.yaml \
 && rm -rf /root/*.* /run/nologin $SPACK_ROOT/.git

# [WORKAROUND]
# https://superuser.com/questions/1241548/
#     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
RUN [ -f ~/.profile ]                                               \
 && sed -i 's/mesg n/( tty -s \\&\\& mesg n || true )/g' ~/.profile \
 || true

WORKDIR /root
SHELL ["docker-shell"]

# Disable bootstrapping from sources
RUN ${SPACK_ROOT}/bin/spack bootstrap untrust spack-install

# TODO: add a command to Spack that (re)creates the package cache
RUN ${SPACK_ROOT}/bin/spack spec hdf5+mpi

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["interactive-shell"]
