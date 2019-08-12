# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dos2unix(MakefilePackage):
    """DOS/Mac to Unix and vice versa text file format converter."""

    homepage = "https://waterlan.home.xs4all.nl/dos2unix.html"
    url      = "https://waterlan.home.xs4all.nl/dos2unix/dos2unix-7.3.4.tar.gz"

    version('7.3.4', '04428e77e2ead8a92c1492ba8977f1d1')

    def install(self, spec, prefix):
        make('prefix={0}'.format(prefix), 'install')
