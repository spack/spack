# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEsmpy(PythonPackage):
    """ESMPy is a Python interface to the Earth System Modeling Framework (ESMF)"""

    homepage = "https://earthsystemmodeling.org/"
    git = "https://github.com/esmf-org/esmf.git"

    # because it relies on py-setuptools-git-versioning, we need to install from git
    version("develop", branch="develop")
    version("8.4.0", tag="v8.4.0")
    version("8.3.1", tag="v8.3.1")
    version("8.3.0", tag="v8.3.0")
    version("8.2.0", tag="v8.2.0")
    version("8.1.1", tag="v8.1.1")
    version("8.0.1", tag="v8.0.1")
    version("8.0.0", tag="v8.0.0")

    maintainers("angus-g")

    # require an in-sync version of ESMF
    for v in ["develop", "8.4.0", "8.3.1", "8.3.0", "8.2.0", "8.1.1", "8.0.1", "8.0.0"]:
        depends_on(f"esmf@{v}", when=f"@{v}", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-git-versioning", type="build")

    build_directory = "src/addon/esmpy"
