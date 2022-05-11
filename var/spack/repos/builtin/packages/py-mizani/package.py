# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.directives import depends_on, version
from spack.util.package import *


class PyMizani(PythonPackage):
    """Mizani is a scales package for graphics. It is based on Hadley Wickham's
    Scales package."""

    pypi = "mizani/mizani-0.7.3.tar.gz"

    version(
        "0.7.3",
        sha256="f521300bd29ca918fcd629bc8ab50fa04e41bdbe00f6bcf74055d3c6273770a4",
    )

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on("py-matplotlib@3.1.1:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-palettable", type=("build", "run"))
    depends_on("py-pandas@1.1.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
