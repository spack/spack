{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
RUN yum update -y \
 && yum install -y epel-release \
 && yum update -y \
 && yum --enablerepo epel install -y \
        bzip2 \
        curl-minimal \
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
        xz \
        zstd \
 && pip3 install boto3 \
 && rm -rf /var/cache/yum \
 && yum clean all
{% endblock %}
