# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpycanvas(PythonPackage):
    """Interactive Canvas in Jupyter."""

    homepage = "https://github.com/martinRenou/ipycanvas"
    pypi = "ipycanvas/ipycanvas-0.9.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.10.2",
        sha256="5313417fa0a57c22253194f04e07c09213b12efa1e74024b323e4b19152b8977",
        url="https://pypi.org/packages/10/ca/752f0b9b406a8108930e36199ade32191b1348cd69c196afe7105c9c958e/ipycanvas-0.10.2-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="4a0b2bcc6b7403c02b6ac1fd6a65800b414a166072ede7998d94b74fd4ba9d08",
        url="https://pypi.org/packages/b6/8b/ec60ae3d0596214c45c70788a7ecbc2ab303ab26decffd318a0e791f48e0/ipycanvas-0.9.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ipywidgets@7.6.0:", when="@0.8.1:0.12.0")
        depends_on("py-numpy")
        depends_on("py-pillow@6:")
