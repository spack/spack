# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class LuaLuajit(Package):
    """Flast flexible JITed lua"""
    homepage = "http://www.luajit.org"
    url      = "http://luajit.org/download/LuaJIT-2.0.4.tar.gz"

    version('2.0.4', sha256='620fa4eb12375021bef6e4f237cbd2dd5d49e56beb414bee052c746beef1807d')

    def install(self, spec, prefix):
        # Linking with the C++ compiler is a dirty hack to deal with the fact
        # that unwinding symbols are not included by libc, this is necessary
        # on some platforms for the final link stage to work
        make("install", "PREFIX=" + prefix, "TARGET_LD=" + os.environ['CXX'])
