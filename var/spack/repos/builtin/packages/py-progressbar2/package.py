# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyProgressbar2(PythonPackage):
    """A progress bar for Python 2 and Python 3"""

    homepage = "https://github.com/WoLpH/python-progressbar"
    url      = "https://files.pythonhosted.org/packages/source/p/progressbar2/progressbar2-3.39.3.tar.gz"

    version('3.39.3', sha256='8e5b5419e04193bb7c3fea71579937bbbcd64c26472b929718c2fe7ec420fe39')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-python-utils', type=('build', 'run'))
