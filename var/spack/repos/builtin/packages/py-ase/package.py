# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAse(PythonPackage):
    """The Atomic Simulation Environment (ASE) is a set of tools
    and Python modules for setting up, manipulating, running,
    visualizing and analyzing atomistic simulations."""

    homepage = "https://wiki.fysik.dtu.dk/ase/"
    url      = "https://pypi.io/packages/source/a/ase/ase-3.13.0.tar.gz"

    version('3.18.0',
            sha256='39d45f12def2669605bffc82926acfb13a0d0610e6d82740fa316aafa70f97f9')
    version('3.15.0', '65a0143753517c2df157e53bd29a18e3')
    version('3.13.0', 'e946a0addc5b61e5e2e75857e0f99b89')

    depends_on('python@2.6:', type=('build', 'run'), when='@:3.15.0')
    depends_on('python@3.5:', type=('build', 'run'), when='@3.18.0:')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-flask', type=('build', 'run'))
