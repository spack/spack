# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class LuaJit(Package):
    """Flast flexible JITed lua"""
    homepage = "http://www.luajit.org"
    url      = "http://luajit.org/download/LuaJIT-2.0.4.tar.gz"

    version('2.0.4', 'dd9c38307f2223a504cbfb96e477eca0')

    def install(self, spec, prefix):
        # Linking with the C++ compiler is a dirty hack to deal with the fact
        # that unwinding symbols are not included by libc, this is necessary
        # on some platforms for the final link stage to work
        make("install", "PREFIX=" + prefix, "TARGET_LD=" + os.environ['CXX'])
