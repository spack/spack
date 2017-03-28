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
# License
# -------
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
#
# Legal Notice
# ------------
# OPENFOAM is a trademark owned by OpenCFD Ltd
# (producer and distributor of the OpenFOAM software via www.openfoam.com).
# The trademark information must remain visible and unadulterated in this
# file and via the "spack info" and comply with the term set by
# http://openfoam.com/legal/trademark-policy.php
#
# This file is not part of OpenFOAM, nor does it constitute a component of an
# OpenFOAM distribution.
#
##############################################################################
#
# Changes
# 2017-03-28 Mark Olesen <mark.olesen@esi-group.com>
#  - avoid installing intermediate targets.
#  - reworked to mirror the openfoam-com package.
#    If changes are needed here, consider if they need applying there too.
#
##############################################################################
from spack import *
from spack.environment import *
import llnl.util.tty as tty

import multiprocessing
import glob
import re
import shutil
import os
from os.path import isdir, isfile


def pkglib(package):
    """Get lib64 or lib from package prefix"""
    libdir = package.prefix.lib64
    if isdir(libdir):
        return libdir
    return package.prefix.lib


def format_export(key, value):
    """Format key,value pair as 'export' with newline for POSIX shell."""
    return 'export {0}={1}\n'.format(key, value)


def format_setenv(key, value):
    """Format key,value pair as 'setenv' with newline for C-shell."""
    return 'setenv {0} {1}\n'.format(key, value)


def write_environ(output, environ, formatter):
    """Write environment settings as 'export' or 'setenv' according to the
    formatter.
    If environ is a dict, write in sorted order.
    If environ is a list, write pair-wise.
    """
    used = False
    with open(output, 'w') as outfile:
        outfile.write('# SPACK settings\n\n')
        if isinstance(environ, dict):
            for key in sorted(environ):
                outfile.write(formatter(key, environ[key]))
                used = True
        elif isinstance(environ, list):
            for item in environ:
                outfile.write(formatter(item[0], item[1]))
                used = True
        if not used:
            outfile.write('# not used\n')


def rewrite_environ_files(environ, bsh, csh):
    """ Use filter_file to rewrite (existing) POSIX shell or C-shell files"""
    if isfile(bsh):
        for k, v in environ.iteritems():
            filter_file(
                r'^(\s*export\s+%s)=.*$' % k,
                r'\1=%s' % v,
                bsh,
                backup=False
            )
    if isfile(csh):
        for k, v in environ.iteritems():
            filter_file(
                r'^(\s*setenv\s+%s)\s+.*$' % k,
                r'\1 %s' % v,
                csh,
                backup=False
            )


class FoamExtend(Package):
    """The Extend Project is a fork of the OpenFOAM opensource library
    for Computational Fluid Dynamics (CFD).
    This offering is not approved or endorsed by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    """

    homepage = "http://www.extend-project.de/"

    version('4.0', git='http://git.code.sf.net/p/foam-extend/foam-extend-4.0')
    version('3.2', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.2')
    version('3.1', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.1')
    version('3.0', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.0')

    # variant('int64', default=False,
    #         description='Compile with 64-bit labels')
    variant('float32', default=False,
            description='Compile with 32-bit scalar (single-precision)')

    variant('paraview', default=False,
            description='Build paraview plugins (eg, paraFoam)')
    variant('scotch', default=True,
            description='With scotch for decomposition')
    variant('ptscotch', default=True,
            description='With ptscotch for decomposition')
    variant('metis', default=True,
            description='With metis for decomposition')
    variant('parmetis', default=True,
            description='With parmetis for decomposition')
    variant('parmgridgen', default=True,
            description='With parmgridgen support')
    variant('source', default=True,
            description='Install library/application sources and tutorials')

    supported_compilers = {'clang': 'Clang', 'gcc': 'Gcc', 'intel': 'Icc'}

    provides('openfoam')
    depends_on('mpi')
    depends_on('python')
    depends_on('zlib')
    depends_on('flex@:2.6.1')  # <- restriction due to scotch
    depends_on('cmake', type='build')

    depends_on('scotch~metis',     when='~ptscotch+scotch')
    depends_on('scotch~metis+mpi', when='+ptscotch')
    depends_on('metis@5:',         when='+metis')
    depends_on('parmetis',         when='+parmetis')
    depends_on('parmgridgen',      when='+parmgridgen')
    depends_on('paraview@:5.0.1',  when='+paraview')

    # Some user settings, to be adjusted manually or via variants
    foam_cfg = {
        'WM_COMPILER':        'Gcc',  # <- %compiler
        'WM_ARCH_OPTION':     '64',   # (32/64-bit on x86_64)
        # FUTURE? 'WM_LABEL_SIZE':      '32',  # <- +int64
        'WM_PRECISION_OPTION': 'DP',  # <- +float32
        'WM_COMPILE_OPTION':  'SPACKOpt',  # Do not change
        'WM_MPLIB':           'SPACK',     # Do not change
    }

    # The system description is frequently needed
    foam_sys = {
        'WM_ARCH':      None,
        'WM_COMPILER':  None,
        'WM_OPTIONS':   None,
    }

    build_script = './spack-Allwmake'  # <- Generated by patch() method.
    # phases = ['configure', 'build', 'install']

    def setup_environment(self, spack_env, run_env):
        run_env.set('FOAM_INST_DIR', self.prefix)
        run_env.set('WM_PROJECT_DIR', self.projectdir)

    @property
    def _canonical(self):
        """Canonical name for this package and version"""
        return 'foam-extend-{0}'.format(self.version.up_to(2))

    @property
    def projectdir(self):
        """Absolute location of project directory: WM_PROJECT_DIR/"""
        return join_path(self.prefix, self._canonical)  # <- prefix/canonical

    @property
    def etc(self):
        """Absolute location of the OpenFOAM etc/ directory"""
        return join_path(self.projectdir, 'etc')

    @property
    def archbin(self):
        """Relative location of architecture-specific executables"""
        wm_options = self.set_openfoam()
        return join_path('applications', 'bin', wm_options)

    @property
    def archlib(self):
        """Relative location of architecture-specific libraries"""
        wm_options = self.set_openfoam()
        return join_path('lib', wm_options)

    @property
    def mplib_content(self):
        """Define 'SPACK' mpi settings to have wmake
        use spack information with minimum modifications to OpenFOAM
        """
        return [
            'PFLAGS = -DOMPI_SKIP_MPICXX -DMPICH_IGNORE_CXX_SEEK',
            'PINC   = -I{0}'.format(self.spec['mpi'].prefix.include),
            'PLIBS  = -L{0} -lmpi'.format(pkglib(self.spec['mpi']))
        ]

    @property
    def rpath_info(self):
        """Define 'SPACKOpt' compiler optimization file to have wmake
        use spack information with minimum modifications to OpenFOAM
        """
        build_libpath   = join_path(self.stage.source_path, self.archlib)
        install_libpath = join_path(self.projectdir, self.archlib)

        # 'DBUG': rpaths
        return '{0}{1} {2}{3}'.format(
            self.compiler.cxx_rpath_arg, install_libpath,
            self.compiler.cxx_rpath_arg, build_libpath,
        )

    # For foam-extend: supports darwinIntel, does not yet support +int64
    def set_openfoam(self):
        """Populate foam_cfg, foam_sys according to
        variants, architecture, compiler.
        Returns WM_OPTIONS.
        """
        # Run once
        wm_options = self.foam_sys['WM_OPTIONS']
        if wm_options:
            return wm_options

        # Trivial check
        if self.compiler.name not in self.supported_compilers:
            raise RuntimeError
            (
                '{0} is an unsupported compiler'.format(self.compiler.name)
            )

        (sysname, nodename, release, version, machine) = os.uname()

        wm_arch = None
        wm_compiler = self.supported_compilers[self.compiler.name]
        if '+knl' in self.spec:
            wm_compiler += 'KNL'

        if sysname == 'Linux':
            wm_arch = 'linux'
            if wm_compiler == 'Clang':
                raise RuntimeError
                (
                    'unsupported os/compiler combination: {0} {1}'
                    .format(sysname, wm_compiler)
                )
        elif sysname == 'Darwin':
            if machine == 'x86_64':
                wm_arch = 'darwinIntel'
            if wm_compiler == 'Icc':
                raise RuntimeError
                (
                    'unsupported os/compiler combination: {0} {1}'
                    .format(sysname, wm_compiler)
                )
        else:
            raise RuntimeError
            (
                'unsupported architecture: {0} {1}'.format(sysname, machine)
            )

        if not wm_arch:
            raise RuntimeError
            (
                'unsupported os/compiler combination: {0} {1}'
                .format(sysname, wm_compiler)
            )

        if machine == 'i686':
            self.foam_cfg['WM_ARCH_OPTION'] = '32'
        elif machine == 'x86_64' and self.foam_cfg['WM_ARCH_OPTION'] == '64':
            wm_arch += '64'  # Eg, linux/darwinIntel -> linux64/darwinIntel64

        # A wmake rule must exist for this architecture/compiler combination
        archCompiler  = wm_arch + wm_compiler
        compiler_rule = join_path(
            self.stage.source_path, 'wmake', 'rules', archCompiler
        )

        if not isdir(compiler_rule):
            raise RuntimeError('No wmake rule for {0}'.format(archCompiler))

        wm_compile_option = self.foam_cfg['WM_COMPILE_OPTION']
        if not re.match(r'.+Opt$', wm_compile_option):
            raise RuntimeError(
                "WM_COMPILE_OPTION={0} is not type '*Opt'"
                .format(wm_compile_option)
            )

        self.foam_sys['WM_ARCH']     = wm_arch
        self.foam_sys['WM_COMPILER'] = wm_compiler
        self.foam_cfg['WM_COMPILER'] = wm_compiler  # For bashrc,cshrc too

        # Adjust for variants
        # FUTURE? self.foam_cfg['WM_LABEL_SIZE'] = (
        # FUTURE?     '64' if '+int64'   in self.spec else '32'
        # FUTURE? )
        self.foam_cfg['WM_PRECISION_OPTION'] = (
            'SP' if '+float32' in self.spec else 'DP'
        )

        # wmake
        # WM_OPTIONS=$WM_ARCH$WM_COMPILER$WM_PRECISION_OPTION$WM_COMPILE_OPTION
        #
        self.foam_sys['WM_OPTIONS'] = ''.join([
            wm_arch,
            wm_compiler,
            self.foam_cfg['WM_PRECISION_OPTION'],
            # FUTURE? 'Int', self.foam_cfg['WM_LABEL_SIZE'],  # Int32/Int64
            wm_compile_option
        ])
        return self.foam_sys['WM_OPTIONS']

    def patch(self):
        """Adjust OpenFOAM build for spack. Where needed, apply filter as an
        alternative to normal patching.
        """
        self.set_openfoam()  # May need foam_cfg/foam_sys information

        # Adjust ParMGridGen - this is still a mess
        files = [
            'src/dbns/Make/options',
            'src/fvAgglomerationMethods/MGridGenGamgAgglomeration/Make/options'  # noqa: E501
        ]
        for f in files:
            filter_file(r'-lMGridGen', r'-lmgrid', f, backup=False)

        # Adjust for flex version check
        files = [
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
        for f in files:
            filter_file(
                r'#if YY_FLEX_SUBMINOR_VERSION < 34',
                r'#if YY_FLEX_MAJOR_VERSION <= 2 && YY_FLEX_MINOR_VERSION <= 5 && YY_FLEX_SUBMINOR_VERSION < 34',   # noqa: E501
                f, backup=False
            )

        # Build wrapper script
        with open(self.build_script, 'w') as out:
            out.write(
                """#!/bin/bash
export FOAM_INST_DIR=$(cd .. && pwd -L)
. $PWD/etc/bashrc ''  # No arguments
mkdir -p $FOAM_APPBIN $FOAM_LIBBIN 2>/dev/null  # Allow interrupt
echo Build openfoam with SPACK
echo WM_PROJECT_DIR = $WM_PROJECT_DIR
exec ./Allwmake       # No arguments
#
""")
        set_executable(self.build_script)
        self.configure(self.spec, self.prefix)  # Should be a separate phase

    def configure(self, spec, prefix):
        """Make adjustments to the OpenFOAM configuration files in their various
        locations: etc/bashrc, etc/config.sh/FEATURE and customizations that
        don't properly fit get placed in the etc/prefs.sh file (similiarly for
        csh).
        """
        self.set_openfoam()  # Need foam_cfg/foam_sys information

        # Content for etc/prefs.{csh,sh}
        etc_prefs = {
            'compilerInstall': 'System',

            'CMAKE_DIR': spec['cmake'].prefix,
            'CMAKE_BIN_DIR': spec['cmake'].prefix.bin,

            'PYTHON_DIR': spec['python'].prefix,
            'PYTHON_BIN_DIR': spec['python'].prefix.bin,

            'FLEX_SYSTEM': 1,
            'FLEX_DIR':    spec['flex'].prefix,

            'BISON_SYSTEM': 1,
            'BISON_DIR': spec['flex'].prefix,

            'ZLIB_SYSTEM': 1,
            'ZLIB_DIR': spec['zlib'].prefix,
        }
        etc_prefs.update(self.foam_cfg)   # Add in config settings too

        if '+scotch' in spec or '+ptscotch' in spec:
            etc_prefs['SCOTCH_SYSTEM'] = 1
            etc_prefs['SCOTCH_DIR'] = spec['scotch'].prefix
            etc_prefs['SCOTCH_BIN_DIR'] = spec['scotch'].prefix.bin
            etc_prefs['SCOTCH_LIB_DIR'] = spec['scotch'].prefix.lib
            etc_prefs['SCOTCH_INCLUDE_DIR'] = spec['scotch'].prefix.include

        if '+metis' in spec:
            etc_prefs['METIS_SYSTEM'] = 1
            etc_prefs['METIS_DIR'] = spec['metis'].prefix
            etc_prefs['METIS_BIN_DIR'] = spec['metis'].prefix.bin
            etc_prefs['METIS_LIB_DIR'] = spec['metis'].prefix.lib
            etc_prefs['METIS_INCLUDE_DIR'] = spec['metis'].prefix.include

        if '+parmetis' in spec:
            etc_prefs['PARMETIS_SYSTEM'] = 1
            etc_prefs['PARMETIS_DIR'] = spec['parmetis'].prefix
            etc_prefs['PARMETIS_BIN_DIR'] = spec['parmetis'].prefix.bin
            etc_prefs['PARMETIS_LIB_DIR'] = spec['parmetis'].prefix.lib
            etc_prefs['PARMETIS_INCLUDE_DIR'] = spec['parmetis'].prefix.include

        if '+parmgridgen' in spec:
            etc_prefs['PARMGRIDGEN_SYSTEM'] = 1
            etc_prefs['PARMGRIDGEN_DIR'] = spec['parmgridgen'].prefix
            etc_prefs['PARMGRIDGEN_BIN_DIR'] = spec['parmgridgen'].prefix.bin
            etc_prefs['PARMGRIDGEN_LIB_DIR'] = spec['parmgridgen'].prefix.lib
            etc_prefs['PARMGRIDGEN_INCLUDE_DIR'] = \
                spec['parmgridgen'].prefix.include

        if '+paraview' in self.spec:
            etc_prefs['PARAVIEW_SYSTEM'] = 1
            etc_prefs['PARAVIEW_DIR'] = spec['paraview'].prefix
            etc_prefs['PARAVIEW_BIN_DIR'] = spec['paraview'].prefix.bin
            etc_prefs['QT_SYSTEM'] = 1
            etc_prefs['QT_DIR'] = spec['qt'].prefix
            etc_prefs['QT_BIN_DIR'] = spec['qt'].prefix.bin

        # Write prefs files according to the configuration.
        # Only need prefs.sh for building, but install both for end-users
        bsh = join_path('etc', 'prefs.sh')
        csh = join_path('etc', 'prefs.csh')
        write_environ(bsh, etc_prefs, format_export)
        write_environ(csh, etc_prefs, format_setenv)

        archCompiler = self.foam_sys['WM_ARCH'] + self.foam_sys['WM_COMPILER']
        compileOpt   = self.foam_cfg['WM_COMPILE_OPTION']
        mplib        = 'mplib{0}'.format(self.foam_cfg['WM_MPLIB'])

        # general_rule   = join_path('wmake', 'rules', 'General')
        compiler_rule  = join_path('wmake', 'rules', archCompiler)

        # Create wmake/rules/<archComp>/mplibSPACK
        with working_dir(compiler_rule):
            with open(mplib, 'w') as out:
                for entry in self.mplib_content:
                    out.write('{0}\n'.format(entry))

        # (src, dst) - eg, (c++Opt, c++SPACKOpt)
        file_pairs = [
            ('{0}Opt'.format(comp), '{0}{1}'.format(comp, compileOpt))
            for comp in ['c', 'c++']
        ]

        # Compiler options for SPACK - eg, wmake/rules/linux64Gcc/
        # Copy from existing cOpt, c++Opt and modify DBUG value
        with working_dir(compiler_rule):
            for item in file_pairs:
                shutil.copyfile(item[0], item[1])  # src -> dst
                filter_file(
                    r'^(\S+DBUG\s*)=.*$',
                    r'\1= %s' % self.rpath_info,
                    item[1],  # dst
                    backup=False
                )

        # Some feedback about file locations
        tty.info(join_path(self.stage.source_path, 'etc', 'bashrc'))
        if etc_prefs:
            tty.info(join_path(self.stage.source_path, 'etc', 'prefs.sh'))

    def build(self, spec, prefix):
        """Build using the OpenFOAM Allwmake script, with a wrapper to source
        its environment first.
        """
        args = []
        if self.parallel:  # Build in parallel? - pass via the environment
            os.environ['WM_NCOMPPROCS'] = str(self.make_jobs) \
                if self.make_jobs else str(multiprocessing.cpu_count())
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the projectdir (== prefix/name-version)"""
        self.build(spec, prefix)  # Should be a separate phase
        wm_options = self.set_openfoam()

        # Fairly ugly since intermediate targets are scattered inside sources
        appdir = 'applications'
        mkdirp(self.projectdir, join_path(self.projectdir, appdir))

        # All top-level files, except spack build info and possibly Allwmake
        if '+source' in spec:
            ignored = re.compile(r'^spack-.*')
        else:
            ignored = re.compile(r'^(Allclean|Allwmake|spack-).*')

        files = [
            f for f in glob.glob("*") if isfile(f) and not ignored.search(f)
        ]
        for f in files:
            install(f, self.projectdir)

        # Install directories. install applications/bin directly
        for d in ['bin', 'etc', 'wmake', 'lib', join_path(appdir, 'bin')]:
            install_tree(
                d,
                join_path(self.projectdir, d)
            )

        if '+source' in spec:
            subitem = join_path(appdir, 'Allwmake')
            install(subitem, join_path(self.projectdir, subitem))

            ignored = [wm_options]

            for d in ['src', 'tutorials']:
                install_tree(
                    d,
                    join_path(self.projectdir, d),
                    ignore=shutil.ignore_patterns(*ignored)
                )

            for d in ['solvers', 'utilities']:
                install_tree(
                    join_path(appdir, d),
                    join_path(self.projectdir, appdir, d),
                    ignore=shutil.ignore_patterns(*ignored)
                )

    def install_links(self):
        """Add symlinks into bin/, lib/ (eg, for other applications)"""
        return

# -----------------------------------------------------------------------------
