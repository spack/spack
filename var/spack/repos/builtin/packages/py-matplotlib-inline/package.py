# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMatplotlibInline(PythonPackage):
    """Inline Matplotlib backend for Jupyter."""

    homepage = "https://github.com/ipython/matplotlib-inline"
    pypi = "matplotlib-inline/matplotlib-inline-0.1.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1.6",
        sha256="f1f41aab5328aa5aaea9b16d083b128102f8712542f819fe7e6a420ff581b311",
        url="https://pypi.org/packages/f2/51/c34d7a1d528efaae3d8ddb18ef45a41f284eacf9e514523b191b7d0872cc/matplotlib_inline-0.1.6-py3-none-any.whl",
    )
    version(
        "0.1.3",
        sha256="aed605ba3b72462d64d475a21a9296f400a19c4f74a31b59103d2a99ffd5aa5c",
        url="https://pypi.org/packages/a6/2d/2230afd570c70074e80fd06857ba2bdc5f10c055bd9125665fe276fadb67/matplotlib_inline-0.1.3-py3-none-any.whl",
    )
    version(
        "0.1.2",
        sha256="5cf1176f554abb4fa98cb362aa2b55c500147e4bdbb07e3fda359143e1da0811",
        url="https://pypi.org/packages/7f/de/6c111d687335729cf8c156394c8d119b0dc3c34b6966ff2a2f7fe4aa79cf/matplotlib_inline-0.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-traitlets")

    # Undocumented dependency
