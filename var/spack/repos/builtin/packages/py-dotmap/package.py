# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class PyDotmap(PythonPackage):
    """Dot access dictionary with dynamic hierarchy creation and ordered iteration"""

    homepage = "https://pypi.org/project/dotmap/"
    pypi = "dotmap/dotmap-1.3.30.tar.gz"

    version("1.3.30", sha256="5821a7933f075fb47563417c0e92e0b7c031158b4c9a6a7e56163479b658b368")

    depends_on("py-setuptools", type=("build", "run"))
