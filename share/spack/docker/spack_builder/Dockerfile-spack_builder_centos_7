
#
# To build this image:
#
# cd <path-to-spack-repo>/share/spack/docker/spack_builder
# docker build -f Dockerfile-spack_builder_centos_7 -t spack_builder_centos_7 .
#

from spack/centos:7

RUN yum update -y          && \
    yum install -y            \
        gmp-devel             \
        libmpc-devel          \
        mpfr-devel            \
        vim                   \
        which              && \
    rm -rf /var/cache/yum && yum clean all

# Download, build and install gcc 5.5.0
RUN mkdir -p /home/spackuser/Download/gcc550/build-gcc550            && \
    mkdir -p /opt/gcc/gcc-5.5.0                                      && \
    cd /home/spackuser/Download/gcc550                               && \
    curl -OL https://ftp.gnu.org/gnu/gcc/gcc-5.5.0/gcc-5.5.0.tar.xz  && \
    tar -xvf gcc-5.5.0.tar.xz                                        && \
    cd build-gcc550                                                  && \
    ../gcc-5.5.0/configure                                              \
        --enable-languages=c,c++,fortran                                \
        --disable-multilib                                              \
        --prefix=/opt/gcc/gcc-5.5.0                                  && \
    make -j$(nproc)                                                  && \
    make install                                                     && \
    cd /home/spackuser                                               && \
    rm -rf /home/spackuser/Download

RUN export PATH=/spack/bin:$PATH              && \
    spack compiler find /opt/gcc/gcc-5.5.0

RUN sed -i 's/f77: null/f77: \/opt\/gcc\/gcc-5.5.0\/bin\/gfortran/g;s/fc: null/fc: \/opt\/gcc\/gcc-5.5.0\/bin\/gfortran/g' ~/.spack/linux/compilers.yaml

RUN mkdir -p /home/spackuser/spackcommand

COPY update_rpaths.py /home/spackuser/spackcommand/update_rpaths.py

RUN spack python /home/spackuser/spackcommand/update_rpaths.py  \
        --prefix /opt/gcc/gcc-5.5.0                             \
        --rpaths /opt/gcc/gcc-5.5.0/lib64

RUN export PATH=/spack/bin:$PATH              && \
    spack install -y llvm@6.0.0%gcc@5.5.0     && \
    spack clean -a

RUN export PATH=/spack/bin:$PATH                                     && \
    spack compiler find $(spack location -i llvm@6.0.0%gcc@5.5.0)

RUN sed -i 's/f77: null/f77: \/opt\/gcc\/gcc-5.5.0\/bin\/gfortran/g;s/fc: null/fc: \/opt\/gcc\/gcc-5.5.0\/bin\/gfortran/g' ~/.spack/linux/compilers.yaml

RUN spack python /home/spackuser/spackcommand/update_rpaths.py  \
        --prefix /spack/opt/spack/linux-centos7-x86_64/gcc-5.5.0/llvm-6.0.0-awfpo7kn3k24weu655rrt2erihzd4gii                             \
        --rpaths /spack/opt/spack/linux-centos7-x86_64/gcc-5.5.0/llvm-6.0.0-awfpo7kn3k24weu655rrt2erihzd4gii/lib

