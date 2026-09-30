# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class PatchWhenDependency(Package):
    """Package with patches whose ``when=`` clause constrains a dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-when-dependency-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("c", type="build")
    depends_on("mpi")

    patch("fix.patch", when="%gcc@10:")
    patch("fix-mpi.patch", when="^mpi@2:")
