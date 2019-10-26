FROM ubuntu:18.04
MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV DOCKERFILE_BASE=ubuntu            \
    DOCKERFILE_DISTRO=ubuntu          \
    DOCKERFILE_DISTRO_VERSION=18.04   \
    SPACK_ROOT=/opt/spack             \
    FORCE_UNSAFE_CONFIGURE=1          \
    DEBIAN_FRONTEND=noninteractive    \
    CURRENTLY_BUILDING_DOCKER_IMAGE=1 \
    container=docker

COPY bin   $SPACK_ROOT/bin
COPY etc   $SPACK_ROOT/etc
COPY lib   $SPACK_ROOT/lib
COPY share $SPACK_ROOT/share
COPY var   $SPACK_ROOT/var
RUN mkdir -p $SPACK_ROOT/opt/spack

RUN apt-get -yqq update                                   \
 && apt-get -yqq install                                  \
        build-essential ca-certificates curl       g++    \
        gcc             gfortran        git        gnupg2 \
        iproute2        lmod            lua-posix  make   \
        openssh-server  python          python-pip tcl    \
        unzip                                             \
 && pip install boto3                                     \
 && rm -rf /var/lib/apt/lists/*

RUN ( echo ". /usr/share/lmod/lmod/init/bash"                       \
 &&   echo ". \$SPACK_ROOT/share/spack/setup-env.sh"                \
 &&   echo "if [ \"\$CURRENTLY_BUILDING_DOCKER_IMAGE\" '!=' '1' ]"  \
 &&   echo "then"                                                   \
 &&   echo "  . \$SPACK_ROOT/share/spack/spack-completion.bash"     \
 &&   echo "fi"                                                   ) \
       >> /etc/profile.d/spack.sh                                   \
 && ( echo "f=\"\$SPACK_ROOT/share/spack/docker/handle-ssh.sh\""    \
 &&   echo "if [ -f \"\$f\" ]"                                      \
 &&   echo "then"                                                   \
 &&   echo "  .  \"\$f\""                                           \
 &&   echo "else"                                                   \
 &&   cat  $SPACK_ROOT/share/spack/docker/handle-ssh.sh             \
 &&   echo "fi"                                                   ) \
       >> /etc/profile.d/handle-ssh.sh                              \
 && ( echo "f=\"\$SPACK_ROOT/share/spack/docker/handle-prompt.sh\"" \
 &&   echo "if [ -f \"\$f\" ]"                                      \
 &&   echo "then"                                                   \
 &&   echo "  .  \"\$f\""                                           \
 &&   echo "else"                                                   \
 &&   cat  $SPACK_ROOT/share/spack/docker/handle-prompt.sh          \
 &&   echo "fi"                                                   ) \
       >> /etc/profile.d/handle-prompt.sh                           \
 && mkdir -p /root/.spack                                           \
 && cp $SPACK_ROOT/share/spack/docker/modules.yaml                  \
        /root/.spack/modules.yaml                                   \
 && rm -rf /root/*.* $SPACK_ROOT/.git

# [WORKAROUND]
# https://superuser.com/questions/1241548/
#     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
RUN [ -f ~/.profile ]                                               \
 && sed -i 's/mesg n/( tty -s \&\& mesg n || true )/g' ~/.profile \
 || true

# [WORKAROUND]
# https://bugs.launchpad.net/ubuntu/+source/lua-posix/+bug/1752082
RUN ln -s posix_c.so /usr/lib/x86_64-linux-gnu/lua/5.2/posix.so

WORKDIR /root
SHELL ["/bin/bash", "-l", "-c"]

# TODO: add a command to Spack that (re)creates the package cache
RUN spack spec hdf5+mpi

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["docker-shell"]
