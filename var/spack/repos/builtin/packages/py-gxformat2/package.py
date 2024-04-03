# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGxformat2(PythonPackage):
    """Galaxy Workflow Format 2 Descriptions"""

    homepage = "https://github.com/galaxyproject/gxformat2"
    pypi = "gxformat2/gxformat2-0.16.0.tar.gz"
    # note that requirements.txt is missing from the tarball. it can be found on github.

    license("MIT")

    version(
        "0.16.0",
        sha256="3501d7f0c2f75efb3a49e0805fd7597db691c2640bce2cdd71d8d263a2607793",
        url="https://pypi.org/packages/11/3d/88016d9ed55ce46cb89d3d2d14ef9f138ee6520a1d3faaba8c76d718fb6e/gxformat2-0.16.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-bioblend")
        depends_on("py-pyyaml")
