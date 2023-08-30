# copyright 2013-2023 lawrence livermore national security, llc and other
# spack project developers. see the top-level copyright file for details.
#
# spdx-license-identifier: (apache-2.0 or mit)


from spack.package import *


class dunecommon(pythonpackage):
    """dune, the distributed and unified numerics environment
        is a modular toolbox for solving partial differential
        equations (pdes) with grid-based methods.
        it supports the easy implementation of methods
        like finite elements (fe), finite volumes (fv),
        and also finite differences (fd).
    """

    homepage = "https://www.dune-project.org/doc/gettingstarted/"
    git = "https://gitlab.dune-project.org/core/dune-common"
    pypi = "dune-common/dune-common-2.9.0.tar.gz"

    version("2.9.0")

    depends_on("cmake@3.13.0:", type="build")
    depends_on("mpi@2:")
    depends_on("pkgconf", type="build")
