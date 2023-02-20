# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TrivialSmokeTest(Package):
    """This package is a stub with trivial smoke test features."""

    homepage = "http://www.example.com/trivial_test"
    url = "http://www.unit-test-should-replace-this-url/trivial_test-1.0.tar.gz"

    version("1.0", "0123456789abcdef0123456789abcdef")

    test_source_filename = "cached_file.in"

    def install(self, spec, prefix):
        pass

    @run_before("install")
    def create_extra_test_source(self):
        mkdirp(self.install_test_root)
        touch(join_path(self.install_test_root, self.test_source_filename))

    @run_after("install")
    def copy_test_sources(self):
        self.cache_extra_test_sources([self.test_source_filename])
