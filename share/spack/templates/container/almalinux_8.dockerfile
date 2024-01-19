{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
# import new gpg key due to key change on January 12, 2024
# https://almalinux.org/blog/2023-12-20-almalinux-8-key-update/
RUN rpm --import https://repo.almalinux.org/almalinux/RPM-GPG-KEY-AlmaLinux \
 && dnf update -y \
 && dnf install -y \
        bzip2 \
        curl \
        file \
        findutils \
        gcc-c++ \
        gcc \
        gcc-gfortran \
        git \
        gnupg2 \
        hg \
        hostname \
        iproute \
        make \
        patch \
        python3 \
        python3-pip \
        python3-setuptools \
        svn \
        unzip \
        zstd \
 && pip3 install boto3 \
 && rm -rf /var/cache/dnf \
 && dnf clean all
{% endblock %}
