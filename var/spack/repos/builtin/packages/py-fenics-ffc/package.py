# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsFfc(PythonPackage):
    """The FEniCS Form Compiler FFC is a compiler for finite element
    variational forms, translating high-level mathematical descriptions
    of variational forms into efficient low-level C++ code for finite
    element assembly."""

    homepage = "https://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/ffc.git"
    url      = "https://bitbucket.org/fenics-project/ffc/get/2018.1.0.post0.tar.gz"

    version('2018.1.0.post0', sha256='822011f5d7a46200a9e2a9f29a4667f3a96d7124d3c846dceaf526f29f8d3c08')
    version('2018.1.0',       sha256='51b21e3557d4c1460b2d52ff2d5646dd3d15a8b458b51706d5ff58adc9485971')
    version('2017.2.0.post0', sha256='ee8c762477ea75d98e579fc8d873e1d6ffd8e6e68994b8e3651003ecc750dc7b')
    version('2017.2.0',       sha256='f0a742e1195cf59eb10f1cce5680484bdf735777caac9ab460849659f11aa067')
    version('2017.1.0.post2', sha256='88f18685fcfc6e8f27e89f7cffe5e3a4b646f039a66e26ef4d27f26910d95734')
    version('2017.1.0.post1', sha256='d15b40f7695195e986d9f7121c907ae6a245003ae899fae9895eab40d88d4f61')
    version('2017.1.0.post0', sha256='68bfd855505f02203c90014bc4162e35ee816ad4126dc1b15c320a5dda19200a')
    version('2017.1.0',       sha256='46e6cc2d95e197f977c803a2110935bcbad35ac22d1e70e24fcc8c4f67cae908')
    version('2016.2.0',       sha256='916c94c18047e1281d08e67c515aa1d4175320723609fbbfb0fc498ab4d41bb6')
    version('2016.1.0',       sha256='f1023bd18b41fa6184770bdf379b205c6357ef23b18c7a3e50773fd706abbd62')
    version('1.6.0',          sha256='418b0b89f2e46e28611476f8269d99461c57a79b8c4e676821c2a063d3ed26c2')
    version('1.5.0',          sha256='3bf34d42cf13a0d86520f732dca7f72fcb10a87caca914110e027847af9e9ed3')
    version('1.4.0',          sha256='d45b896159e0d442457593cd7941c443f2578549f6f90ce8d1d3a3a936e48b6d')
    version('1.3.0',          sha256='1b7ff5a5aa78a5541d53dca8ae90b2a1c63d2790788cbcee14d53a5a3850c1d4')

    depends_on('python@3:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy')

    # FEniCS dependencies
    depends_on('py-fenics-fiat')
    depends_on('py-fenics-ufl')

    def url_for_version(self, version):
        url = "https://bitbucket.org/fenics-project/ffc/get"
        if version >= Version('2017.1.0'):
            url += "/{0}.tar.gz".format(version)
        else:
            url += "/ffc-{0}.tar.gz".format(version)
        return url
