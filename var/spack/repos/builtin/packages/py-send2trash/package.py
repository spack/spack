# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySend2trash(PythonPackage):
    """Python library to send files to Trash/Recycle on all platforms."""

    homepage = "https://github.com/hsoft/send2trash"
    url = "https://github.com/hsoft/send2trash/archive/1.5.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.8.0",
        sha256="f20eaadfdb517eaca5ce077640cb261c7d2698385a6a0f072a4a5447fd49fa08",
        url="https://pypi.org/packages/47/26/3435896d757335ea53dce5abf8d658ca80757a7a06258451b358f10232be/Send2Trash-1.8.0-py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="f1691922577b6fa12821234aeb57599d887c4900b9ca537948d2dac34aea888b",
        url="https://pypi.org/packages/49/46/c3dc27481d1cc57b9385aff41c474ceb7714f7935b1247194adae45db714/Send2Trash-1.5.0-py3-none-any.whl",
    )
