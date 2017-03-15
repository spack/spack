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
from spack.environment import *

import multiprocessing
import os


class FoamExtend(Package):
    """The foam-extend project is a fork of the OpenFOAM open source library
      for Computational Fluid Dynamics (CFD)."""

    homepage = "http://www.extend-project.de/"

    version('4.0', git='http://git.code.sf.net/p/foam-extend/foam-extend-4.0')
    version('3.2', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.2')
    version('3.1', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.1')
    version('3.0', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.0')

    variant('paraview', default=False, description='Enable ParaFOAM')
    variant(
        'scotch', default=True,
        description='Activate Scotch as a possible decomposition library')
    variant(
        'ptscotch', default=True,
        description='Activate PT-Scotch as a possible decomposition library')
    variant(
        'metis', default=True,
        description='Activate Metis as a possible decomposition library')
    variant(
        'parmetis', default=True,
        description='Activate Parmetis as a possible decomposition library')
    variant(
        'parmgridgen', default=True,
        description='Activate Parmgridgen support')
    variant(
        'source', default=True,
        description='Installs also the source folder')

    supported_compilers = {'clang': 'Clang', 'gcc': 'Gcc', 'intel': 'Icc'}

    depends_on('mpi')
    depends_on('python')
    depends_on('flex')
    depends_on('zlib')
    depends_on('cmake', type='build')

    depends_on('scotch ~ metis', when='~ptscotch+scotch')
    depends_on('scotch ~ metis + mpi', when='+ptscotch')
    depends_on('metis@5:', when='+metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('parmgridgen', when='+parmgridgen')

    depends_on('paraview', when='+paraview')

    def set_arch(self):
        (sysname, nodename, release, version, machine) = os.uname()

        if self.compiler.name not in self.supported_compilers:
            raise RuntimeError('{0} is not a supported compiler \
            to compile OpenFOAM'.format(self.compiler.name))

        foam_compiler = self.supported_compilers[self.compiler.name]
        if sysname == 'Linux':
            arch = 'linux'
            if foam_compiler == 'Clang':
                raise RuntimeError('OS, compiler combination not\
                supported ({0} {1})'.format(sysname, foam_compiler))
        elif sysname == 'Darwin':
            if machine == 'x86_64':
                arch = 'darwinIntel'
            if foam_compiler == 'Icc':
                raise RuntimeError('OS, compiler combination not\
                supported ({0} {1})'.format(sysname, foam_compiler))
        else:
            raise RuntimeError('{0} {1} is not a \
            supported architecture'.format(sysname, machine))

        return (arch, foam_compiler)

    def get_openfoam_environment(self):
        return EnvironmentModifications.from_sourcing_files(
            join_path(self.stage.source_path,
                      'etc/bashrc'))

    def patch(self):
        # change names to match the package and not the one patch in
        # the Third-Party of foam-extend
        if '+parmgridgen' in self.spec:
            filter_file(r'-lMGridGen',
                        r'-lmgrid',
                        'src/dbns/Make/options')

            filter_file(
                r'-lMGridGen',
                r'-lmgrid',
                'src/fvAgglomerationMethods/MGridGenGamgAgglomeration/Make/options')  # noqa: E501

        # Get the wmake arch and compiler
        (arch, foam_compiler) = self.set_arch()

        prefs_dict = {
            'compilerInstall': 'System',
            'WM_COMPILER': foam_compiler,
            'WM_ARCH_OPTION': '64',
            'WM_PRECISION_OPTION': 'DP',
            'WM_COMPILE_OPTION': 'SPACKOpt',
            'WM_MPLIB': 'SPACK',

            'CMAKE_DIR': self.spec['cmake'].prefix,
            'CMAKE_BIN_DIR': self.spec['cmake'].prefix.bin,
            'PYTHON_DIR': self.spec['python'].prefix,
            'PYTHON_BIN_DIR': self.spec['python'].prefix.bin,

            'FLEX_SYSTEM': 1,
            'FLEX_DIR': self.spec['flex'].prefix,

            'BISON_SYSTEM': 1,
            'BISON_DIR': self.spec['flex'].prefix,

            'ZLIB_SYSTEM': 1,
            'ZLIB_DIR': self.spec['zlib'].prefix,
        }

        if '+scotch' in self.spec or '+ptscotch' in self.spec:
            prefs_dict['SCOTCH_SYSTEM'] = 1
            prefs_dict['SCOTCH_DIR'] = self.spec['scotch'].prefix
            prefs_dict['SCOTCH_BIN_DIR'] = self.spec['scotch'].prefix.bin
            prefs_dict['SCOTCH_LIB_DIR'] = self.spec['scotch'].prefix.lib
            prefs_dict['SCOTCH_INCLUDE_DIR'] = \
                self.spec['scotch'].prefix.include

        if '+metis' in self.spec:
            prefs_dict['METIS_SYSTEM'] = 1
            prefs_dict['METIS_DIR'] = self.spec['metis'].prefix
            prefs_dict['METIS_BIN_DIR'] = self.spec['metis'].prefix.bin
            prefs_dict['METIS_LIB_DIR'] = self.spec['metis'].prefix.lib
            prefs_dict['METIS_INCLUDE_DIR'] = self.spec['metis'].prefix.include

        if '+parmetis' in self.spec:
            prefs_dict['PARMETIS_SYSTEM'] = 1
            prefs_dict['PARMETIS_DIR'] = self.spec['parmetis'].prefix
            prefs_dict['PARMETIS_BIN_DIR'] = self.spec['parmetis'].prefix.bin
            prefs_dict['PARMETIS_LIB_DIR'] = self.spec['parmetis'].prefix.lib
            prefs_dict['PARMETIS_INCLUDE_DIR'] = \
                self.spec['parmetis'].prefix.include

        if '+parmgridgen' in self.spec:
            prefs_dict['PARMGRIDGEN_SYSTEM'] = 1
            prefs_dict['PARMGRIDGEN_DIR'] = self.spec['parmgridgen'].prefix
            prefs_dict['PARMGRIDGEN_BIN_DIR'] = \
                self.spec['parmgridgen'].prefix.bin
            prefs_dict['PARMGRIDGEN_LIB_DIR'] = \
                self.spec['parmgridgen'].prefix.lib
            prefs_dict['PARMGRIDGEN_INCLUDE_DIR'] = \
                self.spec['parmgridgen'].prefix.include

        if '+paraview' in self.spec:
            prefs_dict['PARAVIEW_SYSTEM'] = 1
            prefs_dict['PARAVIEW_DIR'] = self.spec['paraview'].prefix
            prefs_dict['PARAVIEW_BIN_DIR'] = self.spec['paraview'].prefix.bin
            prefs_dict['QT_SYSTEM'] = 1
            prefs_dict['QT_DIR'] = self.spec['qt'].prefix
            prefs_dict['QT_BIN_DIR'] = self.spec['qt'].prefix.bin

        # write the prefs files to define the configuration needed,
        # only the prefs.sh is used by this script but both are
        # installed for end users
        with working_dir('.'):
            with open("etc/prefs.sh", "w") as fh:
                for key in sorted(prefs_dict):
                    fh.write('export {0}={1}\n'.format(key, prefs_dict[key]))

            with open("etc/prefs.csh", "w") as fh:
                for key in sorted(prefs_dict):
                    fh.write('setenv {0}={1}\n'.format(key, prefs_dict[key]))

        # Defining a different mpi and optimisation file to be able to
        # make wmake get spack info with minimum modifications on
        # configurations scripts
        mpi_info = [
            'PFLAGS = -DOMPI_SKIP_MPICXX -DMPICH_IGNORE_CXX_SEEK',
            'PINC = -I{0}'.format(self.spec['mpi'].prefix.include),
            'PLIBS = -L{0} -lmpi'.format(self.spec['mpi'].prefix.lib)
        ]

        arch_path = ''.join([arch, prefs_dict['WM_ARCH_OPTION'],
                             foam_compiler])
        option_path = ''.join([arch_path,
                               prefs_dict['WM_PRECISION_OPTION'],
                               prefs_dict['WM_COMPILE_OPTION']])
        rule_path = join_path("wmake", "rules", arch_path)
        build_path = join_path(self.stage.source_path, 'lib', option_path)
        install_path = \
            join_path(self.prefix,
                      'foam-extend-{0}'.format(self.version.up_to(2)),
                      option_path)

        rpaths_foam = ' '.join([
            '{0}{1}'.format(self.compiler.cxx_rpath_arg,
                            install_path),
            '{0}{1}'.format(self.compiler.cxx_rpath_arg,
                            build_path)
        ])

        compiler_flags = {
            'DBUG': rpaths_foam,
            'OPT': '-O3',
        }

        with working_dir(rule_path):
            with open('mplibSPACK', "w") as fh:
                fh.write('\n'.join(mpi_info))

            for comp in ['c', 'c++']:
                with open('{0}SPACKOpt'.format(comp), "w") as fh:
                    for key, val in compiler_flags.iteritems():
                        fh.write('{0}{1} = {2}\n'.format(comp, key, val))

        _files_to_patch = [
            'src/thermophysicalModels/reactionThermo/chemistryReaders/chemkinReader/chemkinLexer.L',  # noqa: E501
            'src/surfMesh/surfaceFormats/stl/STLsurfaceFormatASCII.L',  # noqa: E501
            'src/meshTools/triSurface/triSurface/interfaces/STL/readSTLASCII.L',  # noqa: E501
            'applications/utilities/preProcessing/fluentDataToFoam/fluentDataToFoam.L',  # noqa: E501
            'applications/utilities/mesh/conversion/gambitToFoam/gambitToFoam.L',  # noqa: E501
            'applications/utilities/mesh/conversion/fluent3DMeshToFoam/fluent3DMeshToFoam.L',  # noqa: E501
            'applications/utilities/mesh/conversion/ansysToFoam/ansysToFoam.L',  # noqa: E501
            'applications/utilities/mesh/conversion/fluentMeshToFoam/fluentMeshToFoam.L',  # noqa: E501
            'applications/utilities/mesh/conversion/fluent3DMeshToElmer/fluent3DMeshToElmer.L'  # noqa: E501
        ]
        for _file in _files_to_patch:
            filter_file(r'#if YY_FLEX_SUBMINOR_VERSION < 34',
                        r'#if YY_FLEX_MAJOR_VERSION <= 2 && YY_FLEX_MINOR_VERSION <= 5 && YY_FLEX_SUBMINOR_VERSION < 34',   # noqa: E501
                        _file)

    def setup_environment(self, spack_env, run_env):
        with working_dir(self.stage.path):
            spack_env.set('FOAM_INST_DIR', os.path.abspath('.'))

        (arch, foam_compiler) = self.set_arch()

        run_env.set('FOAM_INST_DIR', self.prefix)

    def install(self, spec, prefix):
        env_openfoam = self.get_openfoam_environment()
        env_openfoam.apply_modifications()

        if self.parallel:
            os.environ['WM_NCOMPPROCS'] = str(self.make_jobs) \
                if self.make_jobs else str(multiprocessing.cpu_count())

        allwmake = Executable('./Allwmake')
        allwmake()

        install_path = \
            join_path(self.prefix,
                      'foam-extend-{0}'.format(self.version.up_to(2)))

        if '+source' in spec:
            install_tree('src', join_path(install_path, 'src'))
            install_tree('tutorials', join_path(install_path, 'tutorials'))

        install_tree('lib', join_path(install_path, 'lib'))
        install_tree('bin', join_path(install_path, 'bin'))
        install_tree('applications', join_path(install_path, 'applications'))
        install_tree('etc', join_path(install_path, 'etc'))
        install_tree('wmake', join_path(install_path, 'wmake'))
