# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LuaLpeg(LuaPackage):
    """pattern-matching for lua"""

    homepage = "http://www.inf.puc-rio.br/~roberto/lpeg/"
    url      = "http://www.inf.puc-rio.br/~roberto/lpeg/lpeg-1.0.2.tar.gz"

    version('1.0.2', sha256='48d66576051b6c78388faad09b70493093264588fcd0f258ddaab1cdd4a15ffe')

    depends_on("lua@:5.1.9", when="@:0.12.1^lua")