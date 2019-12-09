# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openmolcas(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://gitlab.com/Molcas/OpenMolcas"
    url      = "https://github.com/Molcas/OpenMolcas/archive/v19.11.tar.gz"

    version('19.11', sha256='8ebd1dcce98fc3f554f96e54e34f1e8ad566c601196ee68153763b6c0a04c7b9')

    depends_on('cmake', type='build')
    depends_on('hdf5')
    depends_on('lapack')
    depends_on('openblas+ilp64')

    def install(self, spec, prefix):
        # configure paths to external libraries and compiler
        conf_cmake = Executable('./configure-cmake')
        conf_cmake('--openblas', self.spec['openblas'].prefix, '--prefix', prefix)

        # run compile script
        Executable('./make-gnu_dev_openblas')()

        # install build
        with working_dir('builds/gnu_dev_openblas'):
            which('make')('install')
