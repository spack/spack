# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from llnl.util.symlink import symlink


class ViewDirSymlinkedDir(Package):
    """Installs <prefix>/bin/x/file_in_symlinked_dir where x -> y is a symlinked dir.
    This should be mergeable with view-dir-dir, but not with view-dir-file."""

    homepage = "http://www.spack.org"
    url = "http://www.spack.org/downloads/aml-1.0.tar.gz"
    has_code = False

    version("0.1.0", sha256="cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b")

    def install(self, spec, prefix):
        mkdirp(join_path(prefix, "bin"))
        mkdirp(join_path(prefix, "bin", "y"))
        with open(join_path(prefix, "bin", "y", "file_in_symlinked_dir"), "wb") as f:
            f.write(b"hello world")
        symlink("y", join_path(prefix, "bin", "x"))
