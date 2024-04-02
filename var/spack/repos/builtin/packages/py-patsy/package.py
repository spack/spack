# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPatsy(PythonPackage):
    """A Python package for describing statistical models and for
    building design matrices."""

    homepage = "https://github.com/pydata/patsy"
    pypi = "patsy/patsy-0.5.2.tar.gz"

    license("PSF-2.0")

    version(
        "0.5.3",
        sha256="7eb5349754ed6aa982af81f636479b1b8db9d5b1a6e957a6016ec0534b5c86b7",
        url="https://pypi.org/packages/2a/e4/b3263b0e353f2be7b14f044d57874490c9cef1798a435f038683acea5c98/patsy-0.5.3-py2.py3-none-any.whl",
    )
    version(
        "0.5.2",
        sha256="cc80955ae8c13a7e7c4051eda7b277c8f909f50bc7d73e124bc38e2ee3d95041",
        url="https://pypi.org/packages/87/7f/d37cd027c25145eeba92b1a756976931c831803d92547c8637a3400c339f/patsy-0.5.2-py2.py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="5465be1c0e670c3a965355ec09e9a502bf2c4cbe4875e8528b0221190a8a5d40",
        url="https://pypi.org/packages/ea/0c/5f61f1a3d4385d6bf83b83ea495068857ff8dfb89e74824c6e9eb63286d8/patsy-0.5.1-py2.py3-none-any.whl",
    )
    version(
        "0.4.1",
        sha256="63102f77df5c6b0c3fe3bf9d57bcea112d1e06d00a41823662b5044ce681f22c",
        url="https://pypi.org/packages/02/8a/255f80a7f939006ec479275fde6301feedf3fdd9ecee782bb64987b84de8/patsy-0.4.1-py2.py3-none-any.whl",
    )

    variant("splines", default=False, description="Offers spline related functions")

    with default_args(type="run"):
        depends_on("py-numpy@1.4:", when="@0.5:")
        depends_on("py-numpy", when="@0.4.1:0.4")
        depends_on("py-six", when="@0.4.1:")
