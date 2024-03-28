# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonBioformats(PythonPackage):
    """Python-bioformats is a Python wrapper for Bio-Formats, a standalone
    Java library for reading and writing life sciences image file formats.
    Bio-Formats is capable of parsing both pixels and metadata for
    a large number of formats, as well as writing to several formats."""

    homepage = "https://github.com/CellProfiler/python-bioformats/"
    pypi = "python-bioformats/python-bioformats-4.0.5.tar.gz"

    license("GPL-2.0-only")

    version(
        "4.0.5",
        sha256="9c5cc32dd78c7b6e891513f0dc897c4c74a8fd4d9e9afb69d40edd0eb481320f",
        url="https://pypi.org/packages/5d/48/0873186982a2800060e63095cfd6b299e815e866ab0fa8bfe2a9cb1d8a08/python_bioformats-4.0.5-py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="53056361d217be870e6071a1d96fecd1519c4a3a3d7c2733b65883e6f124c8d7",
        url="https://pypi.org/packages/61/64/de0a193af35e7052563a5a7af50461e060780f2a9dc7311504eefe921bb1/python_bioformats-4.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-boto3@1.14.23:", when="@4.0.0-rc4:4.0.0,4.0.4:")
        depends_on("py-future@0.18.2:", when="@4.0.0-rc4:4.0.0,4.0.4:")
        depends_on("py-python-javabridge@4.0.3:", when="@4.0.4:")
        depends_on("py-python-javabridge@4.0.0", when="@4.0.0")
