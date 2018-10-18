# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyrad(PythonPackage):
    """RADseq for phylogenetics & introgression analyses"""

    homepage = "http://dereneaton.com/software/pyrad/"
    url      = "https://github.com/dereneaton/pyrad/archive/3.0.66.tar.gz"

    version('3.0.66', '19b8bcd73a574f8a25582d6e8978f0aa')

    depends_on('python@:2.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('vsearch')
    depends_on('muscle')
