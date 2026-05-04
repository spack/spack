# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from urllib.request import pathname2url

from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class SimpleDownload(Package):
    """Test package to test a simple package install using a 
    basic URL fetcher
    """
    archive_name = "simple_download-0.1.tar.gz"
    url = "file:" + pathname2url(os.path.join(os.path.dirname(__file__), archive_name))


    version("0.1", sha256="825ff2bf662c7d662f1c4632324b615a7da56ed3c0c624d9a31d1d718fcae648")

    def install(self, prefix, spec):
        touch(prefix.test)
        copy(os.path.join(self.stage.source_path, "hello"), prefix)

    def test_basic(self):
        assert os.path.exists(self.prefix.test)
        assert os.path.exists(self.prefix.hello)
        with open(self.prefix.hello, "r", encoding="utf-8") as f:
            assert f.read() == "world"
