# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MofemFractureModule(CMakePackage):
    """mofem fracture module"""

    homepage = "http://mofem.eng.gla.ac.uk"
    git = "https://bitbucket.org/likask/mofem_um_fracture_mechanics.git"

    maintainers = ['likask']

    version('develop', branch='develop')
    version('0.9.42', tag='v0.9.42')

    variant('copy_user_modules', default=True,
        description='Copy user modules directory instead linking')

    extends('mofem-cephas')
    depends_on("mofem-users-modules", type=('build', 'link', 'run'))

    # The CMakeLists.txt installed with mofem-cephas package set cmake
    # environment to install extension from extension repository. It searches
    # for modules in user provides paths, for example in Spack source path.Also
    # it finds all cmake exported targets installed in lib directory, which are
    # built with dependent extensions, f.e.mofem - users - modules or others if
    # needed.
    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        spec = self.spec
        return spec['mofem-cephas'].prefix.users_modules

    def cmake_args(self):
        spec = self.spec
        source = self.stage.source_path

        options = []

        # obligatory options
        options.extend([
            '-DWITH_SPACK=YES',
            '-DEXTERNAL_MODULES_BUILD=YES',
            '-DUM_INSTALL_BREFIX=%s' % spec['mofem-users-modules'].prefix,
            '-DEXTERNAL_MODULE_SOURCE_DIRS=%s' % source,
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO')])

        # Set module version
        if self.spec.version == Version('develop'):
            options.extend([
                '-DFM_VERSION_MAJOR=%s' % 0,
                '-DFM_VERSION_MINOR=%s' % 0,
                '-DFM_VERSION_BUILD=%s' % 0])
        else:
            options.extend([
                '-DFM_VERSION_MAJOR=%s' % self.spec.version[0],
                '-DFM_VERSION_MINOR=%s' % self.spec.version[1],
                '-DFM_VERSION_BUILD=%s' % self.spec.version[2]])

        # build tests
        options.append('-DMOFEM_UM_BUILD_TETS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        return options

    # This function is not needed to run code installed by extension, nor in
    # the install process. However for users like to have access to source code
    # to play and make with it. Having source code at hand one can compile in
    # own build directory it in mofem-cephas view when the extension is
    # activated.
    @run_after('install')
    def copy_source_code(self):
        source = self.stage.source_path
        prefix = self.prefix
        install_tree(source, prefix.ext_users_modules.fracture_mechanics)
