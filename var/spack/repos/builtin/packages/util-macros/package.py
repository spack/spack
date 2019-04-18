# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class UtilMacros(AutotoolsPackage):
    """This is a set of autoconf macros used by the configure.ac scripts in
    other Xorg modular packages, and is needed to generate new versions
    of their configure scripts with autoconf."""

    homepage = "http://cgit.freedesktop.org/xorg/util/macros/"
    url = "https://www.x.org/archive/individual/util/util-macros-1.19.1.tar.bz2"

    version('1.19.1', '6e76e546a4e580f15cebaf8019ef1625')
    version('1.19.0', '1cf984125e75f8204938d998a8b6c1e1')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        spack_env.append_path('ACLOCAL_PATH',
                              join_path(self.prefix.share, 'aclocal'))
