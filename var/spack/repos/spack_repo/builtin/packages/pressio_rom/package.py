# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from os.path import join as pjoin

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class PressioRom(Package):
    """
    Pressio is an ecosystem for developing, applying and
    using projection-based model reduction (pROM) methods.
    A key goal is to mitigate the intrusive nature of pROMs
    for large-scale codes, and providing a framework to
    foster research of new ideas as well as incentivize broader
    adoption and usability.
    """

    homepage = "https://pressio.github.io/pressio-rom/"
    git = "https://github.com/pressio/pressio-rom.git"

    license("BSD-3-Clause")
    maintainers("fnrizzi", "cwschilly")

    supported_versions = ["main", "0.15.0"]

    # For now, assume each repo is compatible only with the same version of the other repos
    for supported_version in supported_versions:
        version(supported_version, branch=supported_version)
        depends_on(f"pressio-ops@{supported_version}", type="build", when=f"@{supported_version}")
        depends_on(f"pressio-log@{supported_version}", type="build", when=f"@{supported_version}")

    def install(self, spec, prefix):
        include_dir = prefix.include
        install_tree("include", include_dir)

        # Add symlinks to pressio-ops headers inside main include/pressio directory
        pressio_includes = pjoin(include_dir, "pressio")
        ops_include = pjoin(self.spec["pressio-ops"].prefix.include, "pressio")
        for item in os.listdir(ops_include):
            src_item = pjoin(ops_include, item)
            dest_item = pjoin(pressio_includes, item)
            symlink(src_item, dest_item, target_is_directory=os.path.isdir(src_item))

        # Add symlink to pressio-log headers in include/pressio-log
        log_include = pjoin(self.spec["pressio-log"].prefix.include, "pressio-log")
        symlink(log_include, pjoin(include_dir, "pressio-log"), target_is_directory=True)
