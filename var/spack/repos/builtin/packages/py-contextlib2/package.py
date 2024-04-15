# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyContextlib2(PythonPackage):
    """contextlib2 is a backport of the standard library's contextlib module to
    earlier Python versions."""

    homepage = "https://contextlib2.readthedocs.io/en/stable/"
    pypi = "contextlib2/contextlib2-21.6.0.tar.gz"

    license("PSF-2.0")

    version(
        "21.6.0",
        sha256="3fbdb64466afd23abaf6c977627b75b6139a5a3e8ce38405c5b413aed7a0471f",
        url="https://pypi.org/packages/76/56/6d6872f79d14c0cb02f1646cbb4592eef935857c0951a105874b7b62a0c3/contextlib2-21.6.0-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="9d2c67f18c1f9b6db1b46317f7f784aa82789d2ee5dea5d9c0f0f2a764eb862e",
        url="https://pypi.org/packages/cf/e5/989798d38831a8505d62687c94b0f2954ff0a40782e25f9add8ed675dc1f/contextlib2-0.6.0-py2.py3-none-any.whl",
    )
    version(
        "0.5.5",
        sha256="f5260a6e679d2ff42ec91ec5252f4eeffdcf21053db9113bd0a8e4d953769c00",
        url="https://pypi.org/packages/a2/71/8273a7eeed0aff6a854237ab5453bc9aa67deb49df4832801c21f0ff3782/contextlib2-0.5.5-py2.py3-none-any.whl",
    )
