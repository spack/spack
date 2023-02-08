# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chemfiles(CMakePackage):
    """Chemfiles is a library providing a simple and format agnostic interface for
    reading and writing computational chemistry files: trajectories, configurations,
    and topologies."""

    homepage = "https://chemfiles.org"
    url = "https://github.com/chemfiles/chemfiles/archive/refs/tags/0.10.2.tar.gz"

    maintainers("RMeli")

    version("0.10.3", sha256="5f53d87a668a85bebf04e0e8ace0f1db984573de1c54891ba7d37d31cced0408")
    version("0.10.2", sha256="2e3b58167f25d561ab19ae06acdc02f26b5640bd6c85e0a5b10fedfec59f5285")
    version("0.10.1", sha256="a1bbc26d8e8c33f52a157df4aece0c07e126a986f29231c4fdcb9a55292dc5b0")
    version("0.10.0", sha256="521e7b3a4fe007ffca198b276e5c40a0ae4f2824050e29ccf32ef91dce21b102")

    variant("shared", default=False, description="Build shared libraries")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        return args
