# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIntensityNormalization(PythonPackage):
    """Normalize intensities of images from various MRI modalities"""

    homepage = "https://github.com/jcreinhold/intensity-normalization"
    pypi = "intensity-normalization/intensity-normalization-2.1.1.tar.gz"

    license("Apache-2.0")

    version(
        "2.1.1",
        sha256="b5cdfb141ceb63a4bde000c8a7e7f82a15a09d739b478aafaf72542018fcaa95",
        url="https://pypi.org/packages/ec/02/4361f8d1e05cf9a31d7a7d1a19be9e685cc452f90784773ab8123d860d58/intensity_normalization-2.1.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-matplotlib", when="@:2.1.2")
        depends_on("py-nibabel", when="@:2.1.2")
        depends_on("py-numpy", when="@:2.1.2")
        depends_on("py-scikit-fuzzy", when="@:2.1.2")
        depends_on("py-scikit-image", when="@:2.1.2")
        depends_on("py-scikit-learn", when="@:2.1.2")
        depends_on("py-scipy", when="@:2.1.2")
        depends_on("py-statsmodels", when="@:2.1.2")
