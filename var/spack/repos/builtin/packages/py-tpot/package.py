# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install py-tpot
#
# You can edit this file again by typing:
#
#     spack edit py-tpot
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyTpot(PythonPackage):
    """A Python Automated Machine Learning tool that optimizes machine learning pipelines using genetic programming."""

    homepage = "http://epistasislab.github.io/tpot/"
    url      = "https://github.com/EpistasisLab/tpot/archive/v0.10.2.tar.gz"

    version('0.10.2', sha256='a35c4b7ff1927168a440327004f71d7dd09b6540ab38a951dc0748df5aa91b30')
    version('0.10.1', sha256='21cf91c38cd496f13bd96f343592c889965ef015ee3416bef96a0ea4188b937b')
    version('0.10.0', sha256='4c97ca4ed4baea5a8b99fbe70a949c55d7ed53a822d942cea8d0691c7aa2c011')
    version('0.9.6',  sha256='d4bf08486ed71d2f2cc715eaf663ccb9fbe3d41eb70086cd7db9ac1f85bfba93')
    version('0.9.5',  sha256='178d259f15be1efc758fd38d0a449add283d1fb341a1ce7b390c618b19453c39')

    depends_on('py-deap',           type=('build', 'run'))
    depends_on('py-nose',           type=('build', 'run'))
    depends_on('py-numpy',          type=('build', 'run'))
    depends_on('py-scikit-learn',   type=('build', 'run'))
    depends_on('py-scipy',          type=('build', 'run'))
    depends_on('py-tqdm',           type=('build', 'run'))
    #depends_on('py-update-checker', type=('build', 'run'))
    depends_on('py-stopit',         type=('build', 'run'))
    depends_on('py-pandas',         type=('build', 'run'))
    depends_on('py-joblib',         type=('build', 'run'))

