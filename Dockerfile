FROM ubuntu:16.04

RUN apt-get update \
 && apt-get install -y curl gcc python make automake
COPY . /usr/local/src/spack/
COPY docker/entrypoint.sh /usr/local/bin/
VOLUME ["/usr/local/src/spack/opt/spack/"]
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
