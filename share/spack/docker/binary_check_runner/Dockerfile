#
# To build this image:
#
# sudo docker build -t binary_check_runner .
#

FROM ubuntu:16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential     \
        ca-certificates     \
        curl                \
        g++                 \
        gcc                 \
        gfortran            \
        git                 \
        python &&           \
    rm -rf /var/lib/apt/lists/*
