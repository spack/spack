# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCommonmark(PythonPackage):
    """commonmark.py is a pure Python port of jgm's commonmark.js, a Markdown
    parser and renderer for the CommonMark specification, using only native
    modules."""

    homepage = "https://github.com/readthedocs/commonmark.py"
    pypi = "commonmark/commonmark-0.9.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.9.1",
        sha256="da2f38c92590f83de410ba1a3cbceafbc74fee9def35f9251ba9a971d6d66fd9",
        url="https://pypi.org/packages/b1/92/dfd892312d822f36c55366118b95d914e5f16de11044a27cf10a7d71bbbf/commonmark-0.9.1-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="14c3df31e8c9c463377e287b2a1eefaa6019ab97b22dad36e2f32be59d61d68d",
        url="https://pypi.org/packages/a7/65/2ea45a38e8c6a0a13453c5cadcc9b725049425c8628dbe7da87b30944573/commonmark-0.9.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-future", when="@0.8.1:0.9.0")
