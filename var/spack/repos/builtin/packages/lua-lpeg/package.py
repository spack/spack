# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LuaLpeg(Package):
    """pattern-matching for lua"""

    homepage = "http://www.inf.puc-rio.br/~roberto/lpeg/"
    url      = "https://luarocks.org/manifests/luarocks/lpeg-0.12-1.src.rock"

    version('0.12-1', sha256='3962e8d695d0f9095c9453f2a42f9f1a89fb94db9b0c3bf22934c1e8a3b0ef5a',
            expand=False)

    extends("lua")

    def install(self, spec, prefix):
        luarocks('--tree=' + prefix, 'install', 'lpeg-0.12-1.src.rock')
