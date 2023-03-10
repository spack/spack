# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtldld(PythonPackage):
    """Search, download, and prepare brain atlas data."""

    homepage = "atlas-download-tools.rtfd.io"
    git = "https://github.com/BlueBrain/Atlas-Download-Tools.git"
    pypi = "atldld/atldld-0.3.4.tar.gz"

    maintainers = ["EmilieDel", "jankrepl", "Stannislav"]

    # py-atlinter insists on atldld@0.2.2, and the diff with 0.3.4 is too big to quickly upgrade it
    version("0.3.4", sha256="4385d279e984864814cdb586d19663c525fe2c1eef8dd4be19e8a87b8520a913")
    version("0.2.2", sha256="4bdbb9ccc8e164c970940fc729a10bf883a67035e8c636261913cecb351835d3")

    # Build dependencies
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-appdirs", when="@0.3.1:", type=("build", "run"))
    depends_on("py-click@8:", when="@0.3.0:", type=("build", "run"))
    depends_on("py-dataclasses", when="@0.3.1: ^python@3.6", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("opencv+python3+python_bindings_generator+imgproc", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pillow", when="@0.3.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-responses", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))

    def patch(self):
        if self.version == Version("0.2.2"):
            # Like 0.3.4, it doesn't really need opencv-python
            # if opencv is installed with Python bindings
            filter_file('"opencv-python",', "", "setup.py")
