# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEntrypoints(PythonPackage):
    """Discover and load entry points from installed packages."""

    homepage = "https://github.com/takluyver/entrypoints"
    pypi = "entrypoints/entrypoints-0.2.3.tar.gz"

    license("MIT")

    version(
        "0.4",
        sha256="f174b5ff827504fd3cd97cc3f8649f3693f51538c7e4bdf3ef002c8429d42f9f",
        url="https://pypi.org/packages/35/a8/365059bbcd4572cbc41de17fd5b682be5868b218c3c5479071865cab9078/entrypoints-0.4-py3-none-any.whl",
    )
    version(
        "0.3",
        sha256="589f874b313739ad35be6e0cd7efde2a4e9b6fea91edcc34e58ecbb8dbe56d19",
        url="https://pypi.org/packages/ac/c6/44694103f8c221443ee6b0041f69e2740d89a25641e62fb4f2ee568f2f9c/entrypoints-0.3-py2.py3-none-any.whl",
    )
    version(
        "0.2.3",
        sha256="10ad569bb245e7e2ba425285b9fa3e8178a0dc92fc53b1e1c553805e15a8825b",
        url="https://pypi.org/packages/cc/8b/4eefa9b47f1910b3d2081da67726b066e379b04ca897acfe9f92bac56147/entrypoints-0.2.3-py2.py3-none-any.whl",
    )
