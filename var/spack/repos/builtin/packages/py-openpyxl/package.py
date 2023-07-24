# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpyxl(PythonPackage):
    """A Python library to read/write Excel 2010 xlsx/xlsm files"""

    homepage = "https://openpyxl.readthedocs.org/"
    pypi = "openpyxl/openpyxl-3.1.2.tar.gz"

    version("3.1.2", sha256="a6f5977418eff3b2d5500d54d9db50c8277a368436f4e4f8ddb1be3422870184")
    version("3.0.7", sha256="6456a3b472e1ef0facb1129f3c6ef00713cebf62e736cd7a75bcc3247432f251")
    version("3.0.3", sha256="547a9fc6aafcf44abe358b89ed4438d077e9d92e4f182c87e2dc294186dc4b64")

    depends_on("python@3.7:", when="@3.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-et-xmlfile", when="@2.4:", type=("build", "run"))
    depends_on("py-pip@18.0:", when="@3.1.2:", type=("build", "run"))
    depends_on("py-lxml@4.2.0:", when="@3.1.2:", type=("build", "run"))
    depends_on("py-pillow", when="@3.1.2:", type=("build", "run"))
    depends_on("py-tox", when="@3.1.2:", type=("build", "run"))
    depends_on("py-pandas", when="@3.1.2:", type=("build", "run"))
