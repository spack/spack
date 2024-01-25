# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHumanize(PythonPackage):
    """This modest package contains various common humanization utilities, like
    turning a number into a fuzzy human readable duration ('3 minutes ago') or
    into a human readable size or throughput. It works with python 2.7 and 3.3
    and is localized to Russian, French, Korean and Slovak.
    """

    homepage = "https://github.com/python-humanize/humanize"
    pypi = "humanize/humanize-0.5.1.tar.gz"

    license("MIT")

    version("4.6.0", sha256="5f1f22bc65911eb1a6ffe7659bd6598e33dcfeeb904eb16ee1e705a09bf75916")
    version("4.4.0", sha256="efb2584565cc86b7ea87a977a15066de34cdedaf341b11c851cfcfd2b964779c")
    version("4.0.0", sha256="ee1f872fdfc7d2ef4a28d4f80ddde9f96d36955b5d6b0dac4bdeb99502bddb00")
    version("3.12.0", sha256="5ec1a66e230a3e31fb3f184aab9436ea13d4e37c168e0ffc345ae5bb57e58be6")
    version("0.5.1", sha256="a43f57115831ac7c70de098e6ac46ac13be00d69abbf60bdcac251344785bb19")

    depends_on("py-hatch-vcs", when="@4.6:", type=("build", "run"))
    depends_on("py-hatchling", when="@4.6:", type=("build", "run"))

    with when("@:4.4"):
        depends_on("py-setuptools@42:", when="@3.2:", type=("build", "run"))
        depends_on("py-setuptools", type="build")
        depends_on("py-setuptools-scm+toml@3.4:", when="@3.2:", type="build")
        depends_on("py-setuptools-scm", when="@1:", type="build")

    depends_on("py-importlib-metadata", when="@3.12: ^python@:3.7", type=("build", "run"))
