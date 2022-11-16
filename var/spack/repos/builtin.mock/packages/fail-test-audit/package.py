# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.makefile
from spack.package import *


class FailTestAudit(MakefilePackage):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0", "0123456789abcdef0123456789abcdef")
    version("2.0", "abcdef0123456789abcdef0123456789")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):

    build_time_test_callbacks = ["test"]

    def test(self):
        print("test: test-install-callbacks")
        print("PASSED")
