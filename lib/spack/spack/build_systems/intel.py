##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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

import os
import sys
import glob
import re
import inspect
import xml.etree.ElementTree as ET
import llnl.util.tty as tty

from llnl.util.filesystem import \
    install, join_path, ancestor, filter_file, \
    LibraryList, find_headers, find_libraries, find_system_libraries

from spack.version import Version
from spack.package import PackageBase, run_after, InstallError
from spack.util.executable import Executable
from spack.util.prefix import Prefix
from spack.build_environment import dso_suffix
from spack.environment import EnvironmentModifications


# A couple of utility functions that might be useful in general. If so, they
# should really be defined elsewhere, unless deemed heretical.
# (Or na"ive on my part).

def debug_print(msg, *args):
    '''Prints a message (usu. a variable) and the callers' names for a couple
    of stack frames.
    '''
    # https://docs.python.org/2/library/inspect.html#the-interpreter-stack
    stack = inspect.stack()
    _func_name = 3
    tty.debug("%s.%s:\t%s" % (stack[2][_func_name], stack[1][_func_name], msg),
              *args)


def raise_lib_error(*args):
    '''Bails out with an error message. Shows args after the first as one per
    line, tab-indented, useful for long paths to line up and stand out.
    '''
    raise InstallError("\n\t".join(str(i) for i in args))


def _expand_fields(s):
    '''[Experimental] Expand arch-related fields in a string, typically a
    filename.

    Supported fields and their typical expansions are::

        {platform}  linux
        {arch}      intel64
        {bits}      64

    '''
    # Python-native string formatting requires arg list counts to match the
    # replacement field count; optional fields are far easier with regexes.

    if 'linux' in sys.platform:            # NB: linux2 vs. linux
        s = re.sub('{platform}', 'linux', s)
    # elif 'darwin' in sys.platform:         # TBD
    #     s = re.sub('{platform}', '', s)    # typically not used (right?)
    # elif 'win' in sys.platform:            # TBD
    #     s = re.sub('{platform}', 'windows', s)

    s = re.sub('{arch}', 'intel64', s)      # TBD: ia32
    s = re.sub('{bits}', '64', s)
    return s


class IntelPackage(PackageBase):
    """Specialized class for licensed Intel software.

    This class provides two phases that can be overridden:

    1. :py:meth:`~.IntelPackage.configure`
    2. :py:meth:`~.IntelPackage.install`

    They both have sensible defaults and for many packages the
    only thing necessary will be to override setup_environment
    to set the appropriate environment variables.
    """
    #: Phases of an Intel package
    phases = ['configure', 'install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'IntelPackage'

    #: A dict that maps Spack version specs to release years, needed to infer
    #: the installation directory layout for pre-2016 versions in the family of
    #: Intel packages.
    #
    # Like any property, it can be overridden in client packages, should older
    # versions ever be added there.  The initial dict here contains the
    # packages defined in Spack as of 2018-04.  Keys could conceivably overlap
    # but preferably should not - only the first key in hash traversal order
    # that satisfies self.spec will be used.
    version_years = {
        # intel-daal is versioned 2016 and later, no divining is needed
        'intel-ipp@9.0:9.99':         2016,
        'intel-mkl@11.3.0:11.3.999':  2016,
        'intel-mpi@5.1:5.99':         2016,
    }

    @property
    def license_required(self):
        # The Intel libraries are provided without requiring a license as of
        # version 2017.2. Trying to specify one anyway will fail. See:
        # https://software.intel.com/en-us/articles/free-ipsxe-tools-and-libraries
        return self._has_compilers or self.version < Version('2017.2')

    #: Comment symbol used in the license.lic file
    license_comment = '#'

    #: Environment variables that Intel searches for a license file
    license_vars = ['INTEL_LICENSE_FILE']

    #: URL providing information on how to acquire a license key
    license_url = 'https://software.intel.com/en-us/articles/intel-license-manager-faq'

    #: Location where Intel searches for a license file
    @property
    def license_files(self):
        dirs = ['Licenses']

        if self._has_compilers:
            dirs.append(self.component_bin_dir('compiler'))

            addons_by_variant = {
                '+advisor':    'advisor',
                '+inspector':  'inspector',
                '+itac':       'itac',
                '+vtune':      'vtune_amplifier',
            }

            for variant, dir_name in addons_by_variant.items():
                if variant not in self.spec:
                    continue
                if (self._version_yearlike < Version('2018') and
                        dir_name != 'itac'):
                    dir_name += '_xe'
                dirs.append(self.normalize_path(
                    'licenses', dir_name, relative=True))

        return [os.path.join(d, 'license.lic') for d in dirs]

    #: Components to install (list of name patterns from pset/mediaconfig.xml)
    # NB: Renamed from plain components() for coding and maintainability.
    @property
    def pset_components(self):
        # Do not detail single-purpose client packages.
        if not self._has_compilers:
            return ['ALL']

        # Always include compilers and closely related components.
        # Pre-2016 compiler components have different names - throw in all.
        # Later releases have overlapping minor parts that differ by "edition".
        # NB: The spack package 'intel' is a subset of
        # 'intel-parallel-studio@composer' without the lib variants.
        c = ' intel-icc          intel-ifort' \
            ' intel-ccomp        intel-fcomp        intel-comp-' \
            ' intel-compilerproc intel-compilerprof intel-compilerpro-' \
            ' intel-psxe intel-openmp'

        additions_for = {
            'cluster':      ' intel-icsxe',
            'professional': ' intel-ips-',
            'composer':     ' intel-compxe',
        }
        if self._edition in additions_for:
            c += additions_for[self._edition]

        for variant, components_to_add in {
            '+daal':      ' intel-daal',   # Data Analytics Acceleration Lib
            '+gdb':       ' intel-gdb',    # Integrated Performance Primitives
            '+ipp':       ' intel-ipp intel-crypto-ipp',
            '+mkl':       ' intel-mkl',    # Math Kernel Library
            '+mpi':       ' intel-mpi intel-mpirt intel-imb',
            '+tbb':       ' intel-tbb',    # Threading Building Blocks
            '+advisor':   ' intel-advisor',
            '+clck':      ' intel_clck',   # Cluster Checker
            '+inspector': ' intel-inspector',
            '+itac':      ' intel-itac intel-ta intel-tc'
                          ' intel-trace-analyzer intel-trace-collector',
                          # Trace Analyzer and Collector
            '+vtune':     ' intel-vtune-amplifier',    # VTune
        }.items():
            if variant in self.spec:
                c += components_to_add

        debug_print(c)
        return c.split()

    # ---------------------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------------------
    @property
    def _filtered_components(self):
        '''Expands the list of desired component patterns to the exact names
        present in the given download.
        '''
        c = self.pset_components
        if 'ALL' in c or 'DEFAULTS' in c:    # No filter needed
            return c

        # mediaconfig.xml is known to contain duplicate components.
        # If more than one copy of the same component is used, you
        # will get an error message about invalid components.
        # Use sets to prevent duplicates and for efficient traversal.
        requested = set(c)
        confirmed = set()

        # NB: To get a reasonable overview in pretty much the documented way:
        #
        #   grep -E '<Product|<Abbr|<Name>..[a-z]'  pset/mediaconfig.xml
        #
        # https://software.intel.com/en-us/articles/configuration-file-format
        #
        xmltree = ET.parse('pset/mediaconfig.xml')
        for entry in xmltree.getroot().findall('.//Abbr'):  # XPath expression
            name_present = entry.text
            for name_requested in requested:
                if name_present.startswith(name_requested):
                    confirmed.add(name_present)

        return list(confirmed)

    @property
    def intel64_int_suffix(self):
        '''Provide the suffix for Intel library names to match a client
        application's desired int size, conveyed by the active spec variant.
        The possible suffixes and their meanings are:

          ``ilp64``  all of int, long, and pointer are 64 bit,
          `` lp64``  only long and pointer are 64 bit; int will be 32bit.
        '''
        if '+ilp64' in self.spec:
            return 'ilp64'
        else:
            return 'lp64'

    @property
    def _has_compilers(self):
        return self.name in ['intel', 'intel-parallel-studio']

    @property
    def _edition(self):
        if self.name == 'intel-parallel-studio':
            return self.version[0]      # clearer than .up_to(1), I think.
        elif self.name == 'intel':
            return 'composer'
        else:
            return ''

    @property
    def _version_yearlike(self):
        '''Return the version in a unified style, suitable for Version class
        conditionals.
        '''
        # Versioning styles:
        # - 'intel-parallel-studio' :   <edition>.YYYY.Nupdate
        # - 'intel':                    YY.0.Nupdate (some assigned ad-hoc)
        # - Recent lib packages:        YYYY.Nupdate.Buildseq
        # - Early lib packages:         Major.Minor.Patch.Buildseq
        try:
            if self.name == 'intel':
                # Has a "Minor" version element, but it is always set as 0. To
                # be useful for comparisons, drop it and get YYYY.Nupdate.
                v_tail = self.version[2:]   # coerced just fine via __getitem__
            else:
                v_tail = self.version[1:]
        except IndexError:
            # Hmm - this happens on "spack install intel-mkl@11".
            # I thought concretization picks an actual version??
            return self.version     # give up

        if self.name == 'intel-parallel-studio':
            return v_tail

        v_year = self.version[0]
        if v_year < 2000:
            # Shoehorn Major into release year until we know better.
            v_year += 2000
            for spec, year in self.version_years.items():
                if self.spec.satisfies(spec):
                    v_year = year
                    break

        return Version('%s.%s' % (v_year, v_tail))

    @property
    def _uses_early_dir_layout(self):
        # Intel's nomenclature and scope for product names changed over the
        # years.  In 2015, "Parallel Studio" simply was the higher-tier
        # product. In Spack, we justifiably retconned this as "cluster
        # edition".  "Composer" in 2015 simply was the lower-tier product,
        # later retconned as "composer edition".  Both products used the
        # "composer_xe" dir layout.
        #
        # The *virtual* library packages derived from those 2015 products
        # *also* use the older layout(!).
        #
        # The *standalone* "intel-foo" library packages in Spack as of 2018-04
        # are all 2016 and later releases. All are versioned by year only from
        # 2017 onwards [except DAAL], and *all* use "compilers_and_libraries".

        result = self._version_yearlike < Version('2016')
        debug_print(result)
        return result

    # ---------------------------------------------------------------------
    # Directory handling common to all Intel components
    # ---------------------------------------------------------------------
    # For reference: classes using IntelPackage, as of Spack-0.11:
    #
    #  intel/               intel-ipp/          intel-mpi/
    #  intel-daal/          intel-mkl/          intel-parallel-studio/
    #
    # Not using class IntelPackage:
    #  intel-gpu-tools/        intel-mkl-dnn/          intel-tbb/
    #
    def normalize_suite_dir(self, product_dir_name, version_glob='_*.*.*'):
        '''Returns the version-specific and absolute path to the directory of
        an Intel product or a suite of product components.

        Parameters:

            product_dir_name (str):
                Name of the product directory, without numeric version.

                - Examples::

                    composer_xe, parallel_studio_xe, compilers_and_libraries

                The following will work as well, even though they are not
                directly targets for Spack installation::

                    advisor_xe, inspector_xe, vtune_amplifier_xe,
                    performance_snapshots (new name for vtune as of 2018)

                These are single-component products without subordinate
                components and are normally made available to users by a
                toplevel psxevars.sh or equivalent file to source (and thus by
                the modulefiles that Spack produces).

            version_glob (str): A glob pattern that fully qualifies
                product_dir_name to a specific version within an actual
                directory (not a symlink).
        '''
        # See ./README-intel.rst for background and analysis of dir layouts.

        d = self.prefix
        if sys.platform == 'darwin':
            # TODO: Verify on Mac.
            return Prefix(d)

        # Distinguish between product installations that were done external to
        # Spack (integrated via packages.yaml) and Spack-internal ones. The
        # resulting prefixes may differ in directory depth and specificity.
        dir_to_expand = ''
        if product_dir_name and product_dir_name in d:
            # If e.g. MKL was installed outside of Spack, it is likely just one
            # product or product component among possibly many other Intel
            # products and their releases that were installed in sibling or
            # cousin directories.  In such cases, the prefix given to Spack
            # will inevitably be a highly product-specific and preferably fully
            # version-specific directory.  This is what we want and need, and
            # nothing more specific than that, i.e., if needed, convert:
            #   .../compilers_and_libraries*/* -> .../compilers_and_libraries*
            d = re.sub('(%s%s.*?)%s.*' %
                       (os.sep, re.escape(product_dir_name), os.sep), r'\1', d)

            # The Intel installer scripts try hard to place compatibility links
            # named like this in the install dir to convey upgrade benefits to
            # traditional client apps. But such a generic name can be trouble
            # when given to Spack: the link target is bound to change outside
            # of Spack's purview and when it does, the outcome of subsequent
            # builds of dependent packages may be affected. (Though Intel has
            # been remarkably good at backward compatibility.)
            # I'm not sure if Spack's package hashing includes link targets.
            if d.endswith(product_dir_name):
                # NB: This could get tiresome without a seen++ test.
                # tty.warn('Intel product found in a version-neutral directory'
                #          ' - future builds may not be reproducible.')
                #
                # Simply doing realpath() would not be enough, because:
                #   compilers_and_libraries -> compilers_and_libraries_2018
                # which is mostly a staging directory for symlinks (see next).
                dir_to_expand = d
        else:
            # By contrast, a Spack-internal MKL installation will inherit its
            # prefix from install.sh of Intel's package distribution, where it
            # means the high-level installation directory that is specific to
            # the *vendor* (think of the default "/opt/intel"). We must now
            # step down into the *product* directory to get the usual
            # hierarchy. But let's not do that in haste ...
            #
            # For a Spack-born install, the fully-qualified release directory
            # desired above may seem less important since product upgrades
            # won't land in the same parent. However, only the fully qualified
            # directory contains the regular files for the compiler commands:
            #
            # $ ls -lF <HASH>/compilers_and_libraries*/linux/bin/intel64/icc
            #
            # <HASH>/compilers_and_libraries_2018.1.163/linux/bin/intel64/icc*
            #   A regular file in the actual release directory. Bingo!
            #
            # <HASH>/compilers_and_libraries_2018/linux/bin/intel64/icc -> ...
            #   A symlink - no good. Note that "compilers_and_libraries_2018/"
            #   is itself a directory (not symlink) but it merely holds a
            #   compatibility dir hierarchy with lots of symlinks into the
            #   release dir.
            #
            # <HASH>/compilers_and_libraries/linux/bin/intel64/icc -> ...
            #   Ditto.
            #
            #  Now, the Spack packages for MKL and MPI packges use version
            #  triplets, but the one for intel-parallel-studio does not.
            #  So, we can't have it quite as easy as:
            # d = Prefix(d.append('compilers_and_libraries_' + self.version))
            #  Alright, let's see what we can find instead:
            dir_to_expand = join_path(d, product_dir_name)

        if dir_to_expand:
            matching_dirs = glob.glob(dir_to_expand + version_glob)
            if matching_dirs:
                # Take the highest and thus presumably newest match, which
                # better be the sole one anyway.
                d = matching_dirs[-1]
            else:
                # No match -- this *will* happen during pre-build call to
                # setup_environment() when the destination dir is still empty.
                # Return a sensible value anyway.
                d = dir_to_expand

        debug_print(d)
        return Prefix(d)

    def normalize_path(self, component_path, component_suite_dir=None,
                       relative=False):
        '''Returns the absolute or relative path to a component or file under a
        component suite directory.

        Parameters:

            component_path (str): a component name like 'mkl', or 'mpi', or a
                deeper relative path.

            component_suite_dir (str): _Unversioned_ name of the expected
                parent directory of component_path.  When absent or None,
                the default compilers_and_libraries will be used.  A present
                but empty string "" requests that component_path refer to
                self.prefix directly.

            relative (bool): When True, return path relative to self.prefix,
                otherwise, return an absolute path (the default).
        '''
        # Design note: Choosing the default for `component_suite_dir` was a bit
        # tricky since there better be a sensible means to specify direct
        # parentage under self.prefix (even though you normally shouldn't need
        # a function for that).  I chose "" to allow that case be represented,
        # and 'None' or the absence of the kwarg to represent the most relevant
        # case for the time of writing.

        if component_suite_dir is None:
            if self._uses_early_dir_layout:
                component_suite_dir = 'composer_xe'     # The only one present.
            elif component_path.startswith('ism'):
                component_suite_dir = 'parallel_studio_xe'
            else:
                component_suite_dir = 'compilers_and_libraries'  # most comps.

        d = self.normalize_suite_dir(component_suite_dir)
        parent_dir = ancestor(os.path.realpath(d))   # usu. same as self.prefix

        if component_suite_dir == 'compilers_and_libraries':    # passed or set
            if 'linux' in sys.platform:
                d += '/linux'          # Not used in any other component suite.

        if self._uses_early_dir_layout:
            if component_path.startswith('mpi'):
                # Need to rejigger and re-parent the component dir.
                dirs = glob.glob(join_path(parent_dir, 'impi', '[45].*.*'))
                debug_print('dirs: %s' % dirs)
                # Brazenly assume last match is the most recent version;
                # convert back to relative of parent_dir, and re-assemble.
                rel_dir = dirs[-1].split(parent_dir + os.sep, 1)[-1]
                component_path = component_path.replace('mpi', rel_dir, 1)
                d = parent_dir
            # Ignore imb = MPI Benchmarks; mkl OK under component_suite_dir.

        d = join_path(d, component_path)

        if relative:
            d = os.path.relpath(os.path.realpath(d), parent_dir)

        debug_print(d)
        return d

    def component_bin_dir(self, component, **kwargs):
        d = self.normalize_path(component, **kwargs)

        if sys.platform == 'darwin':
            d = join_path(d, 'bin')
        else:
            if component == 'mpi':
                d = join_path(d, _expand_fields('{arch}'), 'bin')
            elif component == 'compiler':
                d = join_path(ancestor(d), 'bin', _expand_fields('{arch}'))
                # works fine even with relative=True, e.g.:
                #   composer_xe/compiler -> composer_xe/bin/intel64
            else:
                d = join_path(d, 'bin')
        debug_print(d)
        return d

    def component_lib_dir(self, component, **kwargs):
        '''Provide directory suitable for find_libraries() and
        SPACK_COMPILER_EXTRA_RPATHS.
        '''
        d = self.normalize_path(component, **kwargs)

        if sys.platform == 'darwin':
            d = join_path(d, 'lib')
        else:
            if component == 'mpi':
                d = join_path(d, _expand_fields('{arch}'), 'lib')
            else:
                d = join_path(d, 'lib', _expand_fields('{arch}'))

            if component == 'tbb':      # must further qualify for abi
                d = join_path(d, self._tbb_abi)

        debug_print(d)
        return d

    def component_include_dir(self, component, **kwargs):
        d = self.normalize_path(component, **kwargs)

        if component == 'mpi':
            d = join_path(d, _expand_fields('{arch}'))
        d = join_path(d, 'include')
        debug_print(d)
        return d

    @property
    def file_to_source(self):
        '''Full path of file to source for initializing an Intel package.
        A client package could override as follows:
        `    @property`
        `    def file_to_source(self):`
        `        return self.normalize_path("apsvars.sh", "vtune_amplifier")`
        '''
        vars_file_info_for = {
            # key (usu. spack package name) -> [rel_path, component_suite_dir]
            '@early_compiler':       ['bin/compilervars',       None],
            'intel-parallel-studio': ['bin/psxevars', 'parallel_studio_xe'],
            'intel':                 ['bin/compilervars',       None],
            'intel-daal':            ['daal/bin/daalvars',      None],
            'intel-ipp':             ['ipp/bin/ippvars',        None],
            'intel-mkl':             ['mkl/bin/mklvars',        None],
            'intel-mpi':             ['mpi/{arch}/bin/mpivars', None],
        }
        key = self.name
        if self._uses_early_dir_layout:
            # Same file as 'intel' but 'None' for component_suite_dir will
            # resolve differently. Listed as a separate entry to serve as
            # example and to avoid pitfalls upon possible refactoring.
            key = '@early_compiler'

        f, component_suite_dir = vars_file_info_for[key]
        f = _expand_fields(f) + '.sh'
        # TODO?? win32 would have to handle os.sep, '.bat' (unless POSIX??)

        f = self.normalize_path(f, component_suite_dir)
        return f

    # ---------------------------------------------------------------------
    # Threading, including (WIP) support for virtual 'tbb'
    # ---------------------------------------------------------------------
    @property
    def openmp_libs(self):
        '''Supply LibraryList for linking OpenMP'''

        if '%intel' in self.spec:
            # NB: Hunting down explicit library files may be the Spack way of
            # doing things, but be aware that "{icc|ifort} --help openmp"
            # steers us towards options instead: -qopenmp-link={dynamic,static}

            omp_libnames = ['libiomp5']
            omp_libs = find_libraries(
                omp_libnames,
                root=self.component_lib_dir('compiler'),
                shared=('+shared' in self.spec))
            # Note about search root here: For MKL, the directory
            # "$MKLROOT/../compiler" will be present even for an MKL-only
            # product installation (as opposed to one being ghosted via
            # packages.yaml), specificially to provide the 'iomp5' libs.

        elif '%gcc' in self.spec:
            gcc = Executable(self.compiler.cc)
            omp_lib_path = gcc(
                '--print-file-name', 'libgomp.%s' % dso_suffix, output=str)
            omp_libs = LibraryList(omp_lib_path)

        if len(omp_libs) < 1:
            raise_lib_error('Cannot locate OpenMP libraries:', omp_libnames)

        debug_print(omp_libs)
        return omp_libs

    @property
    def tbb_libs(self):
        '''Supply LibraryList for linking TBB'''

        # TODO: When is 'libtbbmalloc' needed?
        tbb_lib = find_libraries(
            ['libtbb'], root=self.component_lib_dir('tbb'))
        # NB: Like icc with -qopenmp, so does icpc steer us towards using an
        # option: "icpc -tbb"

        # TODO: clang(?)
        gcc = Executable('gcc')     # must be gcc, not self.compiler.cc
        cxx_lib_path = gcc(
            '--print-file-name', 'libstdc++.%s' % dso_suffix, output=str)

        libs = tbb_lib + LibraryList(cxx_lib_path)
        debug_print(libs)
        return libs

    @property
    def _tbb_abi(self):
        '''Select the ABI needed for linking TBB'''
        # Match the available gcc, as it's done in tbbvars.sh.
        gcc = Executable('gcc')
        matches = re.search(r'(gcc|LLVM).* ([0-9]+\.[0-9]+\.[0-9]+).*',
                            gcc('--version', output=str), re.I | re.M)
        if matches:
            # TODO: Confirm that this covers clang (needed on Linux only)
            gcc_version = Version(matches.groups()[1])
            if gcc_version >= Version('4.7'):
                abi = 'gcc4.7'
            elif gcc_version >= Version('4.4'):
                abi = 'gcc4.4'
            else:
                abi = 'gcc4.1'     # unlikely, one hopes.
        else:
            abi = ''

        # Alrighty then ...
        debug_print(abi)
        return abi

    # ---------------------------------------------------------------------
    # Support for virtual 'blas/lapack/scalapack'
    # ---------------------------------------------------------------------
    @property
    def blas_libs(self):
        # Main magic here.
        # For reference, see The Intel Math Kernel Library Link Line Advisor:
        # https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor/

        mkl_integer = 'libmkl_intel_' + self.intel64_int_suffix

        if self.spec.satisfies('threads=openmp'):
            if '%intel' in self.spec:
                mkl_threading = 'libmkl_intel_thread'
            elif '%gcc' in self.spec:
                mkl_threading = 'libmkl_gnu_thread'
            threading_engine_libs = self.openmp_libs()
        elif self.spec.satisfies('threads=tbb'):
            mkl_threading = 'libmkl_tbb_thread'
            threading_engine_libs = self.tbb_libs()
        elif self.spec.satisfies('threads=none'):
            mkl_threading = 'libmkl_sequential'
            threading_engine_libs = LibraryList([])
        else:
            raise_lib_error('Cannot determine MKL threading libraries.')

        mkl_libnames = [mkl_integer, mkl_threading, 'libmkl_core']
        mkl_libs = find_libraries(
            mkl_libnames,
            root=self.component_lib_dir('mkl'),
            shared=('+shared' in self.spec))
        debug_print(mkl_libs)

        if len(mkl_libs) < 3:
            raise_lib_error('Cannot locate core MKL libraries:', mkl_libnames)

        # The Intel MKL link line advisor recommends these system libraries
        system_libs = find_system_libraries(
            'libpthread libm libdl'.split(),
            shared=('+shared' in self.spec))
        debug_print(system_libs)

        return mkl_libs + threading_engine_libs + system_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        # Intel MKL does not directly depend on MPI but the BLACS library
        # which underlies ScaLapack does. It comes in several personalities;
        # we must supply a personality matching the MPI implementation that
        # is active for the root package that asked for ScaLapack.
        spec_root = self.spec.root
        if sys.platform == 'darwin' and '^mpich' in spec_root:
            # The only supported choice for MKL 2018 on Mac.
            blacs_lib = 'libmkl_blacs_mpich'
        elif '^openmpi' in spec_root:
            blacs_lib = 'libmkl_blacs_openmpi'
        elif '^mpich@1' in spec_root:
            # Was supported only up to 2015.
            blacs_lib = 'libmkl_blacs'
        elif ('^mpich@2:' in spec_root or
              '^mvapich2' in spec_root or
              '^intel-mpi' in spec_root):
            blacs_lib = 'libmkl_blacs_intelmpi'
        elif '^mpt' in spec_root:
            blacs_lib = 'libmkl_blacs_sgimpt'
        else:
            raise_lib_error('Cannot find a BLACS library for the given MPI.')

        int_suff = '_' + self.intel64_int_suffix
        scalapack_libnames = [
            'libmkl_scalapack' + int_suff,
            blacs_lib + int_suff,
        ]
        sca_libs = find_libraries(
            scalapack_libnames,
            root=self.component_lib_dir('mkl'),
            shared=('+shared' in self.spec))
        debug_print(sca_libs)

        if len(sca_libs) < 2:
            raise_lib_error(
                'Cannot locate ScaLapack/BLACS libraries:', scalapack_libnames)
        # NB: ScaLapack is installed as "cluster" components within MKL or
        # MKL-encompassing products.  But those were *optional* for the ca.
        # 2015/2016 product releases, which was easy to overlook, and I have
        # been bitten by that.  Thus, complain early because it'd be a sore
        # disappointment to have missing ScaLapack libs show up as a link error
        # near the end phase of a client package's build phase.

        return sca_libs

    # ---------------------------------------------------------------------
    # Support for virtual 'mpi'
    # ---------------------------------------------------------------------
    @property
    def compiler_wrappers_mpi(self):
        '''Return paths to compiler wrappers as dict by env-like names'''
        # Intel comes with 2 different flavors of MPI wrappers:
        #
        # * mpiicc, mpiicpc, and mpiifort are hardcoded to wrap around
        #   the Intel compilers.
        # * mpicc, mpicxx, mpif90, and mpif77 allow you to set which
        #   compilers to wrap using I_MPI_CC and friends. By default,
        #   wraps around the GCC compilers.
        #
        # In theory, these should be equivalent as long as I_MPI_CC
        # and friends are set to point to the Intel compilers, but in
        # practice, mpicc fails to compile some applications while
        # mpiicc works.
        bindir = self.component_bin_dir('mpi')
        if self.compiler.name == 'intel':
            return {
                # eschew Prefix notation to emphasize command strings.
                'MPICC':  os.path.join(bindir, 'mpiicc'),
                'MPICXX': os.path.join(bindir, 'mpiicpc'),
                'MPIF77': os.path.join(bindir, 'mpiifort'),
                'MPIF90': os.path.join(bindir, 'mpiifort'),
                'MPIFC':  os.path.join(bindir, 'mpiifort'),
            }
        else:
            return {
                'MPICC':  os.path.join(bindir, 'mpicc'),
                'MPICXX': os.path.join(bindir, 'mpicxx'),
                'MPIF77': os.path.join(bindir, 'mpif77'),
                'MPIF90': os.path.join(bindir, 'mpif90'),
                'MPIFC':  os.path.join(bindir, 'mpif90'),
            }

    # ---------------------------------------------------------------------
    # General support for child packages
    # ---------------------------------------------------------------------
    @property
    def headers(self):
        if '+mpi' in self.spec or self.provides('mpi'):
            return find_headers(
                ['mpi'],
                root=self.component_include_dir('mpi'),
                recursive=False)
        if '+mkl' in self.spec or self.provides('mkl'):
            return find_headers(
                ['mkl_cblas', 'mkl_lapacke'],
                root=self.component_include_dir('mkl'),
                recursive=False)

    @property
    def libs(self):
        if '+mpi' in self.spec or self.provides('mpi'):
            # If prefix is too general, recursive searches may get files from
            # supported but inappropriate sub-architectures like 'mic'.
            libnames = ['libmpifort', 'libmpi']
            if 'cxx' in self.spec.last_query.extra_parameters:
                libnames = ['libmpicxx'] + libnames
            return find_libraries(
                libnames,
                root=self.component_lib_dir('mpi'),
                shared=True, recursive=True)

    def setup_environment(self, spack_env, run_env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source parallel_studio_xe_2017/bin/psxevars.sh intel64
           [and likewise for MKL, MPI, and other components]
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment variables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.
        f = self.file_to_source
        if not f or not os.path.isfile(f):
            return

        tty.debug("sourcing " + f)

        if sys.platform == 'darwin':
            args = ()
        else:
            # All Intel packages expect at least the architecture as argument.
            # Some accept more args, but those are not (yet?) handled here.
            args = (_expand_fields('{arch}'),)

        run_env.extend(EnvironmentModifications.from_sourcing_file(f, *args))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '+mkl' in self.spec or self.provides('mkl'):
            # Spack's env philosophy demands that we replicate some of the
            # settings normally handled by file_to_source ...
            spack_env.set('MKLROOT', self.normalize_path('mkl'))
            spack_env.append_path('SPACK_COMPILER_EXTRA_RPATHS',
                                  self.component_lib_dir('mkl'))

        # NB: The 'mpi' providers must have their own (and unfortunately
        # dupliate) implementation of setup_dependent_environment() since they
        # need `spack_cc`, `spack_fc` etc., apparently inaccessible here:
        #   var/spack/repos/builtin/packages/intel-mpi/package.py
        #   var/spack/repos/builtin/packages/intel-parallel-studio/package.py

    def setup_dependent_package(self, module, dep_spec):
        if '+mpi' in self.spec or self.provides('mpi'):
            w = self.compiler_wrappers_mpi
            self.spec.mpicc  = w['MPICC']
            self.spec.mpicxx = w['MPICXX']
            self.spec.mpif77 = w['MPIF77']
            self.spec.mpifc  = w['MPIFC']

    # ---------------------------------------------------------------------
    # Specifics for installation phase
    # ---------------------------------------------------------------------
    @property
    def global_license_file(self):
        """Returns the path where a Spack-global license file should be stored.

        All Intel software shares the same license, so we store it in a
        common 'intel' directory."""
        return join_path(self.global_license_dir, 'intel',
                         os.path.basename(self.license_files[0]))

    @property
    def _determine_license_type(self):
        '''Provide license-related tokens for silent.cfg.'''
        # For license-related tokens, the following patters are relevant:
        #
        # anythingpat - any string
        # filepat     - the file location pattern (/path/to/license.lic)
        # lspat       - the license server address pattern (0123@hostname)
        # snpat       - the serial number pattern (ABCD-01234567)
        #
        # For more, see: ./README-intel.rst, section "licensing tokens"

        license_type = {}
        f = self.global_license_file
        if os.path.isfile(f):
            # Consider the spack-internal Intel license store *only*
            # when it has been populated.
            #
            # NB: Spack brings up $EDITOR in set_up_license() when
            # self.license_files been defined, regardless of
            # self.license_required. So, the "if" is usually True here.
            #
            # Reference:  lib/spack/spack/hooks/licensing.py
            #
            with open(f) as fh:
                if re.search(r'^[ \t]*[^' + self.license_comment + '\n]',
                             fh.read(), re.MULTILINE):
                    license_type = {
                        'ACTIVATION_TYPE': 'license_file',
                        'ACTIVATION_LICENSE_FILE': f,
                    }

        if not license_type:
            if [v for v in self.license_vars if v in os.environ]:
                license_type = {
                    'ACTIVATION_TYPE': 'exist_lic',
                }
            elif glob.glob('/opt/intel/licenses/*.lic'):
                # Searched for by default ($INTEL_LICENSE_FILE not even needed)
                license_type = {
                    'ACTIVATION_TYPE': 'exist_lic',
                }

        debug_print(license_type)
        return license_type

    def configure(self, spec, prefix):
        '''Generates the silent.cfg file to pass to installer.sh.

        See https://software.intel.com/en-us/articles/configuration-file-format
        '''

        # Both tokens AND values of the configuration file are validated during
        # the run of the underlying binary installer. Any unknown token or
        # unacceptable value will cause that installer to fail.  Notably, this
        # applies to trying to specify a license for a product that does not
        # require one.
        #
        # Fortunately, the validator is a script from a solid code base that is
        # only lightly adapted to the token vocabulary of each product and
        # release.  Let's get that script so we can preempt its objections.
        #
        # Rather than running the script on a trial file and dissecting its
        # pronouncements, let's brazenly skim it for supported tokens and build
        # our configuration accordingly. We can do this because the tokens are
        # quite long and specific.

        validator_code = open('pset/check.awk', 'r').read()
        # Let's go a little further and distill the tokens (plus some noise).
        tokenlike_words = set(re.findall(r'[A-Z_]{4,}', validator_code))

        # NB: .cfg files generated with the "--duplicate filename" option have
        # the COMPONENTS string begin with a separator - do not worry about it.
        components_joined = ';'.join(self._filtered_components)
        nonrpm_db_dir = join_path(prefix, 'nonrpm-db')

        config_draft = {
            # Basics first - these should be accepted in all products.
            'ACCEPT_EULA':                          'accept',
            'PSET_MODE':                            'install',
            'CONTINUE_WITH_OPTIONAL_ERROR':         'yes',
            'CONTINUE_WITH_INSTALLDIR_OVERWRITE':   'yes',
            'SIGNING_ENABLED':                      'no',

            # Highly variable package specifics:
            'PSET_INSTALL_DIR':                     prefix,
            'NONRPM_DB_DIR':                        nonrpm_db_dir,
            'COMPONENTS':                           components_joined,

            # Conditional tokens; the first is supported post-2015 only.
            # Ignore ia32; most recent products don't even provide it.
            'ARCH_SELECTED':                        'INTEL64',   # was: 'ALL'

            # 'ism' component -- see uninstall_ism(); also varies by release.
            'PHONEHOME_SEND_USAGE_DATA':            'no',
            # Ah, as of 2018.2, that somewhat loaded term got replaced by one
            # in business-speak. We uphold our preference, both out of general
            # principles and for technical reasons like overhead and non-routed
            # compute nodes.
            'INTEL_SW_IMPROVEMENT_PROGRAM_CONSENT': 'no',
        }
        # Deal with licensing only if truly needed.
        # NB: Token was 'ACTIVATION' pre ~2013, so basically irrelevant here.
        if 'ACTIVATION_TYPE' in tokenlike_words:
            config_draft.update(self._determine_license_type)

        # Write sorted *by token* so the file looks less like a hash dump.
        f = open('silent.cfg', 'w')
        for token, value in sorted(config_draft.items()):
            if token in tokenlike_words:
                f.write('%s=%s\n' % (token, value))
        f.close()

    def install(self, spec, prefix):
        """Runs the install.sh installation script."""

        install_script = Executable('./install.sh')
        install_script('--silent', 'silent.cfg')

    @run_after('install')
    def configure_rpath(self):
        if '+rpath' not in self.spec:
            return

        # https://software.intel.com/en-us/cpp-compiler-18.0-developer-guide-and-reference-using-configuration-files
        compilers_bin_dir = self.component_bin_dir('compiler')
        compilers_lib_dir = self.component_lib_dir('compiler')

        for compiler_name in 'icc icpc ifort'.split():
            f = os.path.join(compilers_bin_dir, compiler_name)
            if not os.path.isfile(f):
                raise InstallError(
                    'Cannot find compiler command to configure rpath:\n\t' + f)

            compiler_cfg = os.path.abspath(f + '.cfg')
            with open(compiler_cfg, 'w') as fh:
                fh.write('-Xlinker -rpath={0}\n'.format(compilers_lib_dir))

    @run_after('install')
    def filter_compiler_wrappers(self):
        if (('+mpi' in self.spec or self.provides('mpi')) and
                '~newdtags' in self.spec):
            bin_dir = self.component_bin_dir('mpi')
            for f in 'mpif77 mpif90 mpigcc mpigxx mpiicc mpiicpc ' \
                     'mpiifort'.split():
                f = os.path.join(bin_dir, f)
                filter_file('-Xlinker --enable-new-dtags', ' ', f, string=True)

    @run_after('install')
    def preserve_cfg(self):
        """Copies the silent.cfg configuration file to <prefix>/.spack."""
        install('silent.cfg', join_path(self.prefix, '.spack'))

    @run_after('install')
    def uninstall_ism(self):
        # The "Intel(R) Software Improvement Program" [ahem] gets installed,
        # apparently regardless of PHONEHOME_SEND_USAGE_DATA.
        #
        # https://software.intel.com/en-us/articles/software-improvement-program
        # https://software.intel.com/en-us/forums/intel-c-compiler/topic/506959
        # Hubert H. (Intel)  Mon, 03/10/2014 - 03:02 wrote:
        #  "... you can also uninstall the Intel(R) Software Manager
        #  completely: <installdir>/intel/ism/uninstall.sh"

        f = join_path(self.normalize_path('ism'), 'uninstall.sh')
        if os.path.isfile(f):
            tty.warn('Uninstalling "Intel Software Improvement Program"'
                     'component')
            uninstall = Executable(f)
            uninstall('--silent')

        # TODO? also try
        #   ~/intel/ism/uninstall --silent

        debug_print(os.getcwd())
        return

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
