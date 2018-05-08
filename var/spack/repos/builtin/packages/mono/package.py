###############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
