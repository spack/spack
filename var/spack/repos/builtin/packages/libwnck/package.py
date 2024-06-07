# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libwnck(AutotoolsPackage):
    """Window Navigator Construction Kit"""

    homepage = "https://gitlab.gnome.org/GNOME/libwnck"
    url = "https://download.gnome.org/sources/libwnck/3.4/libwnck-3.4.9.tar.xz"

    license("GPLv2", checked_by="teaguesterling")

    version("3.4.9", sha256="96e6353f2701a1ea565ece54d791a7bebef1832d96126f7377c54bb3516682c4")
    version("3.4.8", sha256="37ccf62a09d49ab6709c6515cf623a363140514db5d002da2a0e35b9e00e466a")
    version("3.4.7", sha256="d48ac9c7f50c0d563097f63d07bcc83744c7d92a1b4ef65e5faeab32b5ccb723")
    version("3.4.6", sha256="e3ae2d25b684910f49fc548dc96b8a54b77c431d94ad1fd5a37cbecab7bb1851")
    version("3.4.5", sha256="560f9709405fb33500c2f79efabdb1c4056866dec281f354ad3da97181fbf381")
    version("3.4.4", sha256="a545a23ea7681fafae033b4f68b69ef022d446a9325286291bb8882b9016a130")
    version("3.4.3", sha256="e468118927d50231df250d1f00106b32139aaad1ee9249a4ef316e5526d17d1d")
    version("3.4.2", sha256="1d055d0d7bd1069d97416985d11241eaea48aedb4311a22ff0d3404871707051")
    version("3.4.0", sha256="34a97edf601ee066204bb640b23f58d6897e0f559ce1816b3c1d206d70ea62ad")

    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("notification", default=True, description="Build with startup-notification support")
    variant("tools", default=True, description="Install WNCK tools")

    depends_on("intltool@0.40.6:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("gobject-introspection", when="+introspection")
        depends_on("startup-notification", when="+notification")

        depends_on("glib@2")
        depends_on("gdk-pixbuf")
        depends_on("gtkplus@3.22:")


    def configure_args(self):
        args = []

        args += self.enable_or_disable("introspection")
        args += self.enable_or_disable("tools")
        args += self.enable_or_disable("notification")

        return args
