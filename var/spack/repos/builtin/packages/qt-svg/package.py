# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtSvg(QtPackage):
    """Scalable Vector Graphics (SVG) is an XML-based language for describing
    two-dimensional vector graphics. Qt provides classes for rendering and
    displaying SVG drawings in widgets and on other paint devices."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    version("6.6.1", sha256="b947acd83ac51116f29c7f7278d9faed19b8c11e021dbf08616e7d6200118db8")
    version("6.6.0", sha256="4fd6b4d9307c3cd8fd207e60334823fed07a9acb32f7d53cd9c9be9b6a2f8a30")
    version("6.5.3", sha256="fb8e5574c2480aab78062fad2d0a521633b4591ada600130b918b703c2ddb09a")
    version("6.5.2", sha256="2d0c8780f164472ad968bb4eff325a86b2826f101efedbeca5662acdc0b294ba")
    version("6.5.1", sha256="1b262f860c51bc5af5034d88e74bb5584ecdc661f4903c9ba27c8edad14fc403")
    version("6.5.0", sha256="2f96e22858de18de02b05eb6bcc96fadb6d77f4dadd407e1fa4aebcceb6dd154")
    version("6.4.3", sha256="3cc7479f7787a19e7af8923547dfc35b7b3fd658e3701577e76b2c1e4c1c0c23")
    version("6.4.2", sha256="2f5fa08dbe6f3aea0c1c77acb74b6164dc069e15010103377186902b018fb623")
    version("6.4.1", sha256="be6300292a6f38d85c13bb750890af268bd979fb18ab754f88d5332935215e47")
    version("6.4.0", sha256="375eb69f320121e42d5dc107f9455008980c149646931b8ace19e6bc235dcd80")
    version("6.3.2", sha256="781055bca458be46ef69f2fff147a00226e41f3a23d02c91238b0328a7156518")

    variant("widgets", default=False, description="Build SVG widgets.")

    depends_on("qt-base +gui")
    depends_on("qt-base +widgets", when="+widgets")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)

    def cmake_args(self):
        args = super().cmake_args() + []
        return args

    def setup_run_environment(self, env):
        # to make plugins from SVG module to base, for e.g. icon loading
        env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)
