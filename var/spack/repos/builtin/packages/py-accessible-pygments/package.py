# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAccessiblePygments(PythonPackage):
<<<<<<< HEAD
    """A collection of accessible pygments styles."""
=======
    """This package includes a collection of accessible themes for pygments based on
    different sources."""
>>>>>>> develop

    homepage = "https://github.com/Quansight-Labs/accessible-pygments"
    pypi = "accessible-pygments/accessible-pygments-0.0.4.tar.gz"

<<<<<<< HEAD
    maintainers("chissg", "gartung", "marcmengel", "vitodb")

    version("0.0.4", sha256="e7b57a9b15958e9601c7e9eb07a440c813283545a20973f2574a5f453d0e953e")

    depends_on("py-setuptools", type="build")

    depends_on("py-pygments@1.5:", type=("build", "run"))
=======
    version("0.0.4", sha256="e7b57a9b15958e9601c7e9eb07a440c813283545a20973f2574a5f453d0e953e")

    depends_on("py-pygments@1.5:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
>>>>>>> develop
