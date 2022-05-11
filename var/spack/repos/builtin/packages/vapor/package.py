# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Vapor(CMakePackage):
    """VAPOR is the Visualization and Analysis Platform for Ocean, Atmosphere,
       and Solar Researchers.

       VAPOR provides an interactive 3D visualization environment that can also
       produce animations and still frame images."""

    homepage = "https://www.vapor.ucar.edu/"
    url      = "https://github.com/NCAR/VAPOR/archive/3.3.0.tar.gz"

    maintainers = ['RemiLacroix-IDRIS']

    version('3.5.0', sha256='f055d488c6f5bda5174a63990b6b6600037f7ce73ac68d39ad0f371d67f2d685')
    version('3.3.0', sha256='41c13d206cfcfa4146155d524106de2eb74e7b59af1e2f8c1c3056c15d508a93')

    depends_on('glu')  # GUI
    depends_on('qt@5.13.2:+opengl+dbus')  # GUI
    depends_on('netcdf-c@4.7.0:')
    depends_on('udunits@2.2.26:')
    depends_on('freetype@2.10.1:')
    depends_on('libgeotiff@1.5.1:')
    depends_on('hdf5@1.10.5:')
    depends_on('jpeg@9c:')
    depends_on('glew@2.1.0:')  # GUI
    depends_on('assimp@4.1.0:')
    depends_on('libtiff@4.0.10:')
    depends_on('proj@6.1.1:7')
    depends_on('glm@0.9.9.1:')
    depends_on('python@3.6.9:3.6')
    depends_on('py-numpy')

    def cmake_args(self):
        with open('site.local', 'w') as f:
            python = self.spec['python']
            f.write('set (PYTHONVERSION {0})\n'.format(python.version.up_to(2)))
            f.write('set (PYTHONDIR {0})\n'.format(python.home))
            f.write('set (PYTHONPATH {0})\n'.format(python.package.platlib))
            # install expects the share/images directory to install below this path
            f.write('set (THIRD_PARTY_DIR {0})\n'.format(self.stage.source_path))
            numpy_include = join_path(
                self.spec['py-numpy'].prefix,
                self.spec['python'].package.platlib,
                'numpy', 'core', 'include')
            f.write('set (THIRD_PARTY_INC_DIR "{0}")\n'.format(numpy_include))

        args = ['-DBUILD_OSP=OFF']
        return args

    def setup_run_environment(self, env):
        # set VAPOR_HOME in the module file
        env.set('VAPOR_HOME', self.prefix)
