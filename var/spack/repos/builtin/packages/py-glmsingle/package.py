# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGlmsingle(PythonPackage):
    """A toolbox for accurate single-trial estimates in fMRI time-series data."""

    homepage = "https://github.com/cvnlab/GLMsingle"
    url = "https://github.com/cvnlab/GLMsingle/archive/refs/tags/1.0.tar.gz"
    git = "https://github.com/cvnlab/GLMsingle.git"

    version("main", branch="main")
    version("1.1", sha256="3fe3cb1f0d1e96976f2c707b1f9e8ddb932b74f58e99debbfa6f17761fdbd37b")
    version("1.0", sha256="0481f8ea7637d7e9cb53a7f22c73ba67b9fb8aefebc8c6c98bd4712de95db6aa")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-fracridge", type=("build", "run"))
    depends_on("py-nibabel", when="@1.1:", type=("build", "run"))
    depends_on("py-h5py", when="@1.1:", type=("build", "run"))

    with when("@:1.0"):
        depends_on("py-twine", type=("build", "run"))
        depends_on("py-sphinx", type=("build", "run"))
        depends_on("py-seaborn", type=("build", "run"))
        depends_on("py-pybids@0.8.0", type=("build", "run"))
        depends_on("py-duecredit", type=("build", "run"))
        depends_on("py-ww", type=("build", "run"))
        depends_on("py-numba", type=("build", "run"))
        depends_on("py-joblib", type=("build", "run"))
        depends_on("py-datalad", type=("build", "run"))
        depends_on("py-imageio", type=("build", "run"))
