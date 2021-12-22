# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-datrie
#
# You can edit this file again by typing:
#
#     spack edit py-datrie
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyDatrie(PythonPackage):
    """Super-fast, efficiently stored Trie for Python (2.x and 3.x). Uses libdatrie."""

    pypi = "datrie/datrie-0.8.2.tar.gz"
    maintainers = ['marcusboden']

    version('0.8.2', '525b08f638d5cf6115df6ccd818e5a01298cd230b2dac91c8ff2e6499d18765d')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',  type=('build'))
    depends_on('py-cython', type='build')
    depends_on('py-pytest-runner', type='build')
