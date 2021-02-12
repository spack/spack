# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Skopeo(MakefilePackage):
    """skopeo is a command line utility that performs various operations on
    container images and image repositories."""

    homepage = "https://github.com/containers/skopeo"
    url      = "https://github.com/containers/skopeo/archive/v0.1.39.tar.gz"

    version('1.2.1',  sha256='aed062afdd9aed305679294a0c238d0f39b8a206084db1c6e6aa3b1e20c71be8')
    version('1.2.0',  sha256='113290f6747b7a9946ddf50ad1a7d924d3e507fe923b2e0460df1e6823de0ffb')
    version('1.1.1',  sha256='9e0fdca1f2663f5a07bc1d932fec734578c5fffdb27faa8f847a393a44b072df')
    version('1.1.0',  sha256='3bd3acc614514fc2261b89dc0ea85ac7a4dba64fb7dcef8676ae61849e8faeb4')
    version('1.0.0',  sha256='df5f38ee72e2fede508d1fd272a48773b86eb6bc6cc4b7b856a99669d22fa5df')
    version('0.2.0',  sha256='b58c54732932cdd89f760f30136317fc2fef6457d158fb1e5d4976aeabcb20f2')
    version('0.1.41', sha256='d9f4a0dcf4a43469768dbf16865d5bc98e5434fadd65af35051edb36767c9c70')
    version('0.1.40', sha256='ee1e33245938fcb622f5864fac860e2d8bfa2fa907af4b5ffc3704ed0db46bbf')
    version('0.1.39', sha256='e9d70f7f7b891675a816f06a22df0490285ad20eefbd91f5da69ca12f56c29f2')
    version('0.1.38', sha256='104ceb9c582dc5c3a49dd1752c4c326bba03f2f801596f089372e831f48ed705')
    version('0.1.37', sha256='49c0c1b2c2f32422d3230f827ae405fc554fb34af41a54e59b2121ac1500505d')
    version('0.1.36', sha256='42f9b0bf53ae44bc294be400e2c5259f977ffa4d5dbac3576b0b5e23d59791fd')

    depends_on('go')
    depends_on('go-md2man', type='build')
    depends_on('gpgme')
    depends_on('libassuan')
    depends_on('libgpg-error')
    depends_on('lvm2')

    def edit(self, spec, prefix):
        grep = which('grep')
        files = grep('-lR', '/etc/containers/', 'vendor', output=str,
                     env={'PATH': '/usr/bin:/bin:/usr/sbin:/sbin'})

        for f in files.splitlines():
            edit = FileFilter(f)
            edit.filter('/etc/containers/', '{0}/etc/containers/'.
                        format(prefix))

    def build(self, spec, prefix):
        make('binary-local')

    def install(self, spec, prefix):
        make('binary-local', 'install',
             'DESTDIR={0}'.format(prefix),
             'PREFIX={0}'.format(prefix))
