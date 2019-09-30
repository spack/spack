# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LuaLuv(Package):
    """pattern-matching for lua"""

    homepage = "https://luarocks.org/manifests/creationix"
    url      = "https://luarocks.org/manifests/creationix/luv-1.30.1-1.src.rock"
    version('1.30.1', '3d9a65d9e18ab0413bdc81f5a9508a5d',
            url='https://luarocks.org/manifests/creationix/luv-1.30.1-1.src.rock',
            expand=False)

    extends("lua")

    depends_on("cmake")

    def install(self, spec, prefix):
        luarocks('--tree=' + prefix, 'install', 'luv-1.30.1-1.src.rock')
