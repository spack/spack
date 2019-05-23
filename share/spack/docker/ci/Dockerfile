ARG BASE

FROM $BASE
MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV CURRENTLY_BUILDING_DOCKER_IMAGE=1

MASK PUSH
MASK [[ $DISTRO == centos ]]
RUN yum update -y                                          \
 && yum install -y gmp-devel libmpc-devel mpfr-devel which \
 && rm -rf /var/cache/yum                                  \
 && yum clean all

MASK [[ $DISTRO == ubuntu ]]
RUN apt-get -yqq update                                     \
 && apt-get -yqq install clang g++-5 gcc-5 gfortran-5 unzip \
 && rm -rf /var/lib/apt/lists/*


MASK [[ $DISTRO == centos ]]
# Download, build and install gcc 5.5.0
RUN mkdir -p /gcc-bld /opt/gcc/5.5.0                                    \
 && ( cd /                                                              \
 &&   curl -OL https://ftp.gnu.org/gnu/gcc/gcc-5.5.0/gcc-5.5.0.tar.xz   \
 &&   tar -xvf gcc-5.5.0.tar.xz                                         \
 &&   cd gcc-bld                                                        \
 &&   ../gcc-5.5.0/configure                                            \
          --enable-languages=c,c++,fortran                              \
          --disable-multilib                                            \
          --prefix=/opt/gcc/5.5.0                                       \
 &&   make -j\$(nproc)                                                  \
 &&   make install                                                    ) \
 && rm -rf /gcc-bld /gcc-5.5.0 /gcc-5.5.0.tar.xz

MASK POP


MASK PUSH
MASK [[ $DISTRO == centos ]]
RUN spack compiler find /opt/gcc/5.5.0                                       \
 && FORTRAN='/opt/gcc/5.5.0/bin/gfortran'                                    \
 && SED_SCRIPT="s|f77: null|f77: \${FORTRAN}|g;s|fc: null|fc: \${FORTRAN}|g" \
 && sed -i "\${SED_SCRIPT}" ~/.spack/linux/compilers.yaml

MASK [[ $DISTRO == ubuntu ]]
RUN spack compiler find gcc clang                                            \
 && FORTRAN='/usr/bin/gfortran'                                              \
 && SED_SCRIPT="s|f77: null|f77: \${FORTRAN}|g;s|fc: null|fc: \${FORTRAN}|g" \
 && sed -i "\${SED_SCRIPT}" ~/.spack/linux/compilers.yaml
MASK POP


MASK PUSH
MASK [[ $DISTRO == centos ]]
COPY update_rpaths.py /update_rpaths.py

RUN spack python /update_rpaths.py \
        --prefix /opt/gcc/5.5.0 --rpaths /opt/gcc/5.5.0/lib64

RUN ( spack install      -y llvm@6.0.0%gcc@5.5.0   \
 ||   spack install -j 1 -y llvm@6.0.0%gcc@5.5.0 ) \
 && spack clean -a

RUN spack compiler find \$(spack location -i llvm@6.0.0%gcc@5.5.0)           \
 && FORTRAN='/opt/gcc/5.5.0/bin/gfortran'                                    \
 && SED_SCRIPT="s|f77: null|f77: \${FORTRAN}|g;s|fc: null|fc: \${FORTRAN}|g" \
 && sed -i "\${SED_SCRIPT}" ~/.spack/linux/compilers.yaml

RUN PREFIX="\$(spack location -i llvm@6.0.0%gcc@5.5.0)" \
 && spack python /update_rpaths.py                      \
        --prefix "\$PREFIX" --rpaths "\$PREFIX/lib"
RUN rm /update_rpaths.py
MASK POP
