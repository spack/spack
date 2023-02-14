# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBidscoin(PythonPackage):
    """Converts and organises raw MRI data-sets according to the Brain Imaging
    Data Structure (BIDS)."""

    homepage = "https://github.com/Donders-Institute/bidscoin"
    pypi = "bidscoin/bidscoin-3.7.4.tar.gz"

    version("3.7.4", sha256="efa32238fb7b75e533e7f5cc318ad5a703716d291985435d43f1de4f18402517")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")

    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pydicom@2:", type=("build", "run"))
    depends_on("py-pyqt5@5.12.1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.15.35:", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-multiecho@0.25:", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("dcm2niix", type=("build", "run"))
