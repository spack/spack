ARG BASE

FROM $BASE
MAINTAINER Spack Maintainers <maintainers@spack.io>

ARG BASE
ARG DISTRO
ARG DISTRO_VERSION

ENV DOCKERFILE_BASE=$BASE                     \
    DOCKERFILE_DISTRO=$DISTRO                 \
    DOCKERFILE_DISTRO_VERSION=$DISTRO_VERSION \
    SPACK_ROOT=/spack                         \
    FORCE_UNSAFE_CONFIGURE=1                  \
    DEBIAN_FRONTEND=noninteractive            \
    container=docker

COPY bin   $SPACK_ROOT/bin
COPY etc   $SPACK_ROOT/etc
COPY lib   $SPACK_ROOT/lib
COPY share $SPACK_ROOT/share
COPY var   $SPACK_ROOT/var
RUN mkdir -p $SPACK_ROOT/opt/spack

MASK PUSH
MASK [[ $DISTRO == arch ]]
RUN pacman -Sy --noconfirm                                     \
        base-devel   ca-certificates curl   gcc                \
        gcc-fortran  git             gnupg2 iproute2           \
        make         openssh         python python-pip         \
        sudo         tcl                                       \
 && echo 'nobody ALL=(ALL) NOPASSWD: ALL' >                    \
        /etc/sudoers.d/nobody-sudo                             \
 && sudo -u nobody git clone --depth 1                         \
        https://aur.archlinux.org/lua-posix.git /tmp/lua-posix \
 && sudo -u nobody git clone --depth 1                         \
        https://aur.archlinux.org/lmod.git /tmp/lmod           \
 && (  cd /tmp/lua-posix                                       \
    && sudo -u nobody makepkg -si --asdeps --noconfirm )       \
 && (  cd /tmp/lmod                                            \
    && sudo -u nobody makepkg -si --noconfirm )                \
 && rm -rf /tmp/lua-posix /tmp/lmod /etc/sudoers.d/nobody-sudo

MASK [[ $DISTRO =~ (centos|rhel.*) ]]
RUN yum update -y

  MASK PUSH
  MASK [[ $DISTRO =~ rhel.* ]]
  RUN yum install -y yum-conf-repos.noarch \
   && yum update -y
  MASK POP

RUN yum install -y epel-release                               \
 && yum update -y                                             \
 && yum --enablerepo epel groupinstall -y "Development Tools" \
 && yum --enablerepo epel install -y                          \
         curl           findutils gcc-c++    gcc              \
         gcc-gfortran   git       gnupg2     hostname         \
         iproute        Lmod      make       patch            \
         openssh-server python    python-pip tcl              \
 && rm -rf /var/cache/yum                                     \
 && yum clean all

MASK [[ $DISTRO == fedora ]]
RUN dnf update -y                                            \
 && dnf group install -y "C Development Tools and Libraries" \
 && dnf install -y                                           \
        @development-tools                                   \
        curl            findutils    gcc-c++     gcc         \
        gcc-gfortran    git          gnupg2      hostname    \
        iproute         Lmod         make        patch       \
        openssh-server  python       tcl                     \
 && dnf clean all

MASK [[ $DISTRO == opensuse ]]
RUN zypper -n ref                                              \
 && zypper -n up --skip-interactive --no-recommends            \
 && zypper -n install -l --no-recommends --type pattern        \
        devel_basis  devel_C_C++                               \
 && zypper -n install -l --no-recommends                       \
        bash        bash-completion ca-certificates curl       \
        findutils   gcc             gcc-locale      gcc-c++    \
        gcc-fortran git             glibc-locale    gpg2       \
        hostname    iproute         lua-lmod        make       \
        patch       openssh         python          python-pip \
        python-xml  tcl                                        \
 && zypper clean                                               \
 && rm -rf /var/cache/zypp/*

MASK [[ $DISTRO == ubuntu ]]
RUN apt-get -yqq update                                   \
 && apt-get -yqq install                                  \
        build-essential ca-certificates curl       g++    \
        gcc             gfortran        git        gnupg2 \
        iproute2        lmod            lua-posix  make   \
        openssh-server  python          python-pip tcl

  MASK PUSH
  MASK [[ $DISTRO_VERSION == bionic ]]
  # [WORKAROUND]
  # https://bugs.launchpad.net/ubuntu/+source/lua-posix/+bug/1752082
  RUN ln -s posix_c.so /usr/lib/x86_64-linux-gnu/lua/5.2/posix.so
  MASK POP

RUN rm -rf /var/lib/apt/lists/*

MASK POP

RUN rm -rf $SPACK_ROOT/.git                                          \
 && pip install boto3                                                \
 && (  echo ". /usr/share/lmod/lmod/init/bash"                       \
    && echo ". $SPACK_ROOT/share/spack/setup-env.sh"                 \
    && echo ". $SPACK_ROOT/share/spack/spack-completion.bash" )      \
        >> /etc/profile.d/spack.sh                                   \
 && ln -s $SPACK_ROOT/share/spack/docker/handle-ssh.sh               \
        /etc/profile.d/handle-ssh.sh                                 \
 && ln -s $SPACK_ROOT/share/spack/docker/handle-prompt.sh            \
        /etc/profile.d/handle-prompt.sh                              \
 && mkdir -p /root/.spack                                            \
 && cp $SPACK_ROOT/share/spack/docker/modules.yaml                   \
        /root/.spack/modules.yaml                                    \
 && rm -rf /root/*.*

MASK PUSH
MASK [[ $DISTRO_VERSION =~ (centos|fedora|opensuse|rhel.*) ]]
RUN rm -f /run/nologin
MASK POP

WORKDIR /root
ENTRYPOINT ["bash", "/spack/share/spack/docker/entrypoint.bash"]
CMD ["docker-shell"]

