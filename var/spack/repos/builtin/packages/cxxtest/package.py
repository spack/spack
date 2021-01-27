# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
from spack import *


class Cxxtest(Package):
    """C++ unit test system."""

    homepage = "https://cxxtest.com/"
    url      = "https://sourceforge.net/projects/cxxtest/files/cxxtest/4.4/cxxtest-4.4.tar.gz/download"

    version('4.4', sha256='1c154fef91c65dbf1cd4519af7ade70a61d85a923b6e0c0b007dc7f4895cf7d8')

    def install(self, spec, prefix):
        for path in os.listdir(os.getcwd()):
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(prefix, path))
            else:
                shutil.copy(path, os.path.join(prefix, path))
