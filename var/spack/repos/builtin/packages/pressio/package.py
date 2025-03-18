# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    depends_on("pressio-ops", type="build")
    depends_on("pressio-log", type="build")

    def install(self, spec, prefix):
        include_dir = prefix.include
        install_tree("include", include_dir)

        # Move pressio-ops and pressio-log headers inside of main include dir
        install_tree(self.spec["pressio-ops"].prefix.include, include_dir)
        install_tree(self.spec["pressio-log"].prefix.include, include_dir)
