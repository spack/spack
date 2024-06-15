# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install novnc
#
# You can edit this file again by typing:
#
#     spack edit novnc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Novnc(Package):
    """Open source VNC client written in JavaScript"""

    homepage = "https://novnc.com/info.html"
    url = "https://github.com/novnc/noVNC/archive/refs/tags/v1.4.0.tar.gz"

    maintainers("teaguesterling")

    license("MPL", checked_by="teaguesterling")

    version("1.4.0", sha256="89b0354c94ad0b0c88092ec7a08e28086d3ed572f13660bac28d5470faaae9c1")
    version("1.3.0", sha256="ee8f91514c9ce9f4054d132f5f97167ee87d9faa6630379267e569d789290336")
    version("1.2.0", sha256="36c476b26df4684f1002e15c3d7e034c9e6ee4521e5fa8aac37309f954a07a01")
    version("1.1.0", sha256="2c63418b624a221a28cac7b9a7efecc092b695fc1b7dd88255b074ab32bc72a7")
    version("1.0.0", sha256="58aced9ec76c9d9685b771ed94472b7cedafa2810584e85afaedbcb0b02b8aae")

    variant("index", default=False, description="Rename vnc.html to index.html")
    variant("install_root", 
        default="srv/www",
        description="Where to place the static novnc files",
        values=[
            "srv/www",
            "var/www",
            "usr/share",
            "usr/local/var",
        ],
    )
    variant("nginx", default=False, description="Write nginx configuration files")
    variant("apache", default=False, description="Write apache configuration files")

    @property
    def html_dir(self):
        print(self.spec.variants)
        install_root = f"{self.spec.variants['install_root'].value}"
        return join_path(install_root, self.name)

    def install(self, spec, prefix):
        base = join_path(prefix, self.html_dir)
        mkdirp(base)
        filename = "vnc.html" if spec.satisfies("~index") else "index.html"
        install("vnc.html", join_path(base, filename))
        for res in ["app", "core", "vendor"]:
            install_tree(res, join_path(base, res))

