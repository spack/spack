# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qwtpolar(QMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://sourceforge.net/projects/qwtpolar/files/qwtpolar/1.1.1/qwtpolar-1.1.1.tar.bz2"

    version('1.1.1', sha256='6168baa9dbc8d527ae1ebf2631313291a1d545da268a05f4caa52ceadbe8b295')

    depends_on('qt')
    depends_on('qwt@6.1:')

#    def qmake_args(self):
#        # FIXME: If not needed delete this function
#        args = []
#        return args
