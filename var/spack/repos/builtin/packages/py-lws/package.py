# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyLws(PythonPackage):
    """Fast spectrogram phase recovery using Local Weighted Sums"""

    homepage = "https://pypi.org/project/lws/"
    url      = "https://files.pythonhosted.org/packages/51/a8/3f1727af04052008a748acba02b561b42e63ae275da03a63266ebc3ef64e/lws-1.2.6.tar.gz"
    git      = "https://github.com/Jonathan-LeRoux/lws"

    maintainers = ['jonathanleroux']

    version('1.2.6', sha256='ac94834832aadfcd53fcf4a77e1d95155063b39adbce14c733f8345bdac76e87')

    depends_on('python',          type=('build', 'run'))
    depends_on('py-setuptools',   type='build')
    depends_on('py-numpy',        type=('build', 'run'))
    depends_on('py-scipy',        type=('build', 'run'))
