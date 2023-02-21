# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydicom(PythonPackage):
    """Pure python package for DICOM medical file reading and writing

    pydicom is a pure Python package for working with DICOM files. It lets you
    read, modify and write DICOM data in an easy "pythonic" way."""

    homepage = "https://github.com/pydicom/pydicom"
    pypi = "pydicom/pydicom-2.1.2.tar.gz"

    version("2.3.0", sha256="dbfa081c9ad9ac8ff8a8efbd71784104db9eecf02fd775f7d7773f2183f89386")
    version("2.1.2", sha256="65f36820c5fec24b4e7ca45b7dae93e054ed269d55f92681863d39d30459e2fd")

    variant("numpy", default=False, description="Use NumPy for Pixel data")

    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-numpy", when="+numpy", type="run")
