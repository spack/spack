
#
# To build:
#
#     docker build --build-arg BASE_IMAGE=scottwittenburg/spack_builder_centos_7 -t spack_commander_centos_7 .
#
# or
#
#     docker build --build-arg BASE_IMAGE=scottwittenburg/spack_builder_ubuntu_18.04 -t spack_commander_ubuntu_18.04 .
#

ARG BASE_IMAGE=scottwittenburg/spack_builder_ubuntu_18.04
FROM ${BASE_IMAGE}

RUN mkdir -p /home/scott/spackcommand

COPY spack-container-command.sh /home/scott/spackcommand/spack-container-command.sh

