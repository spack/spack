# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ccache(AutotoolsPackage):
    """ccache is a compiler cache. It speeds up recompilation by caching
    previous compilations and detecting when the same compilation is being done
    again."""

    homepage = "https://ccache.samba.org/"
    url      = "https://www.samba.org/ftp/ccache/ccache-3.3.4.tar.gz"

    version('3.3.4', '61326f1edac7cd211a7018458dfe2d86')
    version('3.3.3', 'ea1f95303749b9ac136c617d1b333eef')
    version('3.3.2', 'b966d56603e1fad2bac22930e5f01830')
    version('3.3.1', '7102ef024cff09d353b3f4c48379b40b')
    version('3.3', 'b7ac8fdd556f93831618483325fbb1ef')
    version('3.2.9', '8f3f6e15e75a0e6020166927d41bd0b3')

    depends_on('gperf')
    depends_on('libxslt')
    depends_on('zlib')
