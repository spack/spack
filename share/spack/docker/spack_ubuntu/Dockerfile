FROM ubuntu
MAINTAINER Omar Padron <omar.padron@kitware.com>

ENV DEBIAN_FRONTEND=noninteractive \
    SPACK_ROOT=/spack              \
    FORCE_UNSAFE_CONFIGURE=1       \
    DISTRO=ubuntu

RUN apt-get -yqq update && apt-get -yqq install \
        build-essential     \
        ca-certificates     \
        curl                \
        g++                 \
        gcc                 \
        gfortran            \
        git                 \
        gnupg2              \
        lmod                \
        make                \
        openssh-server      \
        python              \
        tcl              && \
    git clone --depth 1 git://github.com/llnl/spack.git /spack && \
    rm -rf /spack/.git && rm -rf /var/lib/apt/lists/*

RUN echo "source /usr/share/lmod/lmod/init/bash" \
    > /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/setup-env.sh" \
    >> /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/spack-completion.bash" \
    >> /etc/profile.d/spack.sh
COPY handle-ssh.sh /etc/profile.d/handle-ssh.sh
COPY handle-prompt.sh /etc/profile.d/handle-prompt.sh.tmp

RUN (                                             \
        echo "export DISTRO=$DISTRO"            ; \
        cat /etc/profile.d/handle-prompt.sh.tmp ; \
        rm  /etc/profile.d/handle-prompt.sh.tmp   \
    ) > /etc/profile.d/handle-prompt.sh

RUN mkdir -p /root/.spack
COPY modules.yaml /root/.spack/modules.yaml

RUN rm -rf /root/*.*

WORKDIR /root
ENTRYPOINT ["bash"]
CMD ["-l"]
