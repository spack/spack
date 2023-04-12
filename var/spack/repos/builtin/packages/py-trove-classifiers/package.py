# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTroveClassifiers(PythonPackage):
    """The trove-classifiers pacakge is the canonical source for classifiers
    on PyPI. Classifiers categorize projects per PEP 301."""

    homepage = "https://github.com/pypa/trove-classifiers"
    pypi = "trove-classifiers/trove-classifiers-2023.3.9.tar.gz"

    version("2023.3.9", sha256="ee42f2f8c1d4bcfe35f746e472f07633570d485fab45407effc0379270a3bb03")

    depends_on("py-setuptools", type="build")
    depends_on("py-calver", type="build")
