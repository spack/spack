# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOdfpy(PythonPackage):
    """Odfpy is a library to read and write OpenDocument v. 1.2 files."""

    homepage = "https://github.com/eea/odfpy"
    url = "https://github.com/eea/odfpy/archive/release-1.4.1.tar.gz"

    version("1.4.1", sha256="9f97e4c808f656ce22739eec43a7c1741f645b7decef37d4fb048edb33e8caad")

    depends_on("py-setuptools", type="build")
    depends_on("py-defusedxml", type=("build", "run"))