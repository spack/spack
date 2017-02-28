##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class AdolC(AutotoolsPackage):
    """A package for the automatic differentiation of first and higher
    derivatives of vector functions in C and C++ programs by operator
    overloading."""
    homepage = "https://projects.coin-or.org/ADOL-C"
    url      = "http://www.coin-or.org/download/source/ADOL-C/ADOL-C-2.6.1.tgz"

    version('develop',  git='https://gitlab.com/adol-c/adol-c.git',
            branch='master')
    version('2.6.2', '0f9547584c99c0673e4f81cf64e8d865')
    version('2.6.1', '1032b28427d6e399af4610e78c0f087b')

    variant('advanced_branching', default=False,
            description='Enable advanced branching to reduce retaping')
    variant('atrig_erf', default=True,
            description='Enable arc-trig and error functions')
    variant('doc',      default=True,  description='Install documentation')
    variant('openmp',   default=False, description='Enable OpenMP support')
    variant('sparse',   default=False, description='Enable sparse drivers')
    variant('tests',    default=True,
            description='Build all included examples as a test case')

    # Build dependencies
    depends_on('automake', type='build', when='@develop')
    depends_on('autoconf', type='build', when='@develop')
    depends_on('libtool',  type='build', when='@develop')
    depends_on('m4',       type='build', when='@develop')

    patch('openmp_exam_261.patch', when='@2.6.1')

    def configure_args(self):
        spec = self.spec

        configure_args = []

        if '+advanced_branching' in spec:
            configure_args.extend([
                '--enable-advanced-branching'
            ])

        if '+atrig_erf' in spec:
            configure_args.extend([
                '--enable-atrig-erf'
            ])

        if '+openmp' in spec:
            configure_args.extend([
                '--with-openmp-flag={0}'.format(self.compiler.openmp_flag)
            ])

        if '+sparse' in spec:
            configure_args.extend([
                '--enable-sparse'
            ])

        # We can simply use the bundled examples to check
        # whether Adol-C works as expected
        if '+tests' in spec:
            configure_args.extend([
                '--enable-docexa',  # Documented examples
                '--enable-addexa'  # Additional examples
            ])
            if '+openmp' in spec:
                configure_args.extend([
                    '--enable-parexa'  # Parallel examples
                ])

        return configure_args

    @run_after('install')
    def install_additional_files(self):
        spec = self.spec
        prefix = self.prefix

        # Copy the config.h file, as some packages might require it
        source_directory = self.stage.source_path
        config_h = join_path(source_directory, 'ADOL-C', 'src', 'config.h')
        install(config_h, join_path(prefix.include, 'adolc'))

        # Install documentation to {prefix}/share
        if '+doc' in spec:
            install_tree(join_path('ADOL-C', 'doc'),
                         join_path(prefix.share, 'doc'))

        # Install examples to {prefix}/share
        if '+tests' in spec:
            install_tree(join_path('ADOL-C', 'examples'),
                         join_path(prefix.share, 'examples'))

            # Run some examples that don't require user input
            # TODO: Check that bundled examples produce the correct results
            with working_dir(join_path(
                    source_directory, 'ADOL-C', 'examples')):
                Executable('./tapeless_scalar')()
                Executable('./tapeless_vector')()

            with working_dir(join_path(
                    source_directory,
                    'ADOL-C', 'examples', 'additional_examples')):
                Executable('./checkpointing/checkpointing')()

            if '+openmp' in spec:
                with working_dir(join_path(
                        source_directory,
                        'ADOL-C', 'examples', 'additional_examples')):
                    Executable('./checkpointing/checkpointing')()
