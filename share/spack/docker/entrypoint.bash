#! /usr/bin/env bash -e
#
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

unset CURRENTLY_BUILDING_DOCKER_IMAGE

if [ "$1" '=' 'docker-shell' ] ; then
    if [ -t 0 ] ; then
        exec bash -il
    else
        (
            echo -n "It looks like you're trying to run an intractive shell"
            echo -n " session, but either no psuedo-TTY is allocateed for this"
            echo -n " container's STDIN, or it is closed."
            echo

            echo -n "Make sure you run docker with the --interactive and --tty"
            echo -n " options."
            echo
        ) >&2

        exit 1
    fi
else
    exec 3>&1
    exec 4>&2

    exec 1>&-
    exec 2>&-

    source /etc/profile.d/spack.sh
    source /etc/profile.d/handle-ssh.sh

    exec 1>&3
    exec 2>&4

    exec 3>&-
    exec 4>&-

    spack "$@"
    exit $?
fi
