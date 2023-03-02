# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyAtlannot(PythonPackage):
    """Alignment of brain atlas annotations."""

    homepage = "https://atlas-annotation.rtfd.io"
    maintainers = ["EmilieDel", "Stannislav"]
    pypi = "atlannot/atlannot-0.1.3.tar.gz"

    version("0.1.3", sha256="66717d37dd7808f8d7543c8da4d2b09c7e21d9c6151474ad1079b10d7b66d243")

    # Setup requirements
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    # Installation requirements
    depends_on("py-antspyx@0.2.7:", type=("build", "run"))
    depends_on("py-atldld@0.2.2:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy@1.20:", type=("build", "run"))
    depends_on("py-pynrrd", type=("build", "run"))

    # From the "interactive" extra
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-ipywidgets", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
