# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DuneCommon(PythonPackage):
    """Dune, the distributed and unified numerics environment."""

    homepage = "https://www.dune-project.org/doc/gettingstarted/"
    git = "https://gitlab.dune-project.org/core/dune-common"
    pypi = "dune-common/dune-common-2.9.0.tar.gz"
    url = "https://files.pythonhosted.org/packages/c4/3e/48a506e9f42e1c3f384f55f578b887bba77916cb51f7ceff9d0bd9f315a8/dune-common-2.9.0.tar.gz"

    version("2.9.0", sha256="35e6ede3da10be5c665db4cabb2bf4bd76a2e483255b2fca63c0a9d5ecad064c")

    # FIXME: Add dependencies if required.
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("cmake@3.13.0:", type="build")
    depends_on("mpi@2:")
    depends_on("pkgconf", type="build")
    depends_on("gcc@7:", type="build")
