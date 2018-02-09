FROM {{ image }}

# Install basic system dependencies
RUN {{ dependencies }}

ENV SPACK_ROOT=/home/spack \
    FORCE_UNSAFE_CONFIGURE=1

# Install spack + set the mirror
RUN mkdir -p $SPACK_ROOT && \
    curl -s -L https://api.github.com/repos/{{ repo }}/spack/tarball/{{ branch }} \
    | tar xzC $SPACK_ROOT --strip 1 && \
    $SPACK_ROOT/bin/spack mirror add docker-mirror /share/spack/mirror

ENTRYPOINT ["/home/spack/bin/spack"]
