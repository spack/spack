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

    version('1.19.1', sha256='18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6')
    version('1.19.0', sha256='2835b11829ee634e19fa56517b4cfc52ef39acea0cd82e15f68096e27cbed0ba')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        spack_env.append_path('ACLOCAL_PATH',
                              join_path(self.prefix.share, 'aclocal'))
