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
#     spack install libmolgrid
#
# You can edit this file again by typing:
#
#     spack edit libmolgrid
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Libmolgrid(CMakePackage, CudaPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://gnina.github.io/libmolgrid/"
    url = "https://github.com/gnina/libmolgrid/archive/refs/tags/v0.5.2.tar.gz"

    # notify when the package is updated.
    maintainers = ["RMeli"]

    version("0.5.2", sha256="e732d13a96c2f374d57a73999119bef700172d392c195c751214aa6ac6680c3a")

    variant("shared", default=True)
    variant("static", default=True)
    variant("coverage", default=False)

    depends_on("cmake@3.18:", type="build")

    depends_on("boost+python+numpy")
    depends_on("zlib")
    
    depends_on("python@3.6:")
    depends_on("py-numpy")
    depends_on("py-numpy-quaternion")
    depends_on("py-pytest")

    depends_on("eigen@3:")
    
    depends_on("openbabel@3:", type=("build", "run"))
    
    depends_on("cuda")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED", "shared"),
            self.define_from_variant("BUILD_STATIC", "static"),        
        ]
        return args
