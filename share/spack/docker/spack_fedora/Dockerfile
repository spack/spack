FROM fedora
MAINTAINER Omar Padron <omar.padron@kitware.com>

ENV SPACK_ROOT=/spack \
    FORCE_UNSAFE_CONFIGURE=1

RUN dnf update -y && \
    dnf group install -y "C Development Tools and Libraries" && \
    dnf install -y \
    @development-tools \
        curl findutils gcc-c++ gcc gcc-gfortran git gnupg2 \
        Lmod make patch python tcl && \
    git clone --depth 1 git://github.com/llnl/spack.git /spack && \
    rm -rf /spack/.git && dnf clean all

RUN echo "source /usr/share/lmod/lmod/init/bash" \
    > /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/setup-env.sh" \
    >> /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/spack-completion.bash" \
    >> /etc/profile.d/spack.sh

RUN mkdir -p /root/.spack
COPY modules.yaml /root/.spack/modules.yaml

WORKDIR /spack
ENTRYPOINT ["bash"]
CMD ["-l"]
