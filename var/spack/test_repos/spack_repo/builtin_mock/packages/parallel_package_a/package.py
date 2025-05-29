# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import time

from spack_repo.builtin_mock.build_systems.generic import Package

from llnl.util.filesystem import touch

from spack.package import *


class ParallelPackageA(Package):
    """Simple package with dependencies for testing parallel builds"""

    homepage = "http://www.example.com"
    has_code = False

    depends_on("parallel-package-b")
    depends_on("parallel-package-c")

    version("1.0")

    def install(self, spec, prefix):
        time.sleep(2)
        touch(prefix.dummy_file)
