# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sourmash(PythonPackage):
    """Sourmash: Quickly search, compare, and analyze genomic and metagenomic data sets with
    k-mer sketches."""

    homepage = "https://sourmash.bio/"
    pypi = "sourmash/sourmash-4.8.2.tar.gz"

    version("4.8.2", sha256="e0df78032e53ed88977445933ba3481dd10c7d3bd26d019511a6a4e6d7518475")

    depends_on("python@3.8:")
    # build-only
    depends_on("py-maturin@1:", type="build")
    depends_on("rust", type="build")
    # general
    depends_on("py-screed@1.1.2:")
    depends_on("py-cffi@1.14.0:")
    depends_on("py-numpy")
    depends_on("py-matplotlib")
    depends_on("py-scipy")
    depends_on("py-deprecation@2.0.6:")
    depends_on("py-cachetools@4:")
    depends_on("py-bitstring@3.1.9:")
    depends_on("py-importlib_metadata@3.6:", when="^python@:3.9")
