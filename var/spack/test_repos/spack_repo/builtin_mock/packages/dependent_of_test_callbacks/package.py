# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DependentOfTestCallbacks(Package):
    """Package depending on test-build-callbacks, whose build-time tests fail. Used to check
    that --test=root does not run tests of dependencies, while --test=all does."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dependent-of-test-callbacks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("test-build-callbacks")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
