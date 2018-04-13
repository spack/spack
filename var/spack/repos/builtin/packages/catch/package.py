##############################################################################
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


class Catch(CMakePackage):
    """Catch tests"""

    homepage = "https://github.com/catchorg/Catch2"
    url = "https://github.com/catchorg/Catch2/archive/v1.3.0.tar.gz"

    variant('single_header', default=True,
            description='Install a single header only.')

    # - "make install" was added in 1.7.0
    # - pkg-config package was added in 2.0.1
    # - CMake config package was added in 2.1.2
    conflicts('~single_header', when='@:1.6.1')

    version('2.2.1', '54e56803c84890636bd7fe6c3856b104')
    version('2.1.0', '70b44068976d46d48f3cd8796f675691d3bc726b')
    version('2.0.1', '5c191a031edebd0525640ed2f38cbf64bacb1803')
    version('1.12.1', '7d89cffd9d61f4fdcbdb373b70cc92d1')
    version('1.12.0', '8fb0a64144a2c1572dd930254c7bbdf504ecbe2d')
    version('1.11.0', '3c03a022d8ba8dbbc931e1ce9fb28faec4890b8d')
    version('1.10.0', 'c2033ca00b616e7e703623c68220cf5a8e12bba4')
    version('1.9.7', '7ea41b48a23bd83f377f05a9dfde2be230cfc1b4')
    version('1.9.6', 'e6ae3a50c6e4da64410979dcd4b2bb3f7ba1c364')
    version('1.9.5', '7ba2bb12b5398b8b9ab7a7907f4cd345a55e179a')
    version('1.9.4', 'b48fce35161160def587bd0d8f0e95969b20b786')
    version('1.9.3', 'c0db82118496a2dd0637aad352f31d9356bffc28')
    version('1.9.2', '627fd94d466c0f71ba84010adf82771ed3ce85c7')
    version('1.9.1', '331e4a5cd32fe4c36b4bea15e5198346f18b5c3f')
    version('1.9.0', '5bb46e99eea39224189a8a0442ec7790c635a7b0')
    version('1.8.2', '34b8a2da76befeeaeafc393569538222605dda51')
    version('1.8.1', 'd5f4ae9603fe27c313bc5b5b23c233bdce5c57f7')
    version('1.8.0', '7fa6bfc50e6dbb6fd1352f41496650d56a86ac1a')
    version('1.7.2', '45b0ab04b6da75ce56de25a81f0b0de4c7a62179')
    version('1.7.1', '3a55985aacd5a5ff8a87c1490bbf65f0122647dc')
    version('1.7.0', '6f9869cc066721d525bb03e8a9423b806c362140')
    version('1.6.1', 'e88de5b611c07d5d402142d3dc20b63350fdf76c')
    version('1.6.0', '21273cbed050b8d4785231d04812d5addf5b71b7')
    version('1.5.9', '341bee0b642f0dc9bb6fb41243a068239468b703')
    version('1.5.0', '2d14342c72f12b3f4b975cf6aa8594c8ad43d773')
    version('1.4.0', '3b3b76a842508386be40d73849627bbe12fb5b7f')
    version('1.3.5', '2cfd78bce21368355c7d3880df88716084df2186')
    version('1.3.0', '24cd4e6518273fea20becd47a2e1edbee7ec209a')

    @when('+single_header')
    def cmake(self, spec, prefix):
        pass

    @when('+single_header')
    def build(self, spec, prefix):
        pass

    @when('+single_header')
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install(join_path('single_include', 'catch.hpp'), prefix.include)
        # fakes out spack so it installs a module file
        mkdirp(join_path(prefix, 'bin'))
