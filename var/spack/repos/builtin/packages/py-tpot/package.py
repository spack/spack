# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
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

    depends_on('py-deap',           type=('build', 'run'))
    depends_on('py-nose',           type=('build', 'run'))
    depends_on('py-numpy',          type=('build', 'run'))
    depends_on('py-scikit-learn',   type=('build', 'run'))
    depends_on('py-scipy',          type=('build', 'run'))
    depends_on('py-tqdm',           type=('build', 'run'))
    depends_on('py-stopit',         type=('build', 'run'))
    depends_on('py-pandas',         type=('build', 'run'))
    depends_on('py-joblib',         type=('build', 'run'))

