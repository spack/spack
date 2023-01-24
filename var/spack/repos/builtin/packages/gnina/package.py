# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gnina
#
# You can edit this file again by typing:
#
#     spack edit gnina
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Gnina(CMakePackage, CudaPackage):
    """GNINA: Molecular Docking with Deep Learning"""

    homepage = "https://github.com/gnina/gnina"
    url = "https://github.com/gnina/gnina/archive/refs/tags/v1.0.2.tar.gz"

    maintainers = ["RMeli"] # TODO: dkoes?

    version("1.0.2", sha256="476bfdce9b0d58c74a96fcc793345f4323e275fe6d5b111ee34aa2c86f0a3bba")

    depends_on("zlib")
    
    depends_on("python@3.6:")
    depends_on("py-numpy")
    depends_on("py-pip")
    depends_on("py-pytest")

    depends_on("boost+python+numpy")

    depends_on("openbabel@3.1:")
    #depends_on("rdkit")

    depends_on("eigen@3:")
    #depends_on("atlas")

    depends_on("glog")
    depends_on("protobuf")
    depends_on("hdf5+hl+cxx+shared")


    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
