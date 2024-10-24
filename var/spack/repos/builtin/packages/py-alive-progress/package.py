# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAliveProgress(PythonPackage):
    """A new kind of Progress Bar, with real-time
    throughput, ETA, and very cool animations!"""

    homepage = "https://github.com/rsalmei/alive-progress"
    pypi = "alive-progress/alive-progress-2.4.1.tar.gz"

    license("MIT")

    version("2.4.1", sha256="089757c8197f27ad972ba27e1060f6db92368d83c736884e159034fd74865323")
    version("1.6.2", sha256="642e1ce98becf226c8c36bf24e10221085998c5465a357a66fb83b7dc618b43e")

    depends_on("python@2.7:3", type=("build", "run"))
    depends_on("python@3.6:3", type=("build", "run"), when="@2:")
    depends_on("python@3.7:3", type=("build", "run"), when="@2.2:")
    depends_on("py-setuptools", type="build")
    depends_on("py-about-time@3.1.1", type=("build", "run"), when="@2.4.1:")
    depends_on("py-grapheme@0.6.0", type=("build", "run"), when="@2.4.1:")
