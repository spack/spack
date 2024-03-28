# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpectral(PythonPackage):
    """Spectral Python (SPy) is a pure Python module for processing
    hyperspectral image data (imaging spectroscopy data). It has functions for
    reading, displaying, manipulating, and classifying hyperspectral imagery.
    SPy is Free, Open Source Software (FOSS) distributed under the MIT
    License."""

    homepage = "http://www.spectralpython.net/"
    pypi = "spectral/spectral-0.22.4.tar.gz"

    license("MIT")

    version(
        "0.22.4",
        sha256="46643a3379c748d643de6de2c30acd54b067721be7b5b5bce0aee076ebbb227c",
        url="https://pypi.org/packages/29/58/0d1988431c253cc8628c7946ff753498149f50a899e8c5383fe17625d2b9/spectral-0.22.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@0.21:0.22.1,0.22.3:")
