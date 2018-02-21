##############################################################################
# Copyright (c) 2018 Simone Bna, CINECA.
#
# This file was authored by Simone Bna <simone.bna@cineca.it>
# and is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for the LLNL notice and LGPL.
#
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
import os
import subprocess
import llnl.util.tty as tty


class Catalyst(CMakePackage):
    """Catalyst is an in situ use case library, with an adaptable application
    programming interface (API), that orchestrates the alliance between
    simulation and analysis and/or visualization tasks."""

    homepage = 'http://www.paraview.org'
    url      = "http://www.paraview.org/files/v5.4/ParaView-v5.4.1.tar.gz"
    _urlfmt  = 'http://www.paraview.org/files/v{0}/ParaView-v{1}{2}.tar.gz'

    version('5.4.1', '4030c70477ec5a85aa72d6fc86a30753')
    version('5.4.0', 'b92847605bac9036414b644f33cb7163')
    version('5.3.0', '68fbbbe733aa607ec13d1db1ab5eba71')
    version('5.2.0', '4570d1a2a183026adb65b73c7125b8b0')
    version('5.1.2', '44fb32fc8988fcdfbc216c9e40c3e925')
    version('5.0.1', 'fdf206113369746e2276b95b257d2c9b')
    version('4.4.0', 'fa1569857dd680ebb4d7ff89c2227378')

    variant('python', default=False, description='Enable Python support')
    variant('essentials', default=False, description='Enable Essentials support')
    variant('extras', default=False, description='Enable Extras support')
    variant('rendering', default=False, description='Enable Vtk Rendering support')

    depends_on('git')
    depends_on('mpi')
    depends_on('python@2:2.8', when='+python')
    depends_on('mesa', when='+rendering')
    depends_on("libx11", when='+rendering')
    depends_on("libxt", when='+rendering')
    depends_on('cmake@3.3:', type='build')

    def url_for_version(self, version):
        """Handle ParaView version-based custom URLs."""
        if version < Version('5.1.0'):
            return self._urlfmt.format(version.up_to(2), version, '-source')
        else:
            return self._urlfmt.format(version.up_to(2), version, '')

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball.
        Then, generate the catalyst source files."""
        super(Catalyst, self).do_stage(mirror_only)

        # extract the catalyst part
        paraview_dir = os.path.join(self.stage.path,
                                    'ParaView-v' + str(self.version))
        catalyst_script = os.path.join(paraview_dir, 'Catalyst', 'catalyze.py')
        catalyst_source_dir = os.path.abspath(self.root_cmakelists_dir)

        command = ['python', catalyst_script,
                   '-r', paraview_dir]

        catalyst_edition = os.path.join(paraview_dir, 'Catalyst',
                                        'Editions', 'Base')
        command.append('-i')
        command.append(catalyst_edition)
        if '+python' in self.spec:
            catalyst_edition = os.path.join(paraview_dir, 'Catalyst',
                                            'Editions', 'Enable-Python')
            command.append('-i')
            command.append(catalyst_edition)
        if '+essentials' in self.spec:
            catalyst_edition = os.path.join(paraview_dir, 'Catalyst',
                                            'Editions', 'Essentials')
            command.append('-i')
            command.append(catalyst_edition)
        if '+extras' in self.spec:
            catalyst_edition = os.path.join(paraview_dir, 'Catalyst',
                                            'Editions', 'Extras')
            command.append('-i')
            command.append(catalyst_edition)
        if '+rendering' in self.spec:
            catalyst_edition = os.path.join(paraview_dir, 'Catalyst',
                                            'Editions', 'Rendering-Base')
            command.append('-i')
            command.append(catalyst_edition)

        command.append('-o')
        command.append(catalyst_source_dir)

        if not os.path.isdir(catalyst_source_dir):
            os.mkdir(catalyst_source_dir)
            subprocess.check_call(command)
            tty.msg("Generated catalyst source in %s" % self.stage.path)
        else:
            tty.msg("Already generated %s in %s" % (self.name,
                                                    self.stage.path))

    def setup_environment(self, spack_env, run_env):
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib
        paraview_version = 'paraview-%s' % self.spec.version.up_to(2)
        run_env.prepend_path('LIBRARY_PATH', join_path(lib_dir,
                             paraview_version))
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(lib_dir,
                             paraview_version))

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return os.path.join(self.stage.path, 'Catalyst-v' + str(self.version))

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return join_path(os.path.abspath(self.root_cmakelists_dir),
                         'spack-build')

    def cmake_args(self):
        """Populate cmake arguments for Catalyst."""
        cmake_args = [
            '-DPARAVIEW_GIT_DESCRIBE=v%s' % str(self.version)
        ]
        return cmake_args

    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory through the cmake.sh script"""
        cmake_script_path = os.path.join(
            os.path.abspath(self.root_cmakelists_dir),
            'cmake.sh')
        with working_dir(self.build_directory, create=True):
            subprocess.check_call([cmake_script_path,
                                   os.path.abspath(self.root_cmakelists_dir)] +
                                  self.cmake_args() + self.std_cmake_args)
