# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qca(CMakePackage):
    """Taking a hint from the similarly-named Java Cryptography Architecture,
       QCA aims to provide a straightforward and cross-platform crypto API,
       using Qt datatypes and conventions. QCA separates the API from the
       implementation, using plugins known as Providers. The advantage of
       this model is to allow applications to avoid linking to or explicitly
       depending on any particular cryptographic library. This allows one to
       easily change or upgrade crypto implementations without even needing
       to recompile the application!
       QCA should work everywhere Qt does, including Windows/Unix/MacOSX. """

    homepage = "https://userbase.kde.org/QCA"
    url      = "https://github.com/KDE/qca/archive/v2.1.3.tar.gz"

    version('2.2.1', sha256='c67fc0fa8ae6cb3d0ba0fbd8fca8ee8e4c5061b99f1fd685fd7d9800cef17f6b')
    version('2.1.3', 'bd646d08fdc1d9be63331a836ecd528f')

    depends_on('qt@4.2:')

    depends_on('qt@:5.10.0', when='@2.1.3')

    def cmake_args(self):
        args = []
        args.append('-DCMAKE_CXX_STANDARD=11')
        if self.spec['qt'].version.up_to(1) == Version(4):
            args.append('-DQT4_BUILD=ON')
        return args
