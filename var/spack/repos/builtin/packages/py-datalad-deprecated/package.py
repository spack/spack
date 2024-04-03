# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladDeprecated(PythonPackage):
    """DataLad extension package for deprecated functionality that was phased
    out in the core package."""

    homepage = "https://github.com/datalad/datalad-deprecated"
    pypi = "datalad_deprecated/datalad_deprecated-0.3.0.tar.gz"

    license("MIT")

    version(
        "0.3.0",
        sha256="4c95890996ee50aa67b813fc7bf47f4e07ac25eb8148932c0aac3bc838567b71",
        url="https://pypi.org/packages/94/dc/280c34ac6efc0099c787a80067605cebdbbae572db9d3e0180fa8b632450/datalad_deprecated-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2:")
        depends_on("py-datalad@0.18:", when="@0.3:")
        depends_on("py-exifread", when="@0.2.3:")
        depends_on("py-jsmin")
        depends_on("py-mutagen@1.36:", when="@0.2.3:")
        depends_on("py-pillow", when="@0.2.3:")
        depends_on("py-python-xmp-toolkit", when="@0.2.3:")
        depends_on("py-pyyaml", when="@0.2.3:")
        depends_on("py-whoosh", when="@0.2.3:")
