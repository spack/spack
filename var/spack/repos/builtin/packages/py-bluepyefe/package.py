# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyBluepyefe(PythonPackage):
    """Blue Brain Python E-feature extraction"""

    homepage = "https://github.com/BlueBrain/BluePyEfe"
    pypi = "bluepyefe/bluepyefe-2.2.18.tar.gz"
    git = "https://github.com/BlueBrain/BluePyEfe.git"

    version("2.2.18", sha256="bfb50c6482433ec2ffb4b65b072d2778bd89ae50d92dd6830969222aabb30275")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@:1.23", type=("build", "run"))
    depends_on("py-neo", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-efel", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-igor", type=("build", "run"))
