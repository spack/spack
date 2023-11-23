# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyglet(PythonPackage):
    """pyglet is a cross-platform windowing and multimedia library for Python
    for developing games and other visually rich applications.
    """

    homepage = "https://github.com/pyglet/pyglet"
    pypi = "pyglet/pyglet-2.0.9.zip"

    version("2.0.10", sha256="457cc703bf0a29530cb5e6289bab58402565dda5e3a1845a8c9ba266f052eb75")
    version("2.0.9", sha256="74ac223a0d67294541dc5314e3a14b982dc056664989a1e21eca98985329ef56")
    version("1.4.2", sha256="fda25ae5e99057f05bd339ea7972196d2f44e6fe8fb210951ab01f6609cdbdb7")
    version("1.2.1", sha256="d1afb253d6de230e73698377566da333ef42e1c82190216aa7a0c1b729d6ff4d")

    depends_on("py-setuptools", type="build")
    depends_on("py-future", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"), when="@:1")
    depends_on("python@3.8:", type=("build", "run"), when="@2.0:")
    depends_on("gl", type=("build", "run"), when="@2.0: platform=linux")
    depends_on("glx", type=("build", "run"), when="@2.0: platform=linux")
    depends_on("pil", type=("build", "run"), when="@2.0: platform=linux")
    depends_on("pulseaudio", type=("build", "run"), when="@2.0: platform=linux")

    def url_for_version(self, version):
        if version <= Version("1.4.2"):
            return (
                f"https://files.pythonhosted.org/packages/source/p/pyglet/pyglet-{version}.tar.gz"
            )
        # 2.0.9 and 2.0.10 had an issue with their PyPI zipfile
        # Should be solved for the next version.
        # See https://github.com/pyglet/pyglet/issues/999
        elif version in [Version("2.0.9"), Version("2.0.10")]:
            return f"https://github.com/pyglet/pyglet/archive/refs/tags/v{version.dotted}.zip"
