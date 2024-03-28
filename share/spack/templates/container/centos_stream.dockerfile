{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
RUN dnf update -y \
 # See https://fedoraproject.org/wiki/EPEL#Quickstart for powertools
 && dnf install -y dnf-plugins-core \
 && dnf config-manager --set-enabled powertools \
 && dnf install -y epel-release \
 && dnf update -y \
 && dnf --enablerepo epel groupinstall -y "Development Tools" \
 && dnf --enablerepo epel install -y \
        curl \
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
        svn \
        patch \
        python3.11 \
        python3.11-setuptools \
        unzip \
        zstd \
 && python3.11 -m ensurepip \
 && pip3.11 install boto3 \
 && rm -rf /var/cache/dnf \
 && dnf clean all
{% endblock %}
