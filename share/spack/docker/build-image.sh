#! /usr/bin/env bash
#
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

script="$( basename "$0" )"
cd "$( dirname "$0" )"

export SPACK_VERSION="$( ../../../bin/spack --version )"

if [ -z "$DOCKERFILE" ] ; then
    DOCKERFILE="Dockerfile"
fi

if [ -z "$DOCKER_BUILD_CONTEXT" ] ; then
    DOCKER_BUILD_CONTEXT="../../.."
fi

if [ -z "$BASE_IMAGE" ] ; then
    BASE_IMAGE="ubuntu"
fi

if [ -z "$BASE_TAG" ] ; then
    BASE_TAG="latest"
fi

if [ -z "$TAG" ] ; then
    TAG="latest"
fi

if [ -z "$DISTRO" ] ; then
    DISTRO="${BASE_IMAGE}"
fi

if [ -z "$DISTRO_VERSION" ] ; then
    DISTRO_VERSION="${BASE_TAG}"
fi

if [ -z "$NAME" ] ; then
    NAME="${DISTRO}"
fi

if [ "$BASE_TAG" '=' 'latest' ] ; then
    BASE_TAG=""
fi

if [ "$TAG" '=' 'latest' ] ; then
    TAG=""
fi

if [ -n "$BASE_TAG" ] ; then
    BASE_TAG=":${BASE_TAG}"
fi

if [ -n "$TAG" ] ; then
    TAG=":${TAG}"
fi

eval "BASE_IMAGE=\"${BASE_IMAGE}\""
eval "BASE_TAG=\"${BASE_TAG}\""
eval "DISTRO=\"${DISTRO}\""
eval "DISTRO_VERSION=\"${DISTRO_VERSION}\""
eval "NAME=\"${NAME}\""
eval "TAG=\"${TAG}\""
eval "EXTRA_TAGS=\"${EXTRA_TAGS}\""

export BASE_IMAGE BASE_TAG DISTRO DISTRO_VERSION NAME TAG EXTRA_TAGS

if [ "$script" '=' 'run-image.sh' ] ; then
    com="docker run --rm -ti"

    if [ -z "$DISABLE_MOUNT" ] ; then
        DISABLE_MOUNT=1
        if [ -z "$*" ] ; then
            DISABLE_MOUNT=0
        fi
    fi

    if [ "$DISABLE_MOUNT" '==' 0 ] ; then
        com="${com} -v \"$( readlink -f ../../.. ):/opt/spack\""
    fi

    eval "exec ${com}" "spack/${NAME}${TAG}" "$@"
elif [ "$script" '=' 'render-image-template.sh' ] ; then
    ./dpp.bash "$DOCKERFILE"
elif [ "$script" '=' 'push-image.sh' ] ; then
    docker push "spack/${NAME}${TAG}"
    for tag in ${EXTRA_TAGS} ; do
        docker push "spack/${BASE_NAME}:${tag}"
    done
else
    tag_options="-t spack/${NAME}${TAG}"
    for tag in ${EXTRA_TAGS} ; do
        tag_options="${tag_options} -t spack/${NAME}:${tag}"
    done

    cache_options=""
    if docker pull "spack/${NAME}${TAG}" ; then
        cache_options="--cache-from spack/${NAME}${TAG}"
    fi

    exec ./render-image-template.sh |
         docker build -f -                                           \
                      ${cache_options}                               \
                      ${tag_options}                                 \
                      --build-arg BASE="${BASE_IMAGE}${BASE_TAG}"    \
                      --build-arg DISTRO="${DISTRO}"                 \
                      --build-arg DISTRO_VERSION="${DISTRO_VERSION}" \
                      "$DOCKER_BUILD_CONTEXT"
fi
