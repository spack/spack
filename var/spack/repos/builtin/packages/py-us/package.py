# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyUs(PythonPackage):
    """US state meta information and other fun stuff."""

    homepage = "https://pypi.org/project/us/"
    url      = "https://pypi.io/packages/source/u/us/us-1.0.0.tar.gz"

    version('1.0.0', 'ce13f8d9c4202402acc1eb451e7bf22f')

    depends_on('py-setuptools', type='build')
    depends_on('py-jellyfish', type=('build', 'run'))
