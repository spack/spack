# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libglvnd(MesonPackage):
    """libglvnd is a vendor-neutral dispatch layer for arbitrating OpenGL API calls
    between multiple vendors."""

    homepage = "https://gitlab.freedesktop.org/glvnd/libglvnd"
    url = "https://gitlab.freedesktop.org/glvnd/libglvnd/-/archive/v1.7.0/libglvnd-v1.7.0.tar.gz"

    maintainers("snehring")

    license(
        """MIT-feh AND MIT-Modern-Variant AND BSD-1-Clause AND BSD-3-Clause
           AND GPL-3.0-or-later WITH Autoconf-exception-macro""",
        checked_by="snehring",
    )

    version("1.7.0", sha256="2b6e15b06aafb4c0b6e2348124808cbd9b291c647299eaaba2e3202f51ff2f3d")
    version("1.6.0", sha256="efc756ffd24b24059e1c53677a9d57b4b237b00a01c54a6f1611e1e51661d70c")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("libxext")
    depends_on("libx11")
    depends_on("xorgproto")

    provides("egl")
    provides("gl")
