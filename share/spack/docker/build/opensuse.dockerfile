FROM opensuse
MAINTAINER Omar Padron <omar.padron@kitware.com>

ENV SPACK_ROOT=/spack        \
    FORCE_UNSAFE_CONFIGURE=1 \
    DISTRO=opensuse

RUN zypper -n ref                                        && \
    zypper -n up --skip-interactive --no-recommends      && \
    zypper -n install -l --no-recommends --type pattern     \
        devel_basis                                         \
        devel_C_C++                                      && \
    zypper -n install -l --no-recommends                    \
        bash                                                \
        bash-completion                                     \
        ca-certificates                                     \
        curl                                                \
        findutils                                           \
        gcc                                                 \
        gcc-locale                                          \
        gcc-c++                                             \
        gcc-fortran                                         \
        git                                                 \
        glibc-locale                                        \
        gpg2                                                \
        hostname                                            \
        iproute                                             \
        lua-lmod                                            \
        make                                                \
        patch                                               \
        openssh                                             \
        python                                              \
        python-xml                                          \
        tcl                                              && \
    git clone --depth 1 git://github.com/spack/spack.git /spack && \
    zypper clean                                                && \
    rm -rf /spack/.git /var/cache/zypp/*

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
