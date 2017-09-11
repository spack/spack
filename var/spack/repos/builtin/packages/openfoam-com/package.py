##############################################################################
# Copyright (c) 2017 Mark Olesen, OpenCFD Ltd.
#
# This file was authored by Mark Olesen <mark.olesen@esi-group.com>
# and is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for the LLNL notice and the LGPL.
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
# - mpi handling: WM_MPLIB=USERMPI and use spack to populate an appropriate
#   configuration and generate wmake rules for 'USER' and 'USERMPI'
#   mpi implementations.
#
# - Resolution of flex, zlib needs more attention (within OpenFOAM)
# - +paraview:
#   depends_on should just be 'paraview+plugins' but that resolves poorly.
#   Workaround: use preferred variants "+plugins +qt"
#       packages:
#           paraview:
#               variants: +plugins +qt
#   in ~/.spack/packages.yaml
#
# - Combining +zoltan with +int64 has not been tested, but probably won't work.
#
##############################################################################
from spack import *
from spack.environment import *

import glob
import re
import shutil
import os
from os.path import isdir, isfile

# Not the nice way of doing things, but is a start for refactoring
__all__ = [
    'format_export',
    'format_setenv',
    'write_environ',
    'rewrite_environ_files',
    'mplib_content',
    'generate_mplib_rules',
    'generate_compiler_rules',
]


def format_export(key, value):
    """Format key,value pair as 'export' with newline for POSIX shell."""
    return 'export {0}={1}\n'.format(key, value)


def format_setenv(key, value):
    """Format key,value pair as 'setenv' with newline for C-shell."""
    return 'setenv {0} {1}\n'.format(key, value)


def _write_environ_entries(outfile, environ, formatter):
    """Write environment settings as 'export' or 'setenv'.
    If environ is a dict, write in sorted order.
    If environ is a list, write pair-wise.
    Also descends into sub-dict and sub-list, but drops the key.
    """
    if isinstance(environ, dict):
        for key in sorted(environ):
            entry = environ[key]
            if isinstance(entry, dict):
                _write_environ_entries(outfile, entry, formatter)
            elif isinstance(entry, list):
                _write_environ_entries(outfile, entry, formatter)
            else:
                outfile.write(formatter(key, entry))
    elif isinstance(environ, list):
        for item in environ:
            outfile.write(formatter(item[0], item[1]))


def _write_environ_file(output, environ, formatter):
    """Write environment settings as 'export' or 'setenv'.
    If environ is a dict, write in sorted order.
    If environ is a list, write pair-wise.
    Also descends into sub-dict and sub-list, but drops the key.
    """
    with open(output, 'w') as outfile:
        outfile.write('# SPACK settings\n\n')
        _write_environ_entries(outfile, environ, formatter)


def write_environ(environ, **kwargs):
    """Write environment settings as 'export' or 'setenv'.
    If environ is a dict, write in sorted order.
    If environ is a list, write pair-wise.

       Keyword Options:
         posix[=None]    If set, the name of the POSIX file to rewrite.
         cshell[=None]   If set, the name of the C-shell file to rewrite.
    """
    posix = kwargs.get('posix', None)
    if posix:
        _write_environ_file(posix, environ, format_export)
    cshell = kwargs.get('cshell', None)
    if cshell:
        _write_environ_file(cshell, environ, format_setenv)


def rewrite_environ_files(environ, **kwargs):
    """Use filter_file to rewrite (existing) POSIX shell or C-shell files.
       Keyword Options:
         posix[=None]    If set, the name of the POSIX file to rewrite.
         cshell[=None]   If set, the name of the C-shell file to rewrite.
    """
    posix = kwargs.get('posix', None)
    if posix and isfile(posix):
        for k, v in environ.items():
            filter_file(
                r'^(\s*export\s+%s)=.*$' % k,
                r'\1=%s' % v,
                posix,
                backup=False)
    cshell = kwargs.get('cshell', None)
    if cshell and isfile(cshell):
        for k, v in environ.items():
            filter_file(
                r'^(\s*setenv\s+%s)\s+.*$' % k,
                r'\1 %s' % v,
                cshell,
                backup=False)


def pkglib(package):
    """Get lib64 or lib from package prefix"""
    libdir = package.prefix.lib64
    if isdir(libdir):
        return libdir
    return package.prefix.lib


def mplib_content(spec):
    """The mpi settings to have wmake
    use spack information with minimum modifications to OpenFOAM.
    """
    info = {
        'name':   '{0}-{1}'.format(spec['mpi'].name, spec['mpi'].version),
        'prefix':  spec['mpi'].prefix,
        'include': spec['mpi'].headers,
        'bindir':  spec['mpi'].prefix.bin,
        'libdir':  spec['mpi'].libs,
        'FLAGS':  '-DOMPI_SKIP_MPICXX -DMPICH_IGNORE_CXX_SEEK -DMPICH_SKIP_MPICXX',
        'PINC':    spec['mpi'].headers.include_flags,
        'PLIBS':   spec['mpi'].libs.ld_flags
    }
    return info


def generate_mplib_rules(directory, spec):
    """ Create mplibUSER,mplibUSERMPI rules in the specified directory"""
    content = mplib_content(spec)
    with working_dir(directory):
        for mplib in ['mplibUSER', 'mplibUSERMPI']:
            with open(mplib, 'w') as out:
                out.write("\n".join(["# Use mpi from spack ({name})",
                                     "PFLAGS  = {FLAGS}",
                                     "PINC    = {PINC}",
                                     "PLIBS   = {PLIBS}"]).format(**content))


def generate_compiler_rules(directory, compOpt, value):
    """ Create cSPACKOpt,c++SPACKOpt rules in the specified directory.
    The file content is copied and filtered from the corresponding
    cOpt,c++Opt rules"""
    # Compiler options for SPACK - eg, wmake/rules/linux64Gcc/
    # Copy from existing cOpt, c++Opt and modify DBUG value
    with working_dir(directory):
        for lang in ['c', 'c++']:
            src = '{0}Opt'.format(lang)
            dst = '{0}{1}'.format(lang, compOpt)
            shutil.copyfile(src, dst)  # src -> dst
            filter_file(
                r'^(\S+DBUG\s*)=.*$',
                r'\1= %s' % value,
                dst,
                backup=False)


class OpenfoamCom(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    This offering is supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """

    homepage = "http://www.openfoam.com/"
    baseurl  = "https://sourceforge.net/projects/openfoamplus/files"

    version('1612', 'ca02c491369150ab127cbb88ec60fbdf',
            url=baseurl + '/v1612+/OpenFOAM-v1612+.tgz')

    variant('int64', default=False,
            description='Compile with 64-bit labels')
    variant('float32', default=False,
            description='Compile with 32-bit scalar (single-precision)')
    variant('knl', default=False,
            description='Use KNL compiler settings')

    variant('scotch', default=True,
            description='With scotch/ptscotch for decomposition')
    variant('metis', default=False,
            description='With metis for decomposition')
    variant('zoltan', default=False,
            description='With zoltan renumbering')
    # TODO?#   variant('parmgridgen', default=True,
    # TODO?#           description='With parmgridgen support')
    variant('source', default=True,
            description='Install library/application sources and tutorials')

    variant('paraview', default=True,
            description='Build paraview plugins and runtime post-processing')

    #: Map spack compiler names to OpenFOAM compiler names
    #  By default, simply capitalize the first letter
    compiler_mapping = {'intel': 'icc'}

    provides('openfoam')
    depends_on('mpi')
    depends_on('zlib')
    depends_on('fftw')
    depends_on('boost')
    depends_on('cgal')
    depends_on('flex@:2.6.1')  # <- restriction due to scotch
    depends_on('cmake', type='build')

    depends_on('binutils', type='build')

    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    # scotch+metix conflicts with metis itself due to the order of detection of the headers
    depends_on('scotch~int64~metis+mpi', when='+scotch~int64')
    depends_on('scotch+int64~metis+mpi', when='+scotch+int64')
    depends_on('metis@5:',     when='+metis')
    depends_on('metis+int64',  when='+metis+int64')
    depends_on('parmgridgen',  when='+parmgridgen')
    depends_on('zoltan',       when='+zoltan')

    # For OpenFOAM plugins and run-time post-processing this should just be
    # 'paraview+plugins' but that resolves poorly.
    # Workaround: use preferred variants "+plugins +qt" in
    #   ~/.spack/packages.yaml

    # 1612 plugins need older paraview
    # The native reader in paraview 5.2 is broken, so start after that
    depends_on('paraview@:5.0.1', when='@:1612+paraview')
    depends_on('paraview@5.3:',   when='@1706:+paraview')

    # General patches
    patch('openfoam-site.patch')

    # Version-specific patches
    patch('openfoam-bin-1612.patch', when='@1612')
    patch('openfoam-etc-1612.patch', when='@1612')
    patch('openfoam-mpi-1612.patch', when='@1612')
    patch('openfoam-build-1612.patch', when='@1612')
    patch('scotch-metis-lib-1612.patch', when='@1612')
    patch('zoltan-lib-1612.patch',   when='@1612')

    # Some user settings, to be adjusted manually or via variants
    foam_cfg = {
        'WM_COMPILER':        'Gcc',  # <- %compiler
        'WM_ARCH_OPTION':     '64',   # (32/64-bit on x86_64)
        'WM_LABEL_SIZE':      '32',   # <- +int64
        'WM_PRECISION_OPTION': 'DP',  # <- +float32
        'WM_COMPILE_OPTION':  'SPACKOpt',   # Do not change
        'WM_MPLIB':           'USERMPI',    # Use user mpi for spack
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

    # Add symlinks into bin/, lib/ (eg, for other applications)
    extra_symlinks = False

    # Quickly enable/disable testing with the current develop branch
    if False:
        version(
            'plus',
            branch='develop',
            git='file://{0}/{1}'
            .format(os.path.expanduser("~"), 'openfoam/OpenFOAM-plus/.git'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('WM_PROJECT_DIR', self.projectdir)

    @property
    def projectdir(self):
        """Absolute location of project directory: WM_PROJECT_DIR/"""
        return self.prefix  # <- install directly under prefix

    @property
    def etc(self):
        """Absolute location of the OpenFOAM etc/ directory"""
        return join_path(self.projectdir, 'etc')

    @property
    def archbin(self):
        """Relative location of architecture-specific executables"""
        return join_path('platforms', self.wm_options, 'bin')

    @property
    def archlib(self):
        """Relative location of architecture-specific libraries"""
        return join_path('platforms', self.wm_options, 'lib')

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
        self.foam_cfg['WM_LABEL_SIZE'] = (
            '64' if '+int64'   in self.spec else '32'
        )
        self.foam_cfg['WM_PRECISION_OPTION'] = (
            'SP' if '+float32' in self.spec else 'DP'
        )

        # ----
        # WM_LABEL_OPTION=Int$WM_LABEL_SIZE
        # WM_OPTIONS=$WM_ARCH$WM_COMPILER$WM_PRECISION_OPTION$WM_LABEL_OPTION$WM_COMPILE_OPTION
        # ----
        self.foam_sys['WM_ARCH']     = wm_arch
        self.foam_sys['WM_COMPILER'] = wm_compiler
        self.foam_cfg['WM_COMPILER'] = wm_compiler  # For bashrc,cshrc too
        self.foam_sys['WM_OPTIONS']  = ''.join([
            wm_arch,
            wm_compiler,
            self.foam_cfg['WM_PRECISION_OPTION'],
            'Int', self.foam_cfg['WM_LABEL_SIZE'],  # Int32/Int64
            compileOpt
        ])
        return self.foam_sys['WM_OPTIONS']

    def patch(self):
        """Adjust OpenFOAM build for spack. Where needed, apply filter as an
        alternative to normal patching.
        """
        self.set_openfoam()  # May need foam_cfg/foam_sys information

        # Avoid WM_PROJECT_INST_DIR for ThirdParty, site or jobControl.
        # Use openfoam-site.patch to handle jobControl, site.
        #
        # Filter (not patch) bashrc,cshrc for additional flexibility
        wm_setting = {
            'WM_THIRD_PARTY_DIR':
            r'$WM_PROJECT_DIR/ThirdParty #SPACK: No separate third-party',
        }

        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            wm_setting,
            posix=join_path('etc', 'bashrc'),
            cshell=join_path('etc', 'cshrc'))

        # Adjust ParMGridGen - this is still a mess.
        # We also have no assurances about sizes (int/long, float/double) etc.
        #
        # Need to adjust src/fvAgglomerationMethods/Allwmake
        #     "export ParMGridGen=%s" % spec['parmgridgen'].prefix
        #
        # and src/fvAgglomerationMethods/MGridGenGamgAgglomeration/Make/options
        #     "-I=%s" % spec['parmgridgen'].include
        #     "-L=%s -lmgrid" % spec['parmgridgen'].lib

        # Build wrapper script
        with open(self.build_script, 'w') as out:
            out.write(
                """#!/bin/bash
. $PWD/etc/bashrc ''  # No arguments
mkdir -p $FOAM_APPBIN $FOAM_LIBBIN 2>/dev/null  # Allow interrupt
echo Build openfoam with SPACK
echo WM_PROJECT_DIR = $WM_PROJECT_DIR
./Allwmake $@
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

        # Some settings for filtering bashrc, cshrc
        wm_setting = {}
        wm_setting.update(self.foam_cfg)

        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            wm_setting,
            posix=join_path('etc', 'bashrc'),
            cshell=join_path('etc', 'cshrc'))

        # Content for etc/prefs.{csh,sh}
        self.etc_prefs = {
            # TODO
            # 'CMAKE_ARCH_PATH': spec['cmake'].prefix,
            # 'FLEX_ARCH_PATH':  spec['flex'].prefix,
            # 'ZLIB_ARCH_PATH':  spec['zlib'].prefix,
        }

        # Content for etc/config.{csh,sh}/ files
        self.etc_config = {
            'CGAL': {
                'BOOST_ARCH_PATH': spec['boost'].prefix,
                'CGAL_ARCH_PATH':  spec['cgal'].prefix,
            },
            'FFTW': {
                'FFTW_ARCH_PATH': spec['fftw'].prefix,
            },
            # User-defined MPI
            'mpi-user': [
                ('MPI_ARCH_PATH', spec['mpi'].prefix),  # Absolute
                ('LD_LIBRARY_PATH',
                 '"%s:${LD_LIBRARY_PATH}"' % ':'.join(spec['mpi'].libs.directories)),
                ('PATH', '"%s:${PATH}"' % spec['mpi'].prefix.bin),
            ],
            'scotch': {},
            'metis': {},
            'paraview': [],
        }

        if '+scotch' in spec:
            self.etc_config['scotch'] = {
                'SCOTCH_ARCH_PATH': spec['scotch'].prefix,
                # For src/parallel/decompose/Allwmake
                'SCOTCH_VERSION': 'scotch-{0}'.format(spec['scotch'].version),
            }

        if '+metis' in spec:
            self.etc_config['metis'] = {
                'METIS_ARCH_PATH': spec['metis'].prefix,
            }

        if '+paraview' in spec:
            pvMajor = 'paraview-{0}'.format(spec['paraview'].version.up_to(2))
            self.etc_config['paraview'] = [
                ('ParaView_DIR', spec['paraview'].prefix),
                ('ParaView_INCLUDE_DIR', '$ParaView_DIR/include/' + pvMajor),
                ('PV_PLUGIN_PATH', '$FOAM_LIBBIN/' + pvMajor),
                ('PATH', '"${ParaView_DIR}/bin:${PATH}"'),
            ]

        # Not normally included as etc/config file
        if '+parmgridgen' in spec:
            self.etc_config['parmgridgen'] = {
                'PARMGRIDGEN_ARCH_PATH': spec['parmgridgen'].prefix
            }

        # Optional
        if '+zoltan' in spec:
            self.etc_config['zoltan'] = {
                'ZOLTAN_ARCH_PATH': spec['zoltan'].prefix
            }

        # Write prefs files according to the configuration.
        # Only need prefs.sh for building, but install both for end-users
        if self.etc_prefs:
            write_environ(
                self.etc_prefs,
                posix=join_path('etc', 'prefs.sh'),
                cshell=join_path('etc', 'prefs.csh'))

        # Adjust components to use SPACK variants
        for component, subdict in self.etc_config.items():
            write_environ(
                subdict,
                posix=join_path('etc', 'config.sh',  component),
                cshell=join_path('etc', 'config.csh', component))

        archCompiler  = self.foam_sys['WM_ARCH'] + self.foam_sys['WM_COMPILER']
        compileOpt    = self.foam_cfg['WM_COMPILE_OPTION']
        general_rule  = join_path('wmake', 'rules', 'General')
        compiler_rule = join_path('wmake', 'rules', archCompiler)
        generate_mplib_rules(general_rule, self.spec)
        generate_compiler_rules(compiler_rule, compileOpt, self.rpath_info)
        # Record the spack spec information
        with open("log.spack-spec", 'w') as outfile:
            outfile.write(spec.tree())

    def build(self, spec, prefix):
        """Build using the OpenFOAM Allwmake script, with a wrapper to source
        its environment first.
        """
        self.set_openfoam()  # Force proper population of foam_cfg/foam_sys
        args = ['-silent']
        if self.parallel:  # Build in parallel? - pass as an argument
            args.append(
                '-j{0}'.format(str(self.make_jobs) if self.make_jobs else ''))
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the projectdir (== prefix)"""
        self.build(spec, prefix)  # Should be a separate phase
        opts = self.wm_options

        mkdirp(self.projectdir)
        projdir = os.path.basename(self.projectdir)
        wm_setting = {
            'WM_PROJECT_INST_DIR': os.path.dirname(self.projectdir),
            'WM_PROJECT_DIR': join_path('$WM_PROJECT_INST_DIR', projdir),
        }

        # Retain build log file
        out = "spack-build.out"
        if isfile(out):
            install(out, join_path(self.projectdir, "log." + opts))

        # All top-level files, except spack build info and possibly Allwmake
        if '+source' in spec:
            ignored = re.compile(r'^spack-.*')
        else:
            ignored = re.compile(r'^(Allwmake|spack-).*')

        files = [
            f for f in glob.glob("*") if isfile(f) and not ignored.search(f)
        ]
        for f in files:
            install(f, self.projectdir)

        # Having wmake without sources is actually somewhat pointless...
        dirs = ['bin', 'etc', 'wmake']
        if '+source' in spec:
            dirs.extend(['applications', 'src', 'tutorials'])

        for d in dirs:
            install_tree(
                d,
                join_path(self.projectdir, d))

        dirs = ['platforms']
        if '+source' in spec:
            dirs.extend(['doc'])

        # Install platforms (and doc) skipping intermediate targets
        ignored = ['src', 'applications', 'html', 'Guides']
        for d in dirs:
            install_tree(
                d,
                join_path(self.projectdir, d),
                ignore=shutil.ignore_patterns(*ignored))

        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            wm_setting,
            posix=join_path(self.etc, 'bashrc'),
            cshell=join_path(self.etc, 'cshrc'))
        self.install_links()

    def install_links(self):
        """Add symlinks into bin/, lib/ (eg, for other applications)"""
        if not self.extra_symlinks:
            return

        # ln -s platforms/linux64GccXXX/lib lib
        with working_dir(self.projectdir):
            if isdir(self.archlib):
                os.symlink(self.archlib, 'lib')

        # (cd bin && ln -s ../platforms/linux64GccXXX/bin/* .)
        with working_dir(join_path(self.projectdir, 'bin')):
            for f in [
                f for f in glob.glob(join_path('..', self.archbin, "*"))
                if isfile(f)
            ]:
                os.symlink(f, os.path.basename(f))

# -----------------------------------------------------------------------------
