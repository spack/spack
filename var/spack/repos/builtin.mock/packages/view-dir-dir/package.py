# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ViewDirDir(Package):
    """Installs a <prefix>/bin/x where x is a dir, in contrast to view-dir-file."""

    homepage = "http://www.spack.org"
    url = "http://www.spack.org/downloads/aml-1.0.tar.gz"
    has_code = False

    version("0.1.0")

    def install(self, spec, prefix):
        os.mkdir(os.path.join(prefix, "bin"))
        os.mkdir(os.path.join(prefix, "bin", "x"))
        with open(os.path.join(prefix, "bin", "x", "file_in_dir"), "wb") as f:
            f.write(b"hello world")
