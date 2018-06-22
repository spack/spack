##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Pbbam(CMakePackage):
    """The pbbam software package provides components to create, query,
    & edit PacBio BAM files and associated indices.
    These components include a core C++ library,
    bindings for additional languages, and command-line utilities."""

    homepage = "https://github.com/PacificBiosciences/pbbam"
    url      = "https://github.com/PacificBiosciences/pbbam/archive/0.18.0.tar.gz"

    version('0.18.0', 'abbb687b1e7ea08916c26da828e11384')

    depends_on('zlib')
    depends_on('boost@1.55.0:')
    depends_on('htslib@1.3.1:')
    depends_on('doxygen+graphviz')

    conflicts('%gcc@:5.2.0')

    def cmake_args(self):
        options = []
        if self.run_tests:
            options.append('-DPacBioBAM_build_tests:BOOL=ON')
        else:
            options.append('-DPacBioBAM_build_tests:BOOL=OFF')

        return options

    def install(self, spec, prefix):
        install_tree('spack-build/bin', prefix.bin)
        install_tree('spack-build/lib', prefix.lib)
        install_tree('include/pbbam', prefix.include.pbbam)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('PacBioBAM_LIBRARIES', self.prefix.lib)
        spack_env.set('PacBioBAM_INCLUDE_DIRS', self.prefix.include)
