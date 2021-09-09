# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gnuconfig(Package):
    """
    The GNU config.guess and config.sub scripts versioned by timestamp.
    This package can be used as a build dependency for autotools packages that
    ship a tarball with outdated config.guess and config.sub files.
    """

    has_code = False

    version('2021-08-14')

    def install(self, spec, prefix):
        touch(join_path(prefix, 'config.sub'))
        touch(join_path(prefix, 'config.guess'))
