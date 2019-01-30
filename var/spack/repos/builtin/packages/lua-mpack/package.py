# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LuaMpack(Package):
    """lua bindings to libmpack"""

    homepage = "https://luarocks.org/modules/tarruda/mpack"
    url      = "https://luarocks.org/manifests/tarruda/mpack-1.0.6-0.src.rock"

    depends_on('msgpack-c')

    version('1.0.0-0', '9a7bd842753194124830bc7426e78c1b',
            url='https://luarocks.org/manifests/tarruda/mpack-1.0.6-0.src.rock',
            expand=False)

    extends('lua')

    def install(self, spec, prefix):
        luarocks('--tree=' + prefix, 'install', 'mpack-1.0.6-0.src.rock')
