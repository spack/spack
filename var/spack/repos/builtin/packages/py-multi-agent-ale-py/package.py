# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMultiAgentAlePy(PythonPackage):
    """The Multi-Agent Arcade Learning Environment"""

    homepage = "https://github.com/Farama-Foundation/Multi-Agent-ALE"
    pypi = "multi-agent-ale-py/multi-agent-ale-py-0.1.11.tar.gz"

    license("GPL 2.0", checked_by="ashim-mahara ")

    version("0.1.11", sha256="ba3ff800420f65ff354574975bdfa79035ae1597e8938b37d1df12ffc4122edb")
    version("0.1.10", sha256="67c1c76744adb6c3ccc3a5091cc567e4abfd87d3dc163637a999e95a74e5d659")
    version("0.1.9", sha256="ec706297895d1f09e531720e3a1c9ae52d7e331239d6314520f4c54e73839089")
    version("0.1.8", sha256="7551195119ac2780cd21bfa2e7fa8dafba208c1268cd013e715d158447ac3cb1")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-wheel", type="build")
    depends_on("cmake@3.14:", type="build")
    depends_on("ninja", type="build")
