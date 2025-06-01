# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyFasttextNumpy2(PythonPackage):
    """Library for efficient text classification and representation
    learning, fixed for numpy 2 compatibility."""

    homepage = "https://github.com/simon-ging/fasttext-numpy2"
    pypi = "fasttext-numpy2/fasttext-numpy2-0.10.4.tar.gz"

    maintainers("thomas-bouvier")

    version("0.10.4", sha256="156e84cf2c7db95b24897884284be52c1038fe2b1d0bd9f21bcaf363d2542825")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pybind11@2.2:", type=("build", "run"))
