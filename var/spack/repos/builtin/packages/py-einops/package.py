# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEinops(PythonPackage):
    """Flexible and powerful tensor operations for readable and reliable code.

    Supports numpy, pytorch, tensorflow, and others."""

    homepage = "https://github.com/arogozhnikov/einops"
    pypi = "einops/einops-0.3.2.tar.gz"

    license("MIT")

    version(
        "0.7.0",
        sha256="0f3096f26b914f465f6ff3c66f5478f9a5e380bb367ffc6493a68143fbbf1fd1",
        url="https://pypi.org/packages/29/0b/2d1c0ebfd092e25935b86509a9a817159212d82aa43d7fb07eca4eeff2c2/einops-0.7.0-py3-none-any.whl",
    )
    version(
        "0.6.1",
        sha256="99149e46cc808956b174932fe563d920db4d6e5dadb8c6ecdaa7483b7ef7cfc3",
        url="https://pypi.org/packages/68/24/b05452c986e8eff11f47e123a40798ae693f2fa1ed2f9546094997d2f6be/einops-0.6.1-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="c7b187a5dc725f079860ec2d330c1820448948622d826273345a8dd8d5f695bd",
        url="https://pypi.org/packages/4b/f7/8557c683501eb14462b60e32d21fc51317ab2ba39688db1b8b7cebe1a274/einops-0.6.0-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="055de7eeb3cb9e9710ef3085a811090c6b52e809b7044e8785824ed185f486d1",
        url="https://pypi.org/packages/18/d7/ed1ce1d5e00b0cd0e1ca46a710eb00822add013048c733d5b82db490e643/einops-0.5.0-py3-none-any.whl",
    )
    version(
        "0.3.2",
        sha256="285f3c75620897acb8b5580170c88121f010c77ce130bc7b9f220179009dafe0",
        url="https://pypi.org/packages/1e/00/919421f097de2a6ca2d9b4d9f3f596274e44c243a6ecca210cd0811032c0/einops-0.3.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.6.2-rc0:")
        depends_on("python@3.7:", when="@0.5:0.6.1")
