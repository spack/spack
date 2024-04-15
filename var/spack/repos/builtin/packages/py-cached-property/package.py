# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachedProperty(PythonPackage):
    """A decorator for caching properties in classes."""

    pypi = "cached-property/cached-property-1.5.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.5.2",
        sha256="df4f613cf7ad9a588cc381aaf4a512d26265ecebd5eb9e1ba12f1319eb85a6a0",
        url="https://pypi.org/packages/48/19/f2090f7dad41e225c7f2326e4cfe6fff49e57dedb5b53636c9551f86b069/cached_property-1.5.2-py2.py3-none-any.whl",
    )
    version(
        "1.5.1",
        sha256="3a026f1a54135677e7da5ce819b0c690f156f37976f3e30c5430740725203d7f",
        url="https://pypi.org/packages/3b/86/85c1be2e8db9e13ef9a350aecd6dea292bd612fa288c2f40d035bb750ded/cached_property-1.5.1-py2.py3-none-any.whl",
    )
