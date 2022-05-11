# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.util.package import *


class Alpgen(MakefilePackage):
    """A collection of codes for the generation of
       multi-parton processes in hadronic collisions."""

    homepage = "http://mlm.home.cern.ch/mlm/alpgen/"
    url      = "http://mlm.home.cern.ch/mlm/alpgen/V2.1/v214.tgz"

    maintainers = ['iarspider']
    tags = ['hep']

    patch('alpgen-214.patch', when='recipe=cms')
    patch('alpgen-214-Darwin-x86_84-gfortran.patch', when='platform=darwin recipe=cms')
    patch('alpgen-2.1.4-sft.patch', when='recipe=sft', level=0)

    depends_on('cmake', type='build', when='recipe=sft')

    variant('recipe', values=('cms', 'sft'), default='sft',
            description='Select build recipe: CMS for CMS experiment, ' +
                        'SFT for ATLAS/LHCb/others.')

    version('2.1.4', sha256='2f43f7f526793fe5f81a3a3e1adeffe21b653a7f5851efc599ed69ea13985c5e')

    phases = ['cmake', 'build', 'install']

    # copied from CMakePackage
    @property
    def build_dirname(self):
        """Returns the directory name to use when building the package

        :return: name of the subdirectory for building the package
        """
        return 'spack-build-%s' % self.spec.dag_hash(7)

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return os.path.join(self.stage.path, self.build_dirname)

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return self.stage.source_path

    def cmake_args(self):
        """Produces a list containing all the arguments that must be passed to
        cmake, except:

            * CMAKE_INSTALL_PREFIX
            * CMAKE_BUILD_TYPE

        which will be set automatically.

        :return: list of arguments for cmake
        """
        return []

    @property
    def std_cmake_args(self):
        """Standard cmake arguments provided as a property for
        convenience of package writers

        :return: standard cmake arguments
        """
        # standard CMake arguments
        std_cmake_args = CMakePackage._std_args(self)
        std_cmake_args += getattr(self, 'cmake_flag_args', [])
        return std_cmake_args

    # end

    def url_for_version(self, version):
        root = self.url.rsplit('/', 2)[0]
        return "{0}/V{1}/v{2}.tgz".format(root, version.up_to(2), version.joined)

    def patch(self):
        if self.spec.satisfies('recipe=sft'):
            copy(join_path(os.path.dirname(__file__), 'CMakeLists.txt'),
                 'CMakeLists.txt')

        if self.spec.satisfies('recipe=cms'):
            filter_file('-fno-automatic', '-fno-automatic -std=legacy', 'compile.mk')
            copy(join_path(os.path.dirname(__file__), 'cms_build.sh'), 'cms_build.sh')
            copy(join_path(os.path.dirname(__file__), 'cms_install.sh'),
                 'cms_install.sh')

    @when('recipe=cms')
    def cmake(self, spec, prefix):
        return

    @when('recipe=cms')
    def build(self, spec, prefix):
        bash = which('bash')
        bash('./cms_build.sh')

    @when('recipe=cms')
    def install(self, spec, prefix):
        bash = which('bash')
        bash('./cms_install.sh', prefix)

        for root, dirs, files in os.walk(prefix):
            set_install_permissions(root)
            for file in files:
                set_install_permissions(join_path(root, file))

    @when('recipe=sft')
    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory"""
        options = self.std_cmake_args
        options += self.cmake_args()
        options.append(os.path.abspath(self.root_cmakelists_dir))
        with working_dir(self.build_directory, create=True):
            cmake_x = which('cmake')
            cmake_x(*options)

    @when('recipe=sft')
    def build(self, spec, prefix):
        """Make the build targets"""
        with working_dir(self.build_directory):
            make()

    @when('recipe=sft')
    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            make('install')
