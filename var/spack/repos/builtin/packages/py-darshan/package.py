# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDarshan(PythonPackage):
    """Python utilities to interact with Darshan log records of HPC applications."""

    homepage = "https://www.mcs.anl.gov/research/projects/darshan"
    pypi = "darshan/darshan-3.4.0.1.tar.gz"

    maintainers = ["jeanbez", "shanedsnyder"]

    version("3.4.0.1", sha256="0142fc7c0b12a9e5c22358aa26cca7083d28af42aeea7dfcc5698c56b6aee6b7")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-mako", type=("build", "run"))

    depends_on("darshan-util", type=("build", "run"))
