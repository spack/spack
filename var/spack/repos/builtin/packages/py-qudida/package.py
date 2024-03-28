# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQudida(PythonPackage):
    """QuDiDA is a micro library for very naive though quick
    pixel level image domain adaptation via scikit-learn
    transformers."""

    homepage = "https://github.com/arsenyinfo/qudida"
    pypi = "qudida/qudida-0.0.4.tar.gz"

    version(
        "0.0.4",
        sha256="4519714c40cd0f2e6c51e1735edae8f8b19f4efe1f33be13e9d644ca5f736dd6",
        url="https://pypi.org/packages/f0/a1/a5f4bebaa31d109003909809d88aeb0d4b201463a9ea29308d9e4f9e7655/qudida-0.0.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@0.0.4:")
        depends_on("py-opencv-python-headless@4.0.1:", when="@0.0.4:")
        depends_on("py-scikit-learn@0.19.1:", when="@0.0.4:")
        depends_on("py-typing-extensions", when="@0.0.4:")
