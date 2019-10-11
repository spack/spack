# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEmcee(PythonPackage):
    """emcee is an MIT licensed pure-Python implementation of Goodman & Weare's
    Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler."""

    homepage = "http://dan.iel.fm/emcee/current/"
    url = "https://pypi.io/packages/source/e/emcee/emcee-2.2.1.tar.gz"

    version('2.2.1', sha256='b83551e342b37311897906b3b8acf32979f4c5542e0a25786ada862d26241172')
    version('2.1.0', 'c6b6fad05c824d40671d4a4fc58dfff7')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
