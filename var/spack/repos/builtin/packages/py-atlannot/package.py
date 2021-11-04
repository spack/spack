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

    version(
        "0.1.2",
        url="https://files.pythonhosted.org/packages/08/b9/6edff732ad711e600b91d32052604987b744f054c049739df73c07ef0232/atlannot-0.1.2.tar.gz",
        sha256="145dac874752d5e5d093b977aa04798916daf31d1e942cc64d059175deea27df",
    )
    version(
        "0.1.1",
        tag="v0.1.1",
        git="git@bbpgitlab.epfl.ch:project/proj101/atlas_annotation.git",
    )

    # Setup requirements
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    # Installation requirements
    depends_on("py-antspyx@0.2.4", type=("build", "run"))
    depends_on("py-atldld@0.2.2", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pynrrd", type=("build", "run"))

    # From the "interactive" extra
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-ipywidgets", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
