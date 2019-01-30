# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGoatools(PythonPackage):
    """Python scripts to find enrichment of GO terms"""

    homepage = "https://github.com/tanghaibao/goatools"
    url      = "https://pypi.io/packages/source/g/goatools/goatools-0.7.11.tar.gz"

    version('0.7.11', 'f2ab989ec9c4acdd80504b263c3b3188')

    depends_on('py-nose',        type=('build', 'run'))
    depends_on('py-numpy',       type=('build', 'run'))
    depends_on('py-pandas',      type=('build', 'run'))
    depends_on('py-pydot',       type=('build', 'run'))
    depends_on('py-pyparsing',   type=('build', 'run'))
    depends_on('py-pytest',      type=('build', 'run'))
    depends_on('py-scipy',       type=('build', 'run'))
    depends_on('py-statsmodels', type=('build', 'run'))
    depends_on('py-xlrd',        type=('build', 'run'))
    depends_on('py-xlsxwriter',  type=('build', 'run'))
