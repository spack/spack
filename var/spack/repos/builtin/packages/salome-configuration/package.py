# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Important feature: a set of salome-xxx packages must have all the same version
# - except salome-med that is also fixed but by another number version

from spack.pkgkit import *


class SalomeConfiguration(Package):
    """salome-configuration is a part of SALOME platform and define general
    build tools for the platform."""

    maintainers = ['franciskloss']

    homepage = "https://www.salome-platform.org"
    git      = "https://git.salome-platform.org/gitpub/tools/configuration.git"

    version('9.7.0', tag='V9_7_0')
    version('9.6.0', tag='V9_6_0')
    version('9.5.0', tag='V9_5_0')
    version('9.4.0', tag='V9_4_0')
    version('9.3.0', tag='V9_3_0')

    patch('SalomeMacros.patch',   working_dir='./cmake')
    patch('FindSalomeHDF5.patch', working_dir='./cmake')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('CONFIGURATION_ROOT_DIR', self.prefix)

    def install(self, spec, prefix):
        install_tree('.', prefix)
