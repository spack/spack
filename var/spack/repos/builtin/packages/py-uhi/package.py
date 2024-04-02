# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUhi(PythonPackage):
    """Unified Histogram Interface:
    tools to help library authors work with histograms"""

    homepage = "https://github.com/Scikit-HEP/uhi"
    pypi = "uhi/uhi-0.3.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.3.3",
        sha256="4805a4194550310ee2a58aa8c777e6ab80f8896c96469d7c16fd2436aef4c9c3",
        url="https://pypi.org/packages/70/e7/599c0589e0fcb3f330ea6cc13b3fde9d3f0a65fe939f9b5634c50dde6349/uhi-0.3.3-py3-none-any.whl",
    )
    version(
        "0.3.2",
        sha256="427d7d54f1ac072a52f3b476457732ecd3767da00b2a8b6fdc38dd6820db107e",
        url="https://pypi.org/packages/ad/36/fbc93bc03270b16fd80d7e870fb459289aaaa6b1077bc8cd12836b4b751f/uhi-0.3.2-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="5c2f7ceceacd349f906104a7776859812e0926936273667eadf56762133d6d5e",
        url="https://pypi.org/packages/67/03/b2731129bba0ed39f3dbb5e5cea557491efb82f34cf2d7a9fbaee2be4a83/uhi-0.3.1-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="20fe823e7e34f8f0a5a223ba3c22c164b43cb8fc2b2f9b4ed2e2cd6fceea583e",
        url="https://pypi.org/packages/94/af/227bc7260a770fafe939e9c663ae348f6869f2964e58b1065cf9c312046b/uhi-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.13.3:", when="@0.2:")
        depends_on("py-typing-extensions@3.7:", when="@0.1.2: ^python@:3.7")
