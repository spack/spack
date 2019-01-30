# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Spherepack(Package):
    """SPHEREPACK - A Package for Modeling Geophysical Processes"""

    homepage = "https://www2.cisl.ucar.edu/resources/legacy/spherepack"
    url      = "https://www2.cisl.ucar.edu/sites/default/files/spherepack3.2.tar"

    version('3.2', '283627744f36253b4260efd7dfb7c762')

    def install(self, spec, prefix):
        if self.compiler.fc is None:
            raise InstallError("SPHEREPACK requires a Fortran 90 compiler")
        make("MAKE=make", "F90=f90 -O2", "AR=ar", "libspherepack")
        make("MAKE=make", "F90=f90 -O2", "AR=ar", "testspherepack")
        install_tree("lib", prefix.lib)
