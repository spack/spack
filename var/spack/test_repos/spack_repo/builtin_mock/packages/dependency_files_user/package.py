# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class DependencyFilesUser(Package):
    """Package detected by its executable, whose recipe returns the files of its dependencies"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dependency-files-user-1.0.tar.gz"

    executables = ["^dependency-files-user$"]

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("tool", default=True, description="Run dependency-files-tool")

    depends_on("dependency-files-tool", type=("build", "run"), when="+tool")
    depends_on("dependency-files-tool", type="build", when="~tool")
    depends_on("sonames-owner", type="link")

    @classmethod
    def determine_version(cls, exe):
        return "1.0"

    @classmethod
    def determine_dependency_files(cls, spec):
        # The files are listed in the prefix, as MPI wrappers list the compiler they run
        path = os.path.join(spec.external_path, "share", "dependency-files")
        with open(path, encoding="utf-8") as f:
            return f.read().split()
