# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGtdbtk(PythonPackage):
    """GTDB-Tk is a software toolkit for assigning objective taxonomic
    classifications to bacterial and archaeal genomes based on the Genome
    Database Taxonomy (GTDB)."""

    homepage = "https://github.com/Ecogenomics/GTDBTk"
    pypi = "gtdbtk/gtdbtk-2.1.0.tar.gz"

    license("GPL-3.0-only")

    version(
        "2.3.2",
        sha256="b84a0fa3ca482024f0966aced7e3eccc1fa596c10eea364328ec8ee6089e761a",
        url="https://pypi.org/packages/34/25/c0306cf86abfa667f94f0d7591b251977b7f7af57ce613217873398bc0e5/gtdbtk-2.3.2-py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="69d8ff2d00e8903f8e945b2d5def335d3610a8b953cffeaba0b9490adb8bf4c9",
        url="https://pypi.org/packages/4e/be/72ff9d9e718e08898e8f9817ae91d06c8364b288d3c082026ddab01ba4e0/gtdbtk-2.3.0-py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="6fcf963519fb2fe7c3287f58d017fad7a4a9f1641d026442d52c9daf024213ee",
        url="https://pypi.org/packages/b8/78/853a62dd98c99a31191df3f6d130834cad0ae00c5159d32cb9667af48943/gtdbtk-2.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dendropy@4.1:", when="@1.2:")
        depends_on("py-numpy@1.9:", when="@1.2:")
        depends_on("py-pydantic@1.9.2:1", when="@2.3.2:")
        depends_on("py-pydantic", when="@2.2.1:2.3.0")
        depends_on("py-tqdm@4.35:", when="@1.6:")
