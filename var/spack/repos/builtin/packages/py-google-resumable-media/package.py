# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleResumableMedia(PythonPackage):
    """Utilities for Google Media Downloads and Resumable Uploads."""

    homepage = "https://github.com/GoogleCloudPlatform/google-resumable-media-python"
    pypi = "google-resumable-media/google-resumable-media-0.3.2.tar.gz"

    version("2.4.1", sha256="15b8a2e75df42dc6502d1306db0bce2647ba6013f9cd03b6e17368c0886ee90a")
    version("0.3.2", sha256="3e38923493ca0d7de0ad91c31acfefc393c78586db89364e91cb4f11990e51ba")

    depends_on("py-setuptools", type="build")
    depends_on("py-google-crc32c@1:", when="@2:", type=("build", "run"))
    depends_on("py-six", when="@0", type=("build", "run"))
