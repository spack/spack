# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExodusBundler(PythonPackage):
    """Exodus is a tool that makes it easy to successfully relocate Linux
    ELF binaries from one system to another."""

    homepage = "https://github.com/intoli/exodus"
    pypi = "exodus-bundler/exodus-bundler-2.0.2.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version(
        "2.0.2",
        sha256="efa3392428cfccf9a52539b96eac2a2aab0cb4ac83703028c1574a367d5adae6",
        url="https://pypi.org/packages/3e/f6/5eda49f30947093fe559d8c6b6a3b41baf9a84989e7aa172bce388a1974d/exodus_bundler-2.0.2-py2.py3-none-any.whl",
    )
