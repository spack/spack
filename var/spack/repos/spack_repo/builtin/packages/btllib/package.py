# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *


class Btllib(MesonPackage):
    """Bioinformatics Technology Lab common code library in C++
    with Python wrappers.
    """

    homepage = "https://github.com/bcgsc/btllib"
    url = "https://github.com/bcgsc/btllib/releases/download/v1.7.5/btllib-1.7.5.tar.gz"

    license("GPL-3.0-or-later")

    version("1.7.5", sha256="118a9f8d6445a618178bfbec40d121bbe03014e767261522148f642686090c76")
    version("1.7.4", sha256="8c046340b9db4d580521297bfd9cb55af6877a34b48cf6a053266703ebc17837")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("gettext")

    with default_args(type="build"):
        depends_on("cmake")
        depends_on("ninja")
        depends_on("python@3.9:")

    with default_args(type=("build", "run")):
        depends_on("samtools")
        depends_on("gzip")
        depends_on("xz")
        depends_on("bzip2")
        depends_on("tar")
        depends_on("wget")

    def meson_args(self):
        return ["-Db_ndebug=true", "-Db_coverage=false"]
