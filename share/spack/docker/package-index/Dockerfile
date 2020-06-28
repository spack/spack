# prepare the package index in form of JSON files
FROM ubuntu:18.04 AS build-env

ENV SPACK_ROOT=/opt/spack             \
    DEBIAN_FRONTEND=noninteractive

COPY bin     $SPACK_ROOT/bin
COPY etc     $SPACK_ROOT/etc
COPY lib     $SPACK_ROOT/lib
COPY share   $SPACK_ROOT/share
COPY var     $SPACK_ROOT/var

RUN apt-get -yqq update   \
 && apt-get -yqq install  \
        bash jq python    \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /build
# single, large index file
RUN $SPACK_ROOT/bin/spack list --format version_json > packages.json
# individual packages split into a tree of :firstLetter/:packageName.json
RUN $SPACK_ROOT/share/spack/docker/package-index/split.sh

# nginx web service
FROM nginx:mainline-alpine
MAINTAINER Spack Maintainers <maintainers@spack.io>
COPY --from=build-env --chown=nginx:nginx /build/packages /build/packages.json /usr/share/nginx/html/api/
COPY share/spack/docker/package-index/cors-header.conf /etc/nginx/conf.d/

CMD ["nginx", "-g", "daemon off;"]
