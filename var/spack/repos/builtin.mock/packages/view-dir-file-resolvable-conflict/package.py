# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ViewDirFileResolvableConflict(Package):
    """Installs a symlink <prefix>/bin/x -> <dep>/bin/x (where x is a file). In a view we should
    find the dependency's file, not this package's symlink."""

    homepage = "http://www.spack.org"
    url = "http://www.spack.org/downloads/aml-1.0.tar.gz"
    has_code = False

    version("0.1.0")
    depends_on("view-dir-file")

    def install(self, spec, prefix):
        dep_prefix = spec["view-dir-file"].prefix
        os.mkdir(os.path.join(prefix, "bin"))
        os.symlink(os.path.join(dep_prefix, "bin", "x"), os.path.join(prefix, "bin", "x"))
