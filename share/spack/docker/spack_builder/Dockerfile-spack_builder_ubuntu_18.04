
#
# To build this image:
#
# cd <path-to-spack-repo>/share/spack/docker/spack_builder
# docker build -f Dockerfile-spack_builder_ubuntu_18.04 -t spack_builder_ubuntu_18.04 .
#

from spack/ubuntu:bionic

RUN apt-get -yqq update && apt-get -yqq install \
        clang                                   \
        g++-5                                   \
        gcc-5                                   \
        gfortran-5                              \
        unzip                                   \
        vim                                  && \
    rm -rf /var/lib/apt/lists/*

RUN export PATH=/spack/bin:$PATH             && \
    spack compiler find gcc clang

RUN sed -i 's/f77: null/f77: \/usr\/bin\/gfortran/g;s/fc: null/fc: \/usr\/bin\/gfortran/g' ~/.spack/linux/compilers.yaml
