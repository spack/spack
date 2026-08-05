# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *
from spack.util.filesystem import touch


class ParallelPackageB(Package):
    """Simple dependency package for testing parallel builds"""

    homepage = "http://www.example.com"
    has_code = False

    version("1.0")

    def install(self, spec, prefix):
        touch(prefix.dummy_file)
