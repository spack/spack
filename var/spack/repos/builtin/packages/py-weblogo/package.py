# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWeblogo(PythonPackage):
    """WebLogo is a web based application designed to make the generation of
    sequence logos as easy and painless as possible."""

    homepage = "http://weblogo.threeplusone.com"
    url      = "https://pypi.io/packages/source/w/weblogo/weblogo-3.6.0.tar.gz"

    version('3.6.0', 'd0764f218057543fa664d2ae17d37b6d')

    depends_on('py-setuptools', type='build')
    depends_on('ghostscript', type=('build', 'run'))
    depends_on('pdf2svg', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
