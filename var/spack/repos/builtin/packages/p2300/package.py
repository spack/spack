# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class P2300(CMakePackage):
    """The proposed C++ framework for asynchronous and parallel programming."""

    homepage = "https://github.com/brycelelbach/wg21_p2300_std_execution"
    git = "https://github.com/brycelelbach/wg21_p2300_std_execution.git"
    maintainers = ["msimberg", "aurianer"]

    version("main", branch="main")

    depends_on("cmake@3.22.1:", type="build")

    conflicts("%gcc@:10")
    conflicts("%clang@:13")
