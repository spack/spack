# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyPyvcf(PythonPackage):
    """A Variant Call Format reader for Python"""

    homepage = "https://pyvcf.readthedocs.org/en/latest/index.html"
    pypi = "PyVCF/PyVCF-0.6.0.tar.gz"

    version('0.6.8', sha256='e9d872513d179d229ab61da47a33f42726e9613784d1cb2bac3f8e2642f6f9d9')
    version('0.6.0', sha256='d9ec3bbedb64fa35c2648a9c41fdefaedd3912ff597a436e073d27aeccf5de7c')

    depends_on('py-setuptools@:57', type='build')
    depends_on('py-argparse', when='^python@:2.6,3.0:3.1', type=('build', 'run'))
    depends_on('py-counter', when='^python@:2.6', type=('build', 'run'))
    depends_on('py-ordereddict', when='^python@:2.6', type=('build', 'run'))
    depends_on('py-unittest2', when='^python@:2.6', type=('build', 'run'))
