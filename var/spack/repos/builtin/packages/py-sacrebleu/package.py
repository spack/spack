# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySacrebleu(PythonPackage):
    """SacreBLEU is a standard BLEU implementation that downloads and manages
    WMT datasets, produces scores on detokenized outputs, and reports a string
    encapsulating BLEU parameters, facilitating the production of shareable,
    comparable BLEU scores."""

    homepage = "https://github.com/mjpost/sacrebleu"
    pypi = "sacrebleu/sacrebleu-2.0.0.tar.gz"

    license("Apache-2.0")

    version(
        "2.0.0",
        sha256="1acae0221e27c23c4987834fd17b284b4addc6556941c2097c4d618baa2d67af",
        url="https://pypi.org/packages/fa/63/b3c11f951eafa2dc296862431f29fb12dbe191cb72217cf88ed04c32086b/sacrebleu-2.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama", when="@2:")
        depends_on("py-numpy@1.17.0:", when="@2:")
        depends_on("py-portalocker", when="@1.4:1.5.0,2:")
        depends_on("py-regex", when="@2:")
        depends_on("py-tabulate@0.8.9:", when="@2:")

    def patch(self):
        touch("CHANGELOG.md")
