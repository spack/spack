# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcrypt(AutotoolsPackage):
    """libxcrypt is a modern library for one-way hashing of passwords."""

    homepage = "https://github.com/besser82/libxcrypt"
    url = "https://github.com/besser82/libxcrypt/releases/download/v4.4.30/libxcrypt-4.4.30.tar.xz"
    maintainers("haampie")

    def url_for_version(self, version):
        if version <= Version("4.4.17"):
            return "https://github.com/besser82/libxcrypt/archive/v{}.tar.gz".format(version)
        return "https://github.com/besser82/libxcrypt/releases/download/v{}/libxcrypt-{}.tar.xz".format(
            version, version
        )

    version("4.4.33", sha256="e87acf9c652c573a4713d5582159f98f305d56ed5f754ce64f57d4194d6b3a6f")
    version("4.4.32", sha256="0613f9bd51d713f8bb79fa10705b68d2ab705c3be4c4fc119f0a96bdc72256c4")
    version("4.4.31", sha256="c0181b6a8eea83850cfe7783119bf71fddbde69adddda1d15747ba433d5c57ba")
    version("4.4.30", sha256="b3667f0ba85daad6af246ba4090fbe53163ad93c8b6a2a1257d22a78bb7ceeba")
    version("4.4.17", sha256="7665168d0409574a03f7b484682e68334764c29c21ca5df438955a381384ca07")
    version("4.4.16", sha256="a98f65b8baffa2b5ba68ee53c10c0a328166ef4116bce3baece190c8ce01f375")
    version("4.4.15", sha256="8bcdef03bc65f9dbda742e56820435b6f13eea59fb903765141c6467f4655e5a")

    variant("obsolete_api", default=False, when="@4.4.30:")

    patch("truncating-conversion.patch", when="@4.4.30")

    with when("@:4.4.17"):
        depends_on("autoconf", type="build")
        depends_on("automake@1.14:", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")

    # Some distros have incomplete perl installs, +open catches that.
    depends_on("perl@5.14.0: +open", type="build", when="@4.4.18:")

    def configure_args(self):
        args = [
            # Disable test dependency on Python (Python itself depends on libxcrypt).
            "ac_cv_path_python3_passlib=not found",
            # Disable -Werror, which breaks with newer compilers
            "--disable-werror",
        ]
        args += self.enable_or_disable("obsolete-api", variant="obsolete_api")
        return args

    @property
    def libs(self):
        return find_libraries("libcrypt", root=self.prefix, recursive=True)
