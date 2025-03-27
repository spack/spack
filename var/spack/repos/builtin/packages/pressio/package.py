# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from os.path import join as pjoin

from spack.package import *


class Pressio(Package):
    """
    Pressio is an ecosystem for developing, applying and
    using projection-based model reduction (pROM) methods.
    A key goal is to mitigate the intrusive nature of pROMs
    for large-scale codes, and providing a framework to
    foster research of new ideas as well as incentivize broader
    adoption and usability.
    """

    homepage = "https://pressio.github.io/pressio/"
    git = "https://github.com/pressio/pressio.git"

    license("BSD-3-Clause")
    maintainers("fnrizzi", "cwschilly")

    version("main", branch="main")
    version("0.15.0", branch="v0.15.0")

    depends_on("pressio-ops@develop", type="build", when="@main")
    depends_on("pressio-log@main", type="build", when="@main")

    depends_on("pressio-ops@0.15.0", type="build", when="@0.15.0")
    depends_on("pressio-log@0.15.0", type="build", when="@0.15.0")

    def install(self, spec, prefix):
        include_dir = prefix.include
        install_tree("include", include_dir)

        # Add symlinks to pressio-ops headers inside main include/pressio directory
        pressio_include = pjoin(include_dir, "pressio")
        ops_include = pjoin(self.spec["pressio-ops"].prefix.include, "pressio")
        for item in os.listdir(ops_include):
            src_item = pjoin(ops_include, item)
            dest_item = pjoin(pressio_include, item)
            symlink(src_item, dest_item, target_is_directory=os.path.isdir(src_item))

        # Add symlink to pressio-log headers in include/pressio-log
        log_include = pjoin(self.spec["pressio-log"].prefix.include, "pressio-log")
        symlink(log_include, pjoin(include_dir, "pressio-log"), target_is_directory=True)
