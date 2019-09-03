#! /usr/bin/env bash -e
#
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

exec 3>&1
exec 4>&2

exec 1>&-
exec 2>&-

for script in $( find /etc/profile.d -type f \
                                     -iname '*.sh' \
                                     -not -iname 'handle-prompt.sh' \
                                     -not -iname 'handle-ssh.sh' \
                                     -not -iname 'spack.sh' )
do
    source "$script"
done

source "$SPACK_ROOT/share/spack/docker/shell-helpers.bash"
setup_spack

exec 1>&3
exec 2>&4

exec 3>&-
exec 4>&-

exec "bash" "-c" "$*"
