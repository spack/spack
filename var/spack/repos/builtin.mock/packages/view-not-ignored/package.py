# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class ViewNotIgnored(Package):
    """Install files that should not be ignored by spack."""

    homepage = "http://www.spack.org"
    url = "http://www.spack.org/downloads/aml-1.0.tar.gz"
    has_code = False

    version("0.1.0", sha256="cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b")

    install_test_files = [
        "foo.spack",
        ".spack.bar",
        "aspack",
        "bin/foo.spack",
        "bin/.spack.bar",
        "bin/aspack",
    ]

    def install(self, spec, prefix):
        for test_file in self.install_test_files:
            path = os.path.join(prefix, test_file)
            mkdirp(os.path.dirname(path))
            with open(path, "w") as f:
                f.write(test_file)

    @classmethod
    def assert_installed(cls, prefix):
        for test_file in cls.install_test_files:
            path = os.path.join(prefix, test_file)
            assert os.path.exists(path), "Missing installed file: {}".format(path)

    @classmethod
    def assert_not_installed(cls, prefix):
        for test_file in cls.install_test_files:
            path = os.path.join(prefix, test_file)
            assert not os.path.exists(path), "File was not uninstalled: {}".format(path)
