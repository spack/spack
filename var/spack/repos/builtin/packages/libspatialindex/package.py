# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libspatialindex(CMakePackage):
    """C++ implementation of R*-tree, an MVR-tree and a TPR-tree with C API."""

    homepage = "https://libspatialindex.org/"
    url = "https://github.com/libspatialindex/libspatialindex/archive/refs/tags/1.8.5.tar.gz"

    license("MIT")

    version("2.1.0", sha256="a04513cea04dd20ab2c9d153c14cc45692805ee496b30619103f7929f6fb81bf")
    version("1.9.3", sha256="7b44340a3edc55c11abfc453bb60f148b29f569cef9e1148583e76132e9c7379")
    version("1.8.5", sha256="93cce77269612f45287b521d5afdfb245be2b93b8b6438d92f8b9e0bdb37059d")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.13:", when="@2:", type="build")
    depends_on("cmake@3.5:", type="build")

    @property
    def libs(self):
        return find_libraries(["libspatialindex_c"], root=self.prefix, recursive=True, shared=True)
