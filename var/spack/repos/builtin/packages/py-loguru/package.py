# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLoguru(PythonPackage):
    """Loguru is a library which aims to bring enjoyable logging in Python."""

    homepage = "https://github.com/Delgan/loguru"
    pypi = "loguru/loguru-0.6.0.tar.gz"

    license("MIT")

    version(
        "0.6.0",
        sha256="4e2414d534a2ab57573365b3e6d0234dfb1d84b68b7f3b948e6fb743860a77c3",
        url="https://pypi.org/packages/fe/21/e1d1da2586865a159fc73b611f36bdd50b6c4043cb6132d3d5e972988028/loguru-0.6.0-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="85408b9552adb9a795af102221c7517f35c8b56ffe7b43d98d37e883283854de",
        url="https://pypi.org/packages/4a/59/9deeeba62ecfcb771c0e76d63fab565e2c229e1e418d0c410d9313fa7a4c/loguru-0.3.0-py3-none-any.whl",
    )
    version(
        "0.2.5",
        sha256="ebac59630946721fd6207264679b267a8bdc290b086226067d6aad86830e3123",
        url="https://pypi.org/packages/c4/2d/2861600f1abed3c85e157c78308d3b1de974ad64d67de852a79da9ae7205/loguru-0.2.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ansimarkup@1.4:", when="@:0.2")
        depends_on("py-better-exceptions-fork@0.2.1.post6:", when="@:0.2")
        depends_on("py-colorama@0.3.4:", when="@0.3: platform=windows")
        depends_on("py-colorama@0.3.4:", when="@0.2.3:0.2")
        depends_on("py-win32-setctime", when="@0.3: platform=windows")

    # Missing dependency required for windows
    # depends_on('py-win32-setctime@1.0.0:',
    #            when='platform=windows',
    #            type=('build', 'run'))
    conflicts("platform=windows")
