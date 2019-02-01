# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
