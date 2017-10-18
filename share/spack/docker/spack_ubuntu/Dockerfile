
FROM ubuntu
MAINTAINER Omar Padron <omar.padron@kitware.com>

ENV DEBIAN_FRONTEND=noninteractive \
    SPACK_ROOT=/spack \
    FORCE_UNSAFE_CONFIGURE=1

RUN apt-get -yqq update && apt-get -yqq install \
    build-essential curl g++ gcc gfortran git gnupg2 lmod make python tcl && \
    git clone git://github.com/llnl/spack.git /spack && \
    rm -rf /spack/.git && rm -rf /var/lib/apt/lists/*


RUN echo "source /usr/share/lmod/lmod/init/bash" \
    > /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/setup-env.sh" \
    >> /etc/profile.d/spack.sh
RUN echo "source /spack/share/spack/spack-completion.bash" \
    >> /etc/profile.d/spack.sh

WORKDIR /spack
ENTRYPOINT ["bash"]
CMD ["-l"]

