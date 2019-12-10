FROM ubuntu:18.04 AS base

ENV FORCE_UNSAFE_CONFIGURE=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get -yqq update \
 && apt-get -yqq install \
     --no-install-recommends \
     --no-install-suggests \
        base-files \
        ca-certificates \
        debianutils \
        less \
        locales \
 && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen \
 && rm -rf /var/lib/apt/lists/*

ENV LANGUAGE=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

FROM base AS bootstrap

ENV SPACK_ROOT=/spack

RUN apt-get -yqq update \
 && apt-get -yqq install \
     --no-install-recommends \
     --no-install-suggests \
        curl \
        file \
        g++ \
        gcc \
        libc-dev-bin \
        libc6-dev \
        locales \
        make \
        python3 \
        tar \
 && rm -rf /var/lib/apt/lists/*

COPY bin /spack/bin
COPY etc /spack/etc
COPY lib /spack/lib

COPY share/spack/csh /spack/share/spack/csh
COPY share/spack/docs /spack/share/spack/docs
COPY share/spack/logo /spack/share/spack/logo
COPY share/spack/qa /spack/share/spack/qa
COPY share/spack/setup-env.* /spack/share/spack/
COPY share/spack/spack-completion.bash /spack/share/spack
COPY share/spack/templates /spack/share/spack/templates

COPY share/spack/docker/*.* /spack/share/spack/docker/
COPY share/spack/docker/package-index /spack/share/spack/docker/package-index

COPY var /spack/var

COPY share/spack/docker/conf/0* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 0

COPY share/spack/docker/conf/1* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 1

COPY share/spack/docker/conf/2* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 2

COPY share/spack/docker/conf/3* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 3

RUN /spack/bin/spack clean -a

FROM base

MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV SPACK_ROOT=/opt/spack

COPY --from=bootstrap /spack /opt/spack

RUN ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /bin/docker-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /bin/interactive-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /bin/spack-env \
\
# [WORKAROUND]
# https://superuser.com/questions/1241548/
#     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
 && for dir in /root /etc/skel ; do \
      if [ '!' -f "$dir/.profile" ] ; then continue ; fi \
 ;    sed -i 's/mesg n/(tty -s \&\& mesg n || true)/g' "$dir/.profile" \
 ;    done \
\
# create unprivileged user
 && addgroup --quiet --system --gid 1000 spack \
 && adduser --quiet --system --home /home/spack --shell /bin/sh \
        --disabled-password --uid 1000 --gid 1000 spack \
\
# [WORKAROUND]
# Workaround an issue where nonprivileged user cannot install packages
# because spack tries to create- and write to files under-
#     $spack/var/spack/junit-report
#   (/spack is given to "spack" user below)
# TODO: report this issue
 && rm -rf $SPACK_ROOT/var/spack/junit-report \
 && mkdir -p /spack/junit-report \
 && ln -s /spack/junit-report $SPACK_ROOT/var/spack/junit-report

COPY --from=bootstrap /etc/spack /etc/spack
COPY --from=bootstrap /spack-bootstrap /spack-bootstrap

RUN ln -s /spack-bootstrap/sw/*/*/file*/bin/file /usr/bin/file \
 && ln -s /spack-bootstrap/sw/*/*/python*/bin/python /usr/bin/python \
 && /opt/spack/bin/spack view symlink /usr/local \
      bzip2 \
      coreutils \
      curl \
      diffutils \
      file \
      git \
      gmake \
      gnupg \
      gzip \
      nano \
      patch \
      patchelf \
      python \
      py-boto3 \
      py-pip \
      sed \
      tar \
      unzip \
      xz \
 && chown -R spack:spack /spack \
 && rm -rf /usr/bin/file /usr/bin/python /root/*.* /root/.spack

SHELL ["docker-shell"]

RUN spack load gcc \
 && spack compiler find --scope system \
 && find "$( spack location --install gcc )/libexec" \
        -iname 'mkheaders' -exec '{}' ';' -quit

USER spack
WORKDIR /home/spack

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["interactive-shell"]
