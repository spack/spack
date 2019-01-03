# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsDijitso(PythonPackage):
    """A Python module for distributed just-in-time compilation
    of shared object files."""

    homepage = "https://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/dijitso.git"

    def url_for_version(self, version):
        url = "https://bitbucket.org/fenics-project/dijitso/get"
        if version >= Version('2017.1.0'):
            url += "/{0}.tar.gz".format(version)
        else:
            url += "/dijitso-{0}.tar.gz".format(version)
        return url

    version('2018.1.0',       sha256='2a768a5aac0414c1719a0ea5d66c788d6f8d0838d3b669ecb26e35ff9e452f09')
    version('2017.2.0',       sha256='b759a384cd1c6bf50476803f0277cd6e7a1fdaaee922c7952641bce8c8336678')
    version('2017.1.0.post1', sha256='8c729ad9ef8d04cdf40e11808dc9700bcaff34ccefa72ab5d9af16dabc61feb9')
    version('2017.1.0',       sha256='cb9282888023fb6ee0355a0c022c2a17bd07617ab34e86bb33153af8e5d3c6cf')
    version('2016.2.0',       sha256='7358c6cbeacaada3ef3071bdcf2a5f342cb7ee1ed736742d2b747b1fd4454d4c')
    version('2016.1.0',       sha256='3f820665d114367739fd30d5c1b76e06e9057f9fff70cd3e2f45f2df1936cc23')

    depends_on('python@3:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
