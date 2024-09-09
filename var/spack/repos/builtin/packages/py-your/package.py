# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYour(PythonPackage):
    """Python library to read and process pulsar data in several different formats"""

    homepage = "https://github.com/thepetabyteproject/your"
    git = "https://github.com/thepetabyteproject/your.git"

    maintainers("aweaver1fandm")

    license("GPL-3.0")

    version("main", branch="main", preferred=True)

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-astropy@6.1.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.2.1:", type=("build", "run"))
    depends_on("py-numpy@1.18.4:", type=("build", "run"))
    depends_on("py-h5py@2.10:", type=("build", "run"))
    depends_on("py-scikit-image@0.14.2:", type=("build", "run"))
    depends_on("py-scipy@1.3:", type=("build", "run"))
    depends_on("py-numba@0.48:", type=("build", "run"))
    depends_on("py-pandas@1.0.3:", type=("build", "run"))
    depends_on("py-rich@8:", type=("build", "run"))
