FROM centos:6
MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV DOCKERFILE_BASE=centos            \
    DOCKERFILE_DISTRO=centos          \
    DOCKERFILE_DISTRO_VERSION=6       \
    SPACK_ROOT=/opt/spack             \
    DEBIAN_FRONTEND=noninteractive    \
    CURRENTLY_BUILDING_DOCKER_IMAGE=1 \
    container=docker

# Make yum usable again with CentOS 6
RUN curl https://www.getpagespeed.com/files/centos6-eol.repo --output /etc/yum.repos.d/CentOS-Base.repo

RUN yum update -y \
 && yum install -y epel-release \
 && yum update -y \
 && yum --enablerepo epel groupinstall -y "Development Tools" \
 && yum --enablerepo epel install -y \
        curl \
        findutils \
        gcc-c++ \
        gcc \
        gcc-gfortran \
        git \
        gnupg2 \
        hostname \
        iproute \
        Lmod \
        make \
        patch \
        patchelf \
        python \
        python-pip \
        python-setuptools \
        tcl \
        unzip \
        which \
 && rm -rf /var/cache/yum \
 && yum clean all

# The OS + Python is old enough to have issues fetching the buildcache from
# cloudfront via https. Download it locally to work around that.
RUN mkdir /root/mirrors && cd /root/mirrors && \
    curl -L https://github.com/alalazo/spack-bootstrap-mirrors/releases/download/v0.1-rc.2/bootstrap-buildcache.tar.gz > buildcache.tar.gz && \
    tar xzvf buildcache.tar.gz && rm buildcache.tar.gz

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

RUN sed -i 's\https://mirror.spack.io/bootstrap/github-actions/v0.1\file:///root/mirrors/bootstrap-buildcache\g' $SPACK_ROOT/etc/spack/defaults/bootstrap.yaml

RUN spack spec hdf5+mpi

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["interactive-shell"]
