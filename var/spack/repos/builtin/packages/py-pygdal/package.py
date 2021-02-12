# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygdal(PythonPackage):
    """
    Virtualenv and setuptools friendly version of standard GDAL python
    bindings.

    This package is for you if you had problems installing GDAL in your
    virtualenv. You can install GDAL into your virtualenv using this package
    but you still need to install GDAL library and its header files on your
    system.
    """

    homepage = "https://github.com/nextgis/pygdal"
    pypi = "pygdal/pygdal-3.0.1.5.tar.gz"

    version('3.2.1.6', sha256='c99cb36b1f22b78e3bef0a8dc78be1d20ff9f01b444ffa25eee4b1cd1ff192f2')
    version('3.2.0.6', sha256='2659066eadd3dc5da3f54ac86a1e292b2b13961bf1c2dec0de53d8308ead94a4')
    version('3.1.4.6', sha256='0b07f6ebf1c9a98dbd2da0c0239c81e7714cd58085619aa4c500be7e69ad37a9')
    version('3.1.3.6', sha256='e104da30ec6d68bf0f3e2f740d89ff70a1f0c337422dfe2d76d1ba36be2adfe6')
    version('3.1.2.6', sha256='d6a1df815259ab5f0c3988c6e2fa318881576509d38b870ce4a95d58aa08f375')
    version('3.1.1.6', sha256='dd37ebf53705e91051a95da958214eb5d3e14a4800af8c4066feaa246b9ad18b')
    version('3.1.0.6', sha256='d1c4677a471dfa0dbd282155d61388c2edb87f9b5b6f7d6628270c38ce4bd833')
    version('3.0.4.6', sha256='8e39b58cd9465bb5f41786a7cf6a62df93334c104db05a5bfb8181a0be276b86')
    version('3.0.1.5', sha256='1222f69fe5e6b632d0d2a42d3acb8fac80fb4577c05e01969d8cd5548192ccaa')
    version('2.4.2.5', sha256='73386683c0b10ab43b6d64257fca2ba812f53ec61b268de8811565fd9ae9bacd')
    version('2.4.1.6', sha256='5d1af98ad09f59e34e3b332cf20630b532b33c7120295aaaabbccebf58a11aa4')
    version('2.4.0.6', sha256='728d11f3ecae0cd3493cd27dab599a0b6184f5504cc172d49400d88ea2b24a9c')
    version('1.11.5.3', sha256='746d13b73a284446a1b604772f869789eabfe6e69dee463f537da27845b29fa7')
    version('1.11.4.3', sha256='99d4b0c94d57ae50592924faaa65cc6a0c0892d83764e9f24ef9270c3a4b111a')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.0.0:', type=('build', 'run'))
    depends_on('gdal@3.0.4', type=('build', 'link', 'run'), when='@3.0.4.6')
    depends_on('gdal@3.0.1', type=('build', 'link', 'run'), when='@3.0.1.5')
    depends_on('gdal@2.4.2', type=('build', 'link', 'run'), when='@2.4.2.5')
    depends_on('gdal@2.4.1', type=('build', 'link', 'run'), when='@2.4.1.6')
    depends_on('gdal@2.4.0', type=('build', 'link', 'run'), when='@2.4.0.6')
    depends_on('gdal@1.11.5', type=('build', 'link', 'run'), when='@1.11.5.3')
    depends_on('gdal@1.11.4', type=('build', 'link', 'run'), when='@1.11.4.3')
