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

import inspect
import os
import platform

import spack.build_environment
from llnl.util.filesystem import working_dir
from spack.util.environment import filter_system_paths
from spack.directives import depends_on, variant
from spack.package import PackageBase, InstallError, run_after


class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake

    For more information on the CMake build system, see:
    https://cmake.org/cmake/help/latest/

    This class provides three phases that can be overridden:

        1. :py:meth:`~.CMakePackage.cmake`
        2. :py:meth:`~.CMakePackage.build`
        3. :py:meth:`~.CMakePackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.CMakePackage.cmake_args`.
    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:meth:`~.CMakePackage.root_cmakelists_dir` | Location of the    |
        |                                               | root CMakeLists.txt|
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.CMakePackage.build_directory`     | Directory where to |
        |                                               | build the package  |
        +-----------------------------------------------+--------------------+


    """
    #: Phases of a CMake package
    phases = ['cmake', 'build', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'CMakePackage'

    build_targets = []
    install_targets = ['install']

    build_time_test_callbacks = ['check']

    #: The build system generator to use.
    #:
    #: See ``cmake --help`` for a list of valid generators.
    #: Currently, "Unix Makefiles" and "Ninja" are the only generators
    #: that Spack supports. Defaults to "Unix Makefiles".
    #:
    #: See https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html
    #: for more information.
    generator = 'Unix Makefiles'

    # https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html
    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    depends_on('cmake', type='build')

    @property
    def archive_files(self):
        """Files to archive for packages based on CMake"""
        return [os.path.join(self.build_directory, 'CMakeCache.txt')]

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return self.stage.source_path

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

    @staticmethod
    def _std_args(pkg):
        """Computes the standard cmake arguments for a generic package"""
        try:
            generator = pkg.generator
        except AttributeError:
            generator = 'Unix Makefiles'

        # Make sure a valid generator was chosen
        valid_generators = ['Unix Makefiles', 'Ninja']
        if generator not in valid_generators:
            msg  = "Invalid CMake generator: '{0}'\n".format(generator)
            msg += "CMakePackage currently supports the following "
            msg += "generators: '{0}'".format("', '".join(valid_generators))
            raise InstallError(msg)

        try:
            build_type = pkg.spec.variants['build_type'].value
        except KeyError:
            build_type = 'RelWithDebInfo'

        args = [
            '-G', generator,
            '-DCMAKE_INSTALL_PREFIX:PATH={0}'.format(pkg.prefix),
            '-DCMAKE_BUILD_TYPE:STRING={0}'.format(build_type),
            '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON'
        ]

        if platform.mac_ver()[0]:
            args.extend([
                '-DCMAKE_FIND_FRAMEWORK:STRING=LAST',
                '-DCMAKE_FIND_APPBUNDLE:STRING=LAST'
            ])

        # Set up CMake rpath
        args.append('-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=FALSE')
        rpaths = ';'.join(spack.build_environment.get_rpaths(pkg))
        args.append('-DCMAKE_INSTALL_RPATH:STRING={0}'.format(rpaths))
        # CMake's find_package() looks in CMAKE_PREFIX_PATH first, help CMake
        # to find immediate link dependencies in right places:
        deps = [d.prefix for d in
                pkg.spec.dependencies(deptype=('build', 'link'))]
        deps = filter_system_paths(deps)
        args.append('-DCMAKE_PREFIX_PATH:STRING={0}'.format(';'.join(deps)))
        return args

    def flags_to_build_system_args(self, flags):
        """Produces a list of all command line arguments to pass the specified
        compiler flags to cmake. Note CMAKE does not have a cppflags option,
        so cppflags will be added to cflags, cxxflags, and fflags to mimic the
        behavior in other tools."""
        # Has to be dynamic attribute due to caching
        setattr(self, 'cmake_flag_args', [])

        flag_string = '-DCMAKE_{0}_FLAGS={1}'
        langs = {'C': 'c', 'CXX': 'cxx', 'Fortran': 'f'}

        # Handle language compiler flags
        for lang, pre in langs.items():
            flag = pre + 'flags'
            # cmake has no explicit cppflags support -> add it to all langs
            lang_flags = ' '.join(flags.get(flag, []) + flags.get('cppflags',
                                                                  []))
            if lang_flags:
                self.cmake_flag_args.append(flag_string.format(lang,
                                                               lang_flags))

        # Cmake has different linker arguments for different build types.
        # We specify for each of them.
        if flags['ldflags']:
            ldflags = ' '.join(flags['ldflags'])
            ld_string = '-DCMAKE_{0}_LINKER_FLAGS={1}'
            # cmake has separate linker arguments for types of builds.
            for type in ['EXE', 'MODULE', 'SHARED', 'STATIC']:
                self.cmake_flag_args.append(ld_string.format(type, ldflags))

        # CMake has libs options separated by language. Apply ours to each.
        if flags['ldlibs']:
            libs_flags = ' '.join(flags['ldlibs'])
            libs_string = '-DCMAKE_{0}_STANDARD_LIBRARIES={1}'
            for lang in langs:
                self.cmake_flag_args.append(libs_string.format(lang,
                                                               libs_flags))

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return os.path.join(self.stage.source_path, 'spack-build')

    def cmake_args(self):
        """Produces a list containing all the arguments that must be passed to
        cmake, except:

            * CMAKE_INSTALL_PREFIX
            * CMAKE_BUILD_TYPE

        which will be set automatically.

        :return: list of arguments for cmake
        """
        return []

    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory"""
        options = [os.path.abspath(self.root_cmakelists_dir)]
        options += self.std_cmake_args
        options += self.cmake_args()
        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).cmake(*options)

    def build(self, spec, prefix):
        """Make the build targets"""
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                inspect.getmodule(self).make(*self.build_targets)
            elif self.generator == 'Ninja':
                inspect.getmodule(self).ninja(*self.build_targets)

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                inspect.getmodule(self).make(*self.install_targets)
            elif self.generator == 'Ninja':
                inspect.getmodule(self).ninja(*self.install_targets)

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Searches the CMake-generated Makefile for the target ``test``
        and runs it if found.
        """
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                self._if_make_target_execute('test')
                self._if_make_target_execute('check')
            elif self.generator == 'Ninja':
                self._if_ninja_target_execute('test')
                self._if_ninja_target_execute('check')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
