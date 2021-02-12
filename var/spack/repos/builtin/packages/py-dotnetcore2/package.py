# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys


class PyDotnetcore2(Package):
    """.Net Core 2.1 runtime."""

    homepage = "https://github.com/dotnet/core"

    if sys.platform == 'darwin':
        version('2.1.20', sha256='08af4595570797eb1af813e1421da10a28433933448c1585241a307e8d5d3a9f')
    version('2.1.19', sha256='e5a7280fbcdb8e3b4b4ce8e73930e10d0436102d124087b6972d014d057e56d7')
    version('2.1.18', sha256='6b22b6999dfa9b646b6df04cfe27507100e42521bfee06889326d58ee50bf98a')
    version('2.1.17', sha256='4bc7e65ff12a2f8ef4798a0d4c7c9eb4c6370f114aceb194adaf1ac7c453d8e6')
    version('2.1.16', sha256='e017d171bb3f94168945f1af8afdcc2533afd12fc63bd6bbb10dfe9cf1d783f8')
    version('2.1.15', sha256='b7426c0237bcb382880ec1685d468d412cd5e0d56a3c6fe2ed34d589284146ce')
    version('2.1.14', sha256='68182f4b704db401b2012c10ed8a19561f8d487063632f8731c2e58960ca9242', expand=False,
                url='https://pypi.io/packages/py3/d/dotnetcore2/dotnetcore2-2.1.14-py3-none-macosx_10_9_x86_64.whl')
    elif sys.platform.startswith('linux'):
        version('2.1.14', sha256='d8d83ac30c22a0e48a9a881e117d98da17f95c4098cb9500a35e323b8e4ab737', expand=False,
                url='https://pypi.io/packages/py3/d/dotnetcore2/dotnetcore2-2.1.14-py3-none-manylinux1_x86_64.whl')

    conflicts('target=ppc64:', msg='py-dotnetcore2 is only available for x86_64')
    conflicts('target=ppc64le:', msg='py-dotnetcore2 is only available for x86_64')
    conflicts('target=aarch64:', msg='py-dotnetcore2 is only available for x86_64')

    extends('python')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-distro@1.2.0:', type=('build', 'run'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
