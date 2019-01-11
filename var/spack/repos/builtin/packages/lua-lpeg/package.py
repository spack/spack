# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LuaLpeg(Package):
    """pattern-matching for lua"""

    homepage = "http://www.inf.puc-rio.br/~roberto/lpeg/"
    url      = "https://luarocks.org/manifests/luarocks/lpeg-0.12-1.src.rock"

    version('0.12.1', 'b5778bfee67761fcbe7a2d23cb889ea8',
            url='https://luarocks.org/manifests/luarocks/lpeg-0.12-1.src.rock',
            expand=False)

    extends("lua")

    def install(self, spec, prefix):
        luarocks('--tree=' + prefix, 'install', 'lpeg-0.12-1.src.rock')
