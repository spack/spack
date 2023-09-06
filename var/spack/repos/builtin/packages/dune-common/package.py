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

    version(
        "2.9.0",
        sha256="35e6ede3da10be5c665db4cabb2bf4bd76a2e483255b2fca63c0a9d5ecad064c",
    )

    depends_on("cmake@3.13.0:", type="build")
    depends_on("mpi@2:")
    depends_on("ninja", type=("build"))
    depends_on("py-jinja2", type=("build"))
    depends_on("py-numpy", type=("build"))
    depends_on("py-setuptools@41", type=("build", "run"))
    depends_on("py-portalocker", type=("build"))
    depends_on("py-scikit-build", type=("build"))
    depends_on("py-wheel", type=("build"))
    depends_on("py-requests", type=("build"))
    depends_on("pkgconfig", type=("build"))
    depends_on("py-pip@21.1.2:", type=("build"))

    conflicts("%gcc@:6")
