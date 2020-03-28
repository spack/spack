# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Meson(PythonPackage):
    """Meson is a portable open source build system meant to be both
       extremely fast, and as user friendly as possible."""

    homepage = "http://mesonbuild.com/"
    url      = "https://github.com/mesonbuild/meson/archive/0.49.0.tar.gz"

    version('0.53.2', sha256='eab4f5d5dde12d002b7ddd958a9a0658589b63622b6cea2715e0235b95917888')
    version('0.49.1', sha256='a944e7f25a2bc8e4ba3502ab5835d8a8b8f2530415c9d6fcffb53e0abaea2ced')
    version('0.49.0', sha256='11bc959e7173e714e4a4e85dd2bd9d0149b0a51c8ba82d5f44cc63735f603c74')
    version('0.42.0', sha256='6c318a2da3859326a37f8a380e3c50e97aaabff6990067218dffffea674ed76f')
    version('0.41.2', sha256='2daf448d3f2479d60e30617451f09bf02d26304dd1bd12ee1de936a53e42c7a4')
    version('0.41.1', sha256='a48901f02ffeb9ff5cf5361d71b1fca202f9cd72998043ad011fc5de0294cf8b')

    variant('ninjabuild', default=True)

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('ninja', when='+ninjabuild', type=('build', 'run'))

    # By default, Meson strips the rpath on installation. This patch disables
    # rpath modification completely to make sure that Spack's rpath changes
    # are not reverted.
    patch('rpath.patch', when='@0.49:')
