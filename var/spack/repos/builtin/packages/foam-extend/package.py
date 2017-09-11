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
# Notes
# - mpi handling: WM_MPLIB=USER and provide wmake rules for special purpose
#   'USER and 'USERMPI' mpi implementations.
#   The choice of 'USER' vs 'USERMPI' may change in the future.
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

import multiprocessing
import glob
import re
import shutil
import os
from os.path import isdir, isfile
from spack.pkg.builtin.openfoam_com import *


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

    #: Map spack compiler names to OpenFOAM compiler names
    #  By default, simply capitalize the first letter
    compiler_mapping = {'intel': 'icc'}

    provides('openfoam')
    depends_on('mpi')
    depends_on('python')
    depends_on('zlib')
    depends_on('flex@:2.6.1')  # <- restriction due to scotch
    depends_on('cmake', type='build')
    depends_on('binutils', type='build')

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
        'WM_COMPILE_OPTION':  'SPACKOpt',   # Do not change
        'WM_MPLIB':           'USER',       # USER | USERMPI
    }

    # The system description is frequently needed
    foam_sys = {
        'WM_ARCH':      None,
        'WM_COMPILER':  None,
        'WM_OPTIONS':   None,
    }

    # Content for etc/prefs.{csh,sh}
    etc_prefs = {}

    # Content for etc/config.{csh,sh}/ files
    etc_config = {}

    build_script = './spack-Allwmake'  # <- Generated by patch() method.
    # phases = ['configure', 'build', 'install']
    # build_system_class = 'OpenfoamCom'

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
    def wm_options(self):
        """The architecture+compiler+options for OpenFOAM"""
        opts = self.set_openfoam()
        return opts

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
            self.compiler.cxx_rpath_arg, build_libpath)

    def openfoam_arch(self):
        """Return an architecture value similar to what OpenFOAM does in
        etc/config.sh/settings, but slightly more generous.
        Uses and may adjust foam_cfg[WM_ARCH_OPTION] as a side-effect
        """
        # spec.architecture.platform is like `uname -s`, but lower-case
        platform = self.spec.architecture.platform

        # spec.architecture.target is like `uname -m`
        target   = self.spec.architecture.target

        # \WARNING this is a ugly hack for our specific configuration at SCITAS
        target = 'x86_64'

        if platform == 'linux':
            if target == 'i686':
                self.foam_cfg['WM_ARCH_OPTION'] = '32'  # Force consistency
            elif target == 'x86_64':
                if self.foam_cfg['WM_ARCH_OPTION'] == '64':
                    platform += '64'
            elif target == 'ia64':
                platform += 'ia64'
            elif target == 'armv7l':
                platform += 'ARM7'
            elif target == 'ppc64':
                platform += 'PPC64'
            elif target == 'ppc64le':
                platform += 'PPC64le'
        elif platform == 'darwin':
            if target == 'x86_64':
                platform += 'Intel'
                if self.foam_cfg['WM_ARCH_OPTION'] == '64':
                    platform += '64'
        # ... and others?
        return platform

    def openfoam_compiler(self):
        """Capitalized version of the compiler name, which usually corresponds
        to how OpenFOAM will camel-case things.
        Use compiler_mapping to handing special cases.
        Also handle special compiler options (eg, KNL)
        """
        comp = self.compiler.name
        if comp in self.compiler_mapping:
            comp = self.compiler_mapping[comp]
        comp = comp.capitalize()

        if '+knl' in self.spec:
            comp += 'KNL'
        return comp

    # For foam-extend: does not yet support +int64
    def set_openfoam(self):
        """Populate foam_cfg, foam_sys according to
        variants, architecture, compiler.
        Returns WM_OPTIONS.
        """
        # Run once
        opts = self.foam_sys['WM_OPTIONS']
        if opts:
            return opts

        wm_arch     = self.openfoam_arch()
        wm_compiler = self.openfoam_compiler()
        compileOpt  = self.foam_cfg['WM_COMPILE_OPTION']

        # Insist on a wmake rule for this architecture/compiler combination
        archCompiler  = wm_arch + wm_compiler
        compiler_rule = join_path(
            self.stage.source_path, 'wmake', 'rules', archCompiler)

        if not isdir(compiler_rule):
            raise RuntimeError(
                'No wmake rule for {0}'.format(archCompiler))
        if not re.match(r'.+Opt$', compileOpt):
            raise RuntimeError(
                "WM_COMPILE_OPTION={0} is not type '*Opt'".format(compileOpt))

        # Adjust for variants
        # FUTURE? self.foam_cfg['WM_LABEL_SIZE'] = (
        # FUTURE?     '64' if '+int64'   in self.spec else '32'
        # FUTURE? )
        self.foam_cfg['WM_PRECISION_OPTION'] = (
            'SP' if '+float32' in self.spec else 'DP'
        )

        # ----
        # WM_OPTIONS=$WM_ARCH$WM_COMPILER$WM_PRECISION_OPTION$WM_COMPILE_OPTION
        # ----
        self.foam_sys['WM_ARCH']     = wm_arch
        self.foam_sys['WM_COMPILER'] = wm_compiler
        self.foam_cfg['WM_COMPILER'] = wm_compiler  # For bashrc,cshrc too
        self.foam_sys['WM_OPTIONS']  = ''.join([
            wm_arch,
            wm_compiler,
            self.foam_cfg['WM_PRECISION_OPTION'],
            # FUTURE? 'Int', self.foam_cfg['WM_LABEL_SIZE'],  # Int32/Int64
            compileOpt
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
./Allwmake            # No arguments
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
        self.etc_prefs = {
            '000': {  # Sort first
                'compilerInstall': 'System',
            },
            '001': {},
            'cmake': {
                'CMAKE_DIR':     spec['cmake'].prefix,
                'CMAKE_BIN_DIR': spec['cmake'].prefix.bin,
            },
            'python': {
                'PYTHON_DIR':     spec['python'].prefix,
                'PYTHON_BIN_DIR': spec['python'].prefix.bin,
            },
            'flex': {
                'FLEX_SYSTEM': 1,
                'FLEX_DIR':    spec['flex'].prefix,
            },
            'bison': {
                'BISON_SYSTEM': 1,
                'BISON_DIR':    spec['flex'].prefix,
            },
            'zlib': {
                'ZLIB_SYSTEM': 1,
                'ZLIB_DIR':    spec['zlib'].prefix,
            },
        }
        # Adjust configuration via prefs - sort second
        self.etc_prefs['001'].update(self.foam_cfg)

        if '+scotch' in spec or '+ptscotch' in spec:
            pkg = spec['scotch'].prefix
            self.etc_prefs['scotch'] = {
                'SCOTCH_SYSTEM': 1,
                'SCOTCH_DIR': pkg,
                'SCOTCH_BIN_DIR': pkg.bin,
                'SCOTCH_LIB_DIR': pkg.lib,
                'SCOTCH_INCLUDE_DIR': pkg.include,
            }

        if '+metis' in spec:
            pkg = spec['metis'].prefix
            self.etc_prefs['metis'] = {
                'METIS_SYSTEM': 1,
                'METIS_DIR': pkg,
                'METIS_BIN_DIR': pkg.bin,
                'METIS_LIB_DIR': pkg.lib,
                'METIS_INCLUDE_DIR': pkg.include,
            }

        if '+parmetis' in spec:
            pkg = spec['parmetis'].prefix
            self.etc_prefs['parametis'] = {
                'PARMETIS_SYSTEM': 1,
                'PARMETIS_DIR':     pkg,
                'PARMETIS_BIN_DIR': pkg.bin,
                'PARMETIS_LIB_DIR': pkg.lib,
                'PARMETIS_INCLUDE_DIR': pkg.include,
            }

        if '+parmgridgen' in spec:
            pkg = spec['parmgridgen'].prefix
            self.etc_prefs['parmgridgen'] = {
                'PARMGRIDGEN_SYSTEM': 1,
                'PARMGRIDGEN_DIR':     pkg,
                'PARMGRIDGEN_BIN_DIR': pkg.bin,
                'PARMGRIDGEN_LIB_DIR': pkg.lib,
                'PARMGRIDGEN_INCLUDE_DIR': pkg.include,
            }

        if '+paraview' in self.spec:
            self.etc_prefs['paraview'] = {
                'PARAVIEW_SYSTEM':  1,
                'PARAVIEW_DIR':     spec['paraview'].prefix,
                'PARAVIEW_BIN_DIR': spec['paraview'].prefix.bin,
            }
            self.etc_prefs['qt'] = {
                'QT_SYSTEM':  1,
                'QT_DIR':     spec['qt'].prefix,
                'QT_BIN_DIR': spec['qt'].prefix.bin,
            }

        # Write prefs files according to the configuration.
        # Only need prefs.sh for building, but install both for end-users
        write_environ(
            self.etc_prefs,
            posix=join_path('etc', 'prefs.sh'),
            cshell=join_path('etc', 'prefs.csh'))

        archCompiler  = self.foam_sys['WM_ARCH'] + self.foam_sys['WM_COMPILER']
        compileOpt    = self.foam_cfg['WM_COMPILE_OPTION']
        # general_rule  = join_path('wmake', 'rules', 'General')
        compiler_rule = join_path('wmake', 'rules', archCompiler)
        generate_mplib_rules(compiler_rule, self.spec)
        generate_compiler_rules(compiler_rule, compileOpt, self.rpath_info)
        # Record the spack spec information
        with open("log.spack-spec", 'w') as outfile:
            outfile.write(spec.tree())

    def build(self, spec, prefix):
        """Build using the OpenFOAM Allwmake script, with a wrapper to source
        its environment first.
        """
        self.set_openfoam()  # Force proper population of foam_cfg/foam_sys
        args = []
        if self.parallel:  # Build in parallel? - pass via the environment
            os.environ['WM_NCOMPPROCS'] = str(self.make_jobs) \
                if self.make_jobs else str(multiprocessing.cpu_count())
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the projectdir (== prefix/name-version)"""
        self.build(spec, prefix)  # Should be a separate phase
        opts = self.wm_options

        # Fairly ugly since intermediate targets are scattered inside sources
        appdir = 'applications'
        mkdirp(self.projectdir, join_path(self.projectdir, appdir))

        # Retain build log file
        out = "spack-build.out"
        if isfile(out):
            install(out, join_path(self.projectdir, "log." + opts))

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
                join_path(self.projectdir, d))

        if '+source' in spec:
            subitem = join_path(appdir, 'Allwmake')
            install(subitem, join_path(self.projectdir, subitem))

            ignored = [opts]  # Intermediate targets
            for d in ['src', 'tutorials']:
                install_tree(
                    d,
                    join_path(self.projectdir, d),
                    ignore=shutil.ignore_patterns(*ignored))

            for d in ['solvers', 'utilities']:
                install_tree(
                    join_path(appdir, d),
                    join_path(self.projectdir, appdir, d),
                    ignore=shutil.ignore_patterns(*ignored))

    def install_links(self):
        """Add symlinks into bin/, lib/ (eg, for other applications)"""
        return

# -----------------------------------------------------------------------------
