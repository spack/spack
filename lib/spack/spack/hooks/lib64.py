# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


def post_install(spec):
    """Many places in Spack expect libraries to be in the lib directory.
    Some architectures (such as openSUSE) produce lib64 directories, though.
    If there is a lib64 directory but no lib directory, this hook creates
    a symlink to make sure libraries can be found."""
    if spec.external:
        return

    if os.path.lexists(spec.prefix.lib64) \
       and not os.path.lexists(spec.prefix.lib):
        os.symlink('lib64', spec.prefix.lib)
