# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNetworkit(PythonPackage):
    """NetworKit is a growing open-source toolkit for large-scale network analysis.
       Its aim is to provide tools for the analysis of large networks in the
       size range from thousands to billions of edges. For this purpose, it
       implements efficient graph algorithms, many of them parallel to utilize
       multicore architectures. These are meant to compute standard measures of
       network analysis, such as degree sequences, clustering coefficients, and
       centrality measures. In this respect, NetworKit is comparable to
       packages such as NetworkX, albeit with a focus on parallelism
       and scalability."""

    homepage = "https://networkit.github.io/"
    url      = "https://pypi.python.org/packages/source/n/networkit/networkit-5.0.tar.gz"

    version('5.0', sha256='4fd9439a155cc569000ec039e13680804d8cc233c6d602c88cf0f63174b2babd')

    # Required dependencies
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('cmake', type='build')
    depends_on('ninja', type='build')
    depends_on('py-cython', type='build')
    depends_on('openmpi', type='build')
    depends_on('py-scikit-learn', type='run')
    depends_on('py-networkx', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-matplotlib', type='build')
    depends_on('py-seaborn', type='run')
    depends_on('py-ipython', when='~python3', type='run')
    depends_on('py-jupyter-console', type='run')
    depends_on('py-tabulate', type='run')