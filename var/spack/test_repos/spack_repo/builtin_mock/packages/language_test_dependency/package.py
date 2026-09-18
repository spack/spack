# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class LanguageTestDependency(Package):
    """Package needing a compiler only for its tests (e.g. a header-only library)"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/language-test-dependency-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("cxx", type="test")
