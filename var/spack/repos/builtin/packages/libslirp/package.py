# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Libslirp(MesonPackage):
    """General purpose TCP-IP emulator"""

    homepage    = 'https://gitlab.freedesktop.org/slirp/libslirp'
    url         = 'https://gitlab.freedesktop.org/slirp/libslirp/-/archive/v4.6.1/libslirp-v4.6.1.tar.gz'
    maintainers = ['bernhardkaindl']

    version('4.6.1', sha256='69ad4df0123742a29cc783b35de34771ed74d085482470df6313b6abeb799b11')

    depends_on('pkgconfig', type='build')
    depends_on('glib')
