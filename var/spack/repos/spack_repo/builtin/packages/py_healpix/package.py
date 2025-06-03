# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyHealpix(PythonPackage):
    """Python and C package for HEALPix discretisation of the sphere"""

    homepage = "https://github.com/ntessore/healpix"
    pypi = "healpix/healpix-2024.2.tar.gz"

    license("BSD-3-Clause", checked_by="Chrismarsh")

    version("2024.2", sha256="dc908dd39080a088476bfc451b6dcfe9ad015851473b8d97177bf698e4748ae3")

    depends_on("py-setuptools@61.0:", type="build")
    depends_on("py-numpy@2:", type=("build", "run"))
