# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtQuick3d(QtPackage):
    """A new module and API for defining 3D content in Qt Quick."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    version("6.4.2", sha256="940145615fe3c4c8fb346c5bfc10f94fc7a4005c8c187886e0f3088ea0ce0778")
    version("6.4.1", sha256="67daeed69b9e7b3da516c6205e737fdba30a267978c1fb9d34723a6dc5588585")
    version("6.4.0", sha256="37987536da151b7c2cddabfde734759ebe6173708d32cb85aa008e151751270e")
    version("6.3.2", sha256="a3ec81393f1cd45eb18ee3d47582998679eef141b856bdd2baa2d41f019a0eea")
    version("6.3.1", sha256="79f0813ff776dc2aa07a8513ecd9d550dd8d449dc8fcd834fb0c9b22ea4a1893")
    version("6.3.0", sha256="413dec87828155ea0c0424e6b40c777bf0710f1ffaf98969c5d8b19ad3992823")
    version("6.2.4", sha256="7292ed4373a92913c6811f2faa5191f0426f84bd93a3f6eb7d54b62626b56db5")
    version("6.2.3", sha256="35d06edbdd83b7d781b70e0bada18911fa9b774b6403589d5b21813a73584d80")

    depends_on("assimp@5.0.1:")
    depends_on("embree", when="@6.4:")

    vendor_deps_to_remove = ["assimp", "embree"]

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-declarative@" + v, when="@" + v)
        depends_on("qt-quicktimeline@" + v, when="@" + v)

    def cmake_args(self):
        args = super().cmake_args() + [
            self.define("FEATURE_quick3d_assimp", True),
            self.define("FEATURE_system_assimp", True),
        ]
        return args
