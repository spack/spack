FROM base/archlinux
MAINTAINER Omar Padron <omar.padron@kitware.com>

ENV SPACK_ROOT=/spack        \
    FORCE_UNSAFE_CONFIGURE=1 \
    DISTRO=arch

RUN pacman -Sy --noconfirm  \
        base-devel          \
        ca-certificates     \
        curl                \
        gcc                 \
        gcc-fortran         \
        git                 \
        gnupg2              \
        iproute2            \
        make                \
        openssh             \
        python              \
        sudo                \
        tcl              && \
    git clone --depth 1 git://github.com/spack/spack.git /spack             && \
    echo 'nobody ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/nobody-sudo      && \
    sudo -u nobody git clone --depth 1                                         \
        https://aur.archlinux.org/lua-posix.git /tmp/lua-posix              && \
    sudo -u nobody git clone --depth 1                                         \
        https://aur.archlinux.org/lmod.git /tmp/lmod                        && \
    ( cd /tmp/lua-posix ; sudo -u nobody makepkg -si --asdeps --noconfirm ) && \
    ( cd /tmp/lmod      ; sudo -u nobody makepkg -si          --noconfirm ) && \
    rm -rf /tmp/lua-posix /tmp/lmod /spack/.git /etc/sudoers.d/nobody-sudo

RUN ( cd /usr/share/lmod ; ln -s $( ls -d ./* | head -n 1 ) ./lmod )

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

RUN rm -rf /root/*.*

WORKDIR /root
ENTRYPOINT ["bash"]
CMD ["-l"]
