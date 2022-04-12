# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLibclang(PythonPackage):
    """The repository contains code that taken from the LLVM project, to make
    it easier to install clang's python bindings."""

    homepage = "https://github.com/sighingnow/libclang"

    url = "https://github.com/sighingnow/libclang/archive/refs/tags/llvm-11.1.0.tar.gz"

    version(
        "11.1.0",
        sha256="0b53b3c237725e193c4d2bbbe096f1a1da0f0e5cd528f2892e4dfed3c8fe9506",
    )
    version(
        "11.0.1",
        sha256="739ae984a4a4043ae4d3b4db74597a36a8e46b6f0cbd139c7d2703faf40c5390",
    )
    version(
        "11.0.0",
        sha256="aec204414ea412e4d4e041b0bf48123881338ac723bbcfa948f2a1b92a2428b5",
    )
    version(
        "10.0.1",
        sha256="c15d8f97c4d0f3d4501e8b2625b343569fd92690afebe6260a2c64463d713995",
    )
    version(
        "9.0.1",
        sha256="fc84e7bf3b0eb4f11c496d6603f111e3d8cda97094d6c9c512361371f1b76f1c",
    )

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    for ver in ["9", "10", "11"]:
        depends_on("llvm+clang@" + ver, when="@" + ver, type="build")

    def patch(self):
        filter_file(
            "source_dir = './native/'",
            "source_dir = '{0}'".format(self.spec["llvm"].libs.directories[0]),
            "setup.py", string=True,
        )
