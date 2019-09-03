FROM centos:6
MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV DOCKERFILE_DISTRO=centos    \
    DOCKERFILE_DISTRO_VERSION=6 \
    SPACK_ROOT=/opt/spack       \
    FORCE_UNSAFE_CONFIGURE=1

COPY bin   $SPACK_ROOT/bin
COPY etc   $SPACK_ROOT/etc
COPY lib   $SPACK_ROOT/lib
COPY share $SPACK_ROOT/share
COPY var   $SPACK_ROOT/var
RUN mkdir -p $SPACK_ROOT/opt/spack

RUN yum update -y                                             \
 && yum install -y epel-release                               \
 && yum update -y                                             \
 && yum --enablerepo epel groupinstall -y "Development Tools" \
 && yum --enablerepo epel install -y                          \
        curl           findutils gcc-c++    gcc               \
        gcc-gfortran   git       gnupg2     hostname          \
        iproute        Lmod      make       patch             \
        openssh-server python    python-pip tcl               \
        unzip          which                                  \
 && pip install boto3                                         \
 && rm -rf /var/cache/yum                                     \
 && yum clean all

RUN ( echo ". \$SPACK_ROOT/share/spack/docker/shell-helpers.bash"   \
 &&   echo "setup_spack --with-completion"                        ) \
       >> /etc/profile.d/spack.sh                                   \
 && ( echo ". \$SPACK_ROOT/share/spack/docker/shell-helpers.bash"   \
 &&   echo "ssh_init"                                             ) \
       >> /etc/profile.d/handle-ssh.sh                              \
 && ( echo ". \$SPACK_ROOT/share/spack/docker/handle-prompt.sh"   ) \
       >> /etc/profile.d/handle-prompt.sh                           \
 && mkdir -p /root/.spack                                           \
 && cp $SPACK_ROOT/share/spack/docker/modules.yaml                  \
        /root/.spack/modules.yaml                                   \
 && rm -rf /root/*.* /run/nologin $SPACK_ROOT/.git

# [WORKAROUND]
# https://superuser.com/questions/1241548/
#     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
RUN [ -f ~/.profile ]                                             \
 && sed -i 's/mesg n/( tty -s \&\& mesg n || true )/g' ~/.profile \
 || true

WORKDIR /root
SHELL ["/bin/bash", "/opt/spack/share/spack/docker/custom-shell.bash"]

# TODO: add a command to Spack that (re)creates the package cache
RUN spack spec hdf5+mpi

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["docker-shell"]
