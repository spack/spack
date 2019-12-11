# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNetworkit(PythonPackage):
    """NetworKit is a growing open-source toolkit for large-scale network analysis. Its aim is to provide tools for the analysis of large networks in the size range from thousands to billions of edges. For this purpose, it implements efficient graph algorithms, many of them parallel to utilize multicore architectures. These are meant to compute standard measures of network analysis, such as degree sequences, clustering coefficients, and centrality measures. In this respect, NetworKit is comparable to packages such as NetworkX, albeit with a focus on parallelism and scalability."""

    homepage = "https://networkit.github.io/"
    git      = "https://github.com/networkit/networkit.git"
    version('6.0', tag='6.0', submodules=True)

    # Required dependencies
    depends_on('libnetworkit', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('cmake', type='build')
    depends_on('ninja', type='build')
    depends_on('py-cython', type='build')
    depends_on('openmpi', type='build')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))

    phases = ['build_ext', 'install']

    networkit_folder = ""

    def build_ext_args(self, spec, prefix):
        networkit_folder = format(spec['libnetworkit'].prefix)
        rpath = self.rpath
        rpath.append(format(spec['libnetworkit'].prefix.lib))
        args = ['--networkit-external-core']
        args.extend(['--rpath=%s' % ":".join(rpath)])
        return args
