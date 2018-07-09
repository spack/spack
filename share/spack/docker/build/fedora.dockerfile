FROM fedora:24
MAINTAINER Omar Padron <omar.padron@kitware.com>

ENV SPACK_ROOT=/spack        \
    FORCE_UNSAFE_CONFIGURE=1 \
    DISTRO=fedora

RUN dnf update -y && \
    dnf group install -y "C Development Tools and Libraries" && \
    dnf install -y            \
        @development-tools    \
        curl                  \
        findutils             \
        gcc-c++               \
        gcc                   \
        gcc-gfortran          \
        git                   \
        gnupg2                \
        hostname              \
        iproute               \
        Lmod                  \
        make                  \
        patch                 \
        openssh-server        \
        python                \
        tcl                && \
    git clone --depth 1 git://github.com/spack/spack.git /spack && \
    rm -rf /spack/.git && dnf clean all

RUN echo "source /usr/share/lmod/lmod/init/bash" \
    > /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/setup-env.sh" \
    >> /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/spack-completion.bash" \
    >> /etc/profile.d/spack.sh
COPY common/handle-ssh.sh /etc/profile.d/handle-ssh.sh
COPY common/handle-prompt.sh /etc/profile.d/handle-prompt.sh.source

RUN (                                                         \
    echo "export DISTRO=$DISTRO"                            ; \
    echo "if [ x\$PROMPT '!=' 'x' -a x\$PROMPT '!=' 'x0' ]" ; \
    echo "then"                                             ; \
    echo "source /etc/profile.d/handle-prompt.sh.source"    ; \
    echo "fi"                                               ; \
) > /etc/profile.d/handle-prompt.sh

RUN mkdir -p /root/.spack
COPY common/modules.yaml /root/.spack/modules.yaml

RUN rm -f /run/nologin

RUN rm -rf /root/*.*

WORKDIR /root
ENTRYPOINT ["bash"]
CMD ["-l"]
