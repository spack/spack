# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mono(AutotoolsPackage):
    """Mono is a software platform designed to allow developers to easily
       create cross platform applications. It is an open source
       implementation of Microsoft's .NET Framework based on the ECMA
       standards for C# and the Common Language Runtime.
    """

    homepage = "http://www.mono-project.com/"
    url      = "https://download.mono-project.com/sources/mono/mono-5.0.1.1.tar.bz2"

    # /usr/share/.mono/keypairs needs to exist or be able to be
    # created, e.g. https://github.com/gentoo/dotnet/issues/6
    variant('patch-folder-path', default=False,
            description='Point SpecialFolder.CommonApplicationData folder '
            'into Spack installation instead of /usr/share')

    # Spack's openssl interacts badly with mono's vendored
    # "boringssl", don't drag it in w/ cmake
    depends_on('cmake~openssl', type=('build'))
    depends_on('libiconv')
    depends_on('perl', type=('build'))

    version('5.18.0.240', sha256='143e80eb00519ff496742e78ee07403a3c3629437f3a498eee539de8108da895')
    version('5.16.0.220', sha256='f420867232b426c062fa182256a66b29efa92992c119847359cdd1ab75af8de3')
    version('5.14.0.177', sha256='d4f5fa2e8188d66fbc8054f4145711e45c1faa6d070e63600efab93d1d189498')
    version('5.12.0.309', sha256='7c4738c91187bfcea7b40f9e7a4bf3a0e4f54fdc0f4472612f84803e8bed368f')
    version('5.10.1.57',  sha256='76cbd8545db6adc5a1738c343d957a7015c95e1439c461ea4f2bd56bd6337ab4')
    version('5.4.1.7', '28a82df5d0b7854b387d4f21d852ac70')
    version('5.4.0.167', '103c7a737632046a9e9a0b039d752ee1')
    version('5.0.1.1', '17692c7a797f95ee6f9a0987fda3d486')
    version('4.8.0.524', 'baeed5b8139a85ad7e291d402a4bcccb')

    def patch(self):
        if '+patch-folder-path' in self.spec:
            before = 'return "/usr/share";'
            after = 'return "{0}";'.format(self.prefix.share)
            f = 'mcs/class/corlib/System/Environment.cs'
            kwargs = {'ignore_absent': False, 'backup': True, 'string': True}
            filter_file(before, after, f, **kwargs)

    def configure_args(self):
        args = []
        li = self.spec['libiconv'].prefix
        args.append('--with-libiconv-prefix={p}'.format(p=li))
        return args
