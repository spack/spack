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

    version(
        "2.4.1",
        sha256="5503ffca0a0607d5f0d24d3b10a718fe50e375470fa07602b246333eb7ec88ee",
        url="https://pypi.org/packages/e4/01/7a6bcf3eb3fb030fac47854a984dcc488304af15721df33ce827f25158d1/alive_progress-2.4.1-py3-none-any.whl",
    )
    version(
        "1.6.2",
        sha256="0f1111f56b1b870f5e5edd57e89fc97dc1ca0a73eb5c5a09533494c7e850a818",
        url="https://pypi.org/packages/cc/5c/d63b13cc0bd945b4a9b16e921cc00c5657143f68da4f296bb628b8d1ff17/alive_progress-1.6.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@2.2:")
        depends_on("python@:3", when="@:2.1")
        depends_on("py-about-time@3.1.1:3.1", when="@2")
        depends_on("py-grapheme@0.6:", when="@2:")
