# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

    license("BSD-3-Clause")

    version(
        "2.0.10",
        sha256="e10a1f1a6a2dcfbf23155913746ff6fbf8ea18c5ee813b6d0e79d273bb2b3c18",
        url="https://pypi.org/packages/e9/33/cbff7525a357c950e76717ea9741127a662a7ed49a92874897b8a4036db9/pyglet-2.0.10-py3-none-any.whl",
    )
    version(
        "2.0.9",
        sha256="8520b22dde75f47167e1fedeed58ac0bb0c890c0dca17d8528427d6b318cd9cc",
        url="https://pypi.org/packages/94/a1/475458ccf34d2996abdb6ef29fa8d3fed2e62f72df5f2a7f4b4b076915c7/pyglet-2.0.9-py3-none-any.whl",
    )
    version(
        "1.4.2",
        sha256="c1c49b2c384bc310aa3dca87817d2b4d22383e35776e73dace5a38235f0992a4",
        url="https://pypi.org/packages/d4/eb/e3742cc05eb640b6b59618ad8c8ae38f43aa57539e4cd1b40576c93afccb/pyglet-1.4.2-py2.py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="91a49322e5ef17aed704a2622cb7f66793b9519ce9ec8af45284eb9cab7d93ea",
        url="https://pypi.org/packages/4f/2a/52827e866bc2ebe0f67d83d0c49fcd2ceecd58245d9e79b69df0919e740b/pyglet-1.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-future", when="@1.3:1.5.0")
