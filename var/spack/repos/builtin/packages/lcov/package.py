##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Lcov(MakefilePackage):
    """GCOV extension"""

    homepage = "https://github.com/linux-test-project/lcov"
    url      = "https://github.com/linux-test-project/lcov/archive/v1.13.tar.gz"

    version('1.13', sha256='3650ad22773c56aaf8c5288e068dd35bd03f57659b6455dc6f8e21451c83b5e8')

    depends_on('perl')

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
