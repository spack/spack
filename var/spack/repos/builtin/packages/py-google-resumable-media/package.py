# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleResumableMedia(PythonPackage):
    """Utilities for Google Media Downloads and Resumable Uploads."""

    homepage = "https://github.com/GoogleCloudPlatform/google-resumable-media-python"
    pypi = "google-resumable-media/google-resumable-media-0.3.2.tar.gz"

    license("Apache-2.0")

    version(
        "2.7.0",
        sha256="79543cfe433b63fd81c0844b7803aba1bb8950b47bedf7d980c38fa123937e08",
        url="https://pypi.org/packages/b2/c6/1202ef64a9336d846f713107dac1c7a0b016cb3840ca3d5615c7005a23d1/google_resumable_media-2.7.0-py2.py3-none-any.whl",
    )
    version(
        "2.4.1",
        sha256="831e86fd78d302c1a034730a0c6e5369dd11d37bad73fa69ca8998460d5bae8d",
        url="https://pypi.org/packages/0b/d8/9a46125189d955ff50228351848019aef51775787db59373fefb20b09b3b/google_resumable_media-2.4.1-py2.py3-none-any.whl",
    )
    version(
        "0.3.2",
        sha256="2dae98ee716efe799db3578a7b902fbf5592fc5c77d3c0906fc4ef9b1b930861",
        url="https://pypi.org/packages/e2/5d/4bc5c28c252a62efe69ed1a1561da92bd5af8eca0cdcdf8e60354fae9b29/google_resumable_media-0.3.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.4:")
        depends_on("py-google-crc32c@1:", when="@1:2.0.1,2.0.3:")
        depends_on("py-six", when="@:1.3.0")
