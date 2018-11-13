# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUmiTools(PythonPackage):
    """Tools for handling Unique Molecular Identifiers in NGS data sets"""

    homepage = "https://github.com/CGATOxford/UMI-tools"
    url      = "https://github.com/CGATOxford/UMI-tools/archive/0.5.3.tar.gz"

    version('0.5.3', '08bdebe30f84867d352ff5e1a2fe4d94')

    depends_on('python@2.7:')
    depends_on('py-setuptools@1.1:',   type='build')
    depends_on('py-numpy@1.7:',        type=('build', 'run'))
    depends_on('py-pandas@0.12:',      type=('build', 'run'))
    depends_on('py-pysam@0.8.4:',      type=('build', 'run'))
    depends_on('py-future',            type=('build', 'run'))
    depends_on('py-six',               type=('build', 'run'))
    depends_on('py-regex',             type=('build', 'run'))
    depends_on('py-scipy',             type=('build', 'run'))
    depends_on('py-matplotlib',        type=('build', 'run'))
