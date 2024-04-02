# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDocstringToMarkdown(PythonPackage):
    """On the fly conversion of Python docstrings to markdown."""

    homepage = "https://github.com/python-lsp/docstring-to-markdown"
    pypi = "docstring-to-markdown/docstring-to-markdown-0.10.tar.gz"

    maintainers("alecbcs")

    license("LGPL-2.1-or-later")

    version(
        "0.11",
        sha256="01900aee1bc7fde5aacaf319e517a5e1d4f0bf04e401373c08d28fcf79bfb73b",
        url="https://pypi.org/packages/ea/69/88a13ac387ebd1fcfda95eccfe4fa2dfb7e9794c7fa6a76c497c0bfe135c/docstring_to_markdown-0.11-py3-none-any.whl",
    )
    version(
        "0.10",
        sha256="a2cd520599d1499d4a5d4eb16dea5bdebe32e5627504fb417d5733570f3d4d0b",
        url="https://pypi.org/packages/a9/ad/71cb84c8be4aa428d27b2c8e380a265b61671b2a15ce0dc4103133d12f6b/docstring_to_markdown-0.10-py3-none-any.whl",
    )
