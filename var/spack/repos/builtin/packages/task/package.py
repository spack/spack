# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Task(CMakePackage):
    """Feature-rich console based todo list manager"""

    homepage = "https://www.taskwarrior.org"
    url = "https://taskwarrior.org/download/task-2.4.4.tar.gz"

    license("MIT")

    version("2.6.2", sha256="b1d3a7f000cd0fd60640670064e0e001613c9e1cb2242b9b3a9066c78862cfec")
    version("2.5.1", sha256="d87bcee58106eb8a79b850e9abc153d98b79e00d50eade0d63917154984f2a15")
    version("2.4.4", sha256="7ff406414e0be480f91981831507ac255297aab33d8246f98dbfd2b1b2df8e3b")

    depends_on("cmake@2.8:", type="build")
    depends_on("gnutls")
    depends_on("uuid")

    conflicts("%gcc@:4.7")
