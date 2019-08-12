# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyscaf(PythonPackage):
    """pyScaf orders contigs from genome assemblies utilising several types of
       information"""

    homepage = "https://pypi.python.org/pypi/pyScaf"
    url      = "https://pypi.io/packages/source/p/pyScaf/pyScaf-0.12a4.tar.gz"

    version('0.12a4', 'c67526747eb04d1e28279ac310916d40')

    depends_on('py-setuptools', type='build')
    depends_on('py-fastaindex', type=('build', 'run'))
