##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
    install, join_path, ancestor, \
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


def _valid_components():
    """A generator that yields valid components."""

    tree = ET.parse('pset/mediaconfig.xml')
    root = tree.getroot()

    components = root.findall('.//Abbr')
    for component in components:
        yield component.text


class IntelPackage(PackageBase):
    """Specialized class for licensed Intel software.

    This class provides two phases that can be overridden:

    1. :py:meth:`~.IntelPackage.configure`
    2. :py:meth:`~.IntelPackage.install`

    They both have sensible defaults and for many packages the
    only thing necessary will be to override ``setup_environment``
    to set the appropriate environment variables.
    """
    #: Phases of an Intel package
    phases = ['configure', 'install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'IntelPackage'

    #: By default, we assume that all Intel software requires a license.
    #: This can be overridden for packages that do not require a license.
    license_required = True

    #: Comment symbol used in the ``license.lic`` file
    license_comment = '#'

    #: Location where Intel searches for a license file
    license_files = ['Licenses/license.lic']

    #: Environment variables that Intel searches for a license file
    license_vars = ['INTEL_LICENSE_FILE']

    #: URL providing information on how to acquire a license key
    license_url = 'https://software.intel.com/en-us/articles/intel-license-manager-faq'

    #: Components of the package to install.
    #: By default, install 'ALL' components.
    components = ['ALL']

    @property
    def _filtered_components(self):
        """Returns a list or set of valid components that match
        the requested components from ``components``."""

        # Don't filter 'ALL'
        if self.components == ['ALL']:
            return self.components

        # mediaconfig.xml is known to contain duplicate components.
        # If more than one copy of the same component is used, you
        # will get an error message about invalid components.
        # Use a set to store components to prevent duplicates.
        matches = set()

        for valid in _valid_components():
            for requested in self.components:
                if valid.startswith(requested):
                    matches.add(valid)

        return matches

    @property
    def _want_shared(self):
        return ('+shared' in self.spec)

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

    # ---------------------------------------------------------------------
    # Directory handling common to all Intel components
    # ---------------------------------------------------------------------
    def product_dir(self, product_dir_name, version_glob='_*.*.*',
                    postfix_dir=''):
        '''Returns the version-specific directory of an Intel product release,
        holding the main product and possibly auxiliary files from other
        products.

        Arguments:

        ``product_dir_name``
            Name of component directory, without a numeric version.

            - Supported::
                compilers_and_libraries, parallel_studio_xe
            - TBD::
                advisor_xe, composer_xe, inspector_xe, vtune_amplifier_xe,
                performance_snapshots

        ``version_glob``
            A glob pattern that fully qualifies ``product_dir_name`` to a
            specific version within an actual directory (not a symlink).

        ``postfix_dir``
            Subdirectory below ``product_dir_name + version_glob``.
            Example:
                ``('compilers_and_libraries', postfix_dir='linux')``
        '''
        # See ./README-intel.rst for background and analysis of dir layouts.

        d = self.prefix
        if sys.platform == 'darwin':
            # TODO: Verify on Mac.
            return d

        # Distinguish between product installations that were done external to
        # Spack (integrated via packages.yaml) and Spack-internal ones. The
        # resulting prefixes may differ in directory depth and specificity.
        if ('%s_' % product_dir_name) in d and '.' in d:
            # If e.g. MKL was installed outside of Spack, it is likely just one
            # product or product component among possibly many other Intel
            # products and their releases that were installed in sibling or
            # cousin directories.  In such cases, the prefix given to Spack
            # will inevitably be a highly product-specific and preferably fully
            # version-specific directory.  This is what we want and need.
            pass
        elif product_dir_name in d:
            # The Intel installer scripts try hard to place compatibility links
            # named like this in the install dir to convey upgrade benefits to
            # traditional client apps. But such a generic name can be trouble
            # when given to Spack: the link target is bound to change outside
            # of Spack's purview and when it does, the outcome of subsequent
            # builds of dependent packages may be affected. (Though Intel has
            # been remarkably good at backward compatibility.)
            # I'm not sure if Spack's package hashing includes link targets.
            #
            # NB: Code may never be reached if self.prefix is abspath()'ed!?
            # NB2: Warning could get tiresome without a seen++ test.
            #
            # tty.warn('Intel product found in a version-neutral directory - '
            #          'future builds may not be reproducible.')
            pass
        else:
            # By contrast, a Spack-born MKL installation will inherit its
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
            matching_dirs = glob.glob(
                join_path(d, product_dir_name + version_glob))

            if matching_dirs:
                # Take the highest and thus presumably newest match, which
                # better be the sole one anyway.
                d = Prefix(matching_dirs[-1])
            else:
                # No match -- this *will* happen during pre-build
                # setup_environment() when the destination dir is still empty.
                # Return a sensible value anyway.
                d = Prefix(join_path(d, product_dir_name))

            # Alright, now the final flight of stairs.
            # NB: A Spack-external package should have this in prefix already,
            # so it's only applied here, for Spack-internal requests.
            d = Prefix(join_path(d, postfix_dir))

        debug_print(d)
        return d

    @property
    def compilers_dir(self):
        # TODO? accommodate other platforms(?)
        platform = 'linux'
        d = self.product_dir('compilers_and_libraries', postfix_dir=platform)

        # On my system, when using a external MKL, self.prefix showed up as
        # ending with "/compiler". I think this is because I provided that MKL
        # by means of the side effect of loading an env. module for the Intel
        # *compilers*, and Spack inspects $PATH(?) Well, I can live with that!
        # It's just a jump to the left, and then a step to the right; let's do
        # the time warp again:
        #
        # Ahem, apparently, the Prefix class lacks a native parent() method
        # (kinda understandably so), and the syntax blows up on trying "..".
        #
        # NB: Targeting a platform, we can indulge in hardcoding the path sep.
        platform_dir = '/' + platform
        while platform_dir in d and not d.endswith(platform_dir):
            d = Prefix(ancestor(d))

        debug_print(d)
        return d

    @property
    def studio_dir(self):
        # The Parallel Studio dir as such holds mostly symlinks to other
        # components, so it's rarely needed, except for, ta-da, psxevars.sh.

        d = self.product_dir('parallel_studio_xe', postfix_dir='')
        #  NODO: The sole 2015 "composer" version in the Spack repos (as of
        #  2018-02) would in fact need:
        # d = self.product_dir('composer_xe', postfix_dir='')
        #  But a site running Spack likely has the successors licensed, right?

        debug_print(d)
        return d

    def component_dir(self, component=None):
        '''Returns the directory of a product component, appropriate for
        presenting to users in environment variables like MKLROOT and
        I_MPI_ROOT, or the product dir itself (when the component is not
        evident from the package name and wasn't specified).
        '''
        # Assign early so advanced add-ons (VTune, Advisor, ...) can override.
        d = self.compilers_dir

        if component is None:
            # For ref.: Intel packages in Spack-0.11 (not using current func.):
            #
            #  intel/               intel-ipp/          intel-mpi/
            #  intel-daal/          intel-mkl/          intel-parallel-studio
            #  intel-gpu-tools/     intel-mkl-dnn/      intel-tbb/
            #
            if self._is_personality('mkl'):
                component = 'mkl'
            elif self._is_personality('mpi'):
                component = 'mpi'
                # Note analysis of MPI dir in ./README-intel.rst :
                # Since both I_MPI_ROOT and MANPATH need the 'mpi' dir, do NOT
                # qualify further.
                # NODO: d = d.intel64
            # elif ...
            #     component = ...
            else:
                component = 'compiler'

        d = Prefix(join_path(d, component))
        debug_print(d)
        return d

    def component_bin_dir(self, component=None, relative=False):
        d = self.component_dir(component)

        if sys.platform == 'darwin':
            # TODO: verify
            d = d.bin
        else:
            if self._is_personality('mpi', component):
                d = d.intel64.bin
            elif component == 'compiler' or 'parallel-studio' in self.name:
                d = Prefix(ancestor(d)).bin.intel64
                # NB: psxevars.sh is wrested specially from studio_dir, in
                # intel-parallel-studio/package.py:file_to_source
            else:
                d = d.bin

        if relative:
            d = self.relative_path(d)

        debug_print(d)
        return d

    def component_lib_dir(self, component=None, relative=False):
        '''Provide directory suitable for find_libraries() and
        SPACK_COMPILER_EXTRA_RPATHS.
        '''
        d = self.component_dir(component)

        if sys.platform == 'darwin':
            d = d.lib
        else:
            if self._is_personality('mpi', component):
                d = d.intel64.lib
            else:
                d = d.lib.intel64

        if self._is_personality('tbb', component):
            # Must qualify further
            d = Prefix(join_path(d, self._tbb_abi))

        if relative:
            d = self.relative_path(d)

        debug_print(d)
        return d

    @property
    def component_include_dir(self, component=None, relative=False):
        d = self.component_dir(component)

        if self._is_personality('mpi', component):
            d = d.intel64
        d = d.include

        if relative:
            d = self.relative_path(d)

        debug_print(d)
        return d

    # ---------------------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------------------
    def _is_personality(self, nominal_component, component=None,
        accept_variant=None):
        '''Provide the Intel component as explicitly requested in
        ``component``, or, when called as virtual package, provide the
        appropriate component.
        '''
        # This part acts as a mere macro for equality testing.
        if nominal_component == component:
            return True

        # This part is both the fallback for the personality test and the
        # inverse for "provides()" in child packages.
        satisfies = {
            'mkl': r'intel-mkl|mkl|blas|lapack|scalapack',
            'mpi': r'intel-mpi|mpi',
            'tbb': r'intel-tbb|tbb',
        }
        try:
            return (bool(re.match(satisfies[nominal_component], self.name)) or
                    (accept_variant and accept_variant in self.spec))
        except KeyError:
            raise InstallError("Support for component '%s' not available." %
                               nominal_component)

    def _locate_script(self, filename):
        debug_print(filename)
        if filename.startswith('/'):
            return filename             # absolute path - no need to search

        c = self.component_dir()
        if not c or not os.path.isdir(c):       # does not exist during pre-install
            debug_print("Cannot (yet) locate " + str(filename))
            return

        # Line up low-hanging fruit first:
        try_dirs = [
            join_path(c, 'bin'),
            self.component_bin_dir(),   # not necessariliy the same as c/'bin'
            c,
        ]
        # Add others:
        try_dirs.extend(glob.glob(join_path(self.component_dir(), '*')))
        # debug_print(try_dirs)

        # Too bad we can't simply write: .. in [foo, bar, glob.glob(baz)]
        for d in try_dirs:
            f = join_path(d, filename)
            if os.path.isfile(f):
                return f

    def relative_path(self, file_or_dir, relative_to=''):
        if not relative_to:
            relative_to = self.prefix
        file_or_dir = os.path.realpath(file_or_dir)
        relative_to = os.path.realpath(relative_to)
        p = os.path.relpath(file_or_dir, relative_to)
        return p

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
                root=self.component_lib_dir(component='compiler'),
                shared=self._want_shared)
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

        tbb_lib = find_libraries(
            ['libtbb'], root=self.component_lib_dir(component='tbb'))
        # NB: shared=False is not and has never been supported for TBB:
        # https://www.threadingbuildingblocks.org/faq/there-version-tbb-provides-statically-linked-libraries
        #
        # NB2: Like icc with -qopenmp, so does icpc steer us towards using an
        # option: "icpc -tbb"

        # TODO: clang
        gcc = Executable('gcc')     # must be gcc, not self.compiler.cc
        cxx_lib_path = gcc(
            '--print-file-name', 'libstdc++.%s' % dso_suffix, output=str)

        libs = tbb_lib + LibraryList(cxx_lib_path)
        debug_print(libs)
        return libs

    def _tbb_abi(self):
        '''Select the ABI needed for linking TBB'''
        # Match the available gcc (or clang?), as it's done in tbbvars.sh.

        # TODO: clang
        gcc = Executable('gcc')
        matches = re.search(r'gcc.* ([0-9]+\.[0-9]+\.[0-9]+).*',
                            gcc('--version', output=str))
        if matches:
            gcc_version = Version(matches.groups()[0])
            if gcc_version >= Version('4.7'):
                abi = 'gcc4.7'
            elif gcc_version >= Version('4.4'):
                abi = 'gcc4.4'
        else:
            abi = 'gcc4.1'     # unlikely, one hopes.

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
        elif self.spec.satisfies('threads=tbb'):    # TODO: allow in MKL
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
            root=self.component_lib_dir(component='mkl'),
            shared=self._want_shared)
        debug_print(mkl_libs)

        if len(mkl_libs) < 3:
            raise_lib_error('Cannot locate core MKL libraries:', mkl_libnames)

        # The Intel MKL link line advisor recommends these system libraries
        system_libs = find_system_libraries(
            'libpthread libm libdl'.split(),
            shared=self._want_shared)
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
            root=self.component_lib_dir(component='mkl'),
            shared=self._want_shared)
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
    # Support for virtual 'mpi' and 'mkl'
    # ---------------------------------------------------------------------
    @property
    def mpi_libs(self):
        # If prefix is too general, recursive searches may get file variants
        # from supported but inappropriate sub-architectures like 'mic'.
        libnames = ['libmpifort', 'libmpi']
        if 'cxx' in self.spec.last_query.extra_parameters:
            libnames = ['libmpicxx'] + libnames
        return find_libraries(libnames,
                              root=self.component_lib_dir(component='mpi'),
                              shared=True, recursive=True)

    @property
    def mpi_headers(self):
        return find_headers('mpi',
                            root=self.component_include_dir(component='mpi'),
                            recursive=False)

    @property
    def mkl_headers(self):
        return find_headers(['mkl_cblas', 'mkl_lapacke'],
                            root=self.component_include_dir(component='mkl'),
                            recursive=False)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if self._is_personality('mkl', accept_variant='+mkl'):
            # BTW: The name and meaning of the 'root=' keyword arg of
            # find_libraries() entices us to feed it an "mkl_root" variable,
            # but that is a siren song that pulls us down and under from the
            # true MKLROOT. Hence, such a variable name is not used here
            # [anymore].
            spack_env.set('MKLROOT', self.component_dir(component='mkl'))
            spack_env.append_path('SPACK_COMPILER_EXTRA_RPATHS',
                                  self.component_lib_dir(component='mkl'))

        # Hmm, +mpi would be nice to handle here as well but unification from:
        #   var/spack/repos/builtin/packages/intel-mpi/package.py
        #   var/spack/repos/builtin/packages/intel-parallel-studio/package.py
        # fails because flake8 says spack_cc & friends are undefined - grep(1)
        # failed me in determining where these are defined.
        #
        # if '+mpi' in self.spec or 'intel-mpi' in self.name:
        #   spack_env.set('I_MPI_CC', spack_cc)
        #   spack_env.set('I_MPI_CXX', spack_cxx)
        #   spack_env.set('I_MPI_F77', spack_fc)
        #   spack_env.set('I_MPI_F90', spack_f77)
        #   spack_env.set('I_MPI_FC', spack_fc)
        #   # Convenience variable.
        #   spack_env.set('I_MPI_ROOT', self.component_dir(component='mpi'))

    def setup_dependent_package(self, module, dep_spec):
        if self._is_personality('mpi', accept_variant='+mpi'):
            # Intel comes with 2 different flavors of MPI wrappers:
            #
            # * mpiicc, mpiicpc, and mpifort are hardcoded to wrap around
            #   the Intel compilers.
            # * mpicc, mpicxx, mpif90, and mpif77 allow you to set which
            #   compilers to wrap using I_MPI_CC and friends. By default,
            #   wraps around the GCC compilers.
            #
            # In theory, these should be equivalent as long as I_MPI_CC
            # and friends are set to point to the Intel compilers, but in
            # practice, mpicc fails to compile some applications while
            # mpiicc works.
            bindir = self.component_bin_dir(component='mpi')
            if self.compiler.name == 'intel':
                self.spec.mpicc  = bindir.mpiicc
                self.spec.mpicxx = bindir.mpiicpc
                self.spec.mpifc  = bindir.mpiifort
                self.spec.mpif77 = bindir.mpiifort
            else:
                self.spec.mpicc  = bindir.mpicc
                self.spec.mpicxx = bindir.mpicxx
                self.spec.mpifc  = bindir.mpif90
                self.spec.mpif77 = bindir.mpif77

    # ---------------------------------------------------------------------
    # General support for child packages
    # ---------------------------------------------------------------------
    def headers(self):
        if self._is_personality('mpi', accept_variant='+mpi'):
            return self.mpi_headers()
        if self._is_personality('mkl', accept_variant='+mkl'):
            return self.mkl_headers()

    def libs(self):
        if self._is_personality('mpi', accept_variant='+mpi'):
            return self.mpi_libs()

    def setup_environment(self, spack_env, run_env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source parallel_studio_xe_2017/bin/psxevars.sh intel64
           [and likewise for MKL, MPI, and other components]
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment v=ariables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.

        f = self._locate_script(self.file_to_source)
        debug_print('sourcing ' + str(f))
        if not f or not os.path.isfile(f):
            return

        if sys.platform == 'darwin':
            run_env.extend(
                EnvironmentModifications.from_sourcing_file(f))
        else:
            run_env.extend(
                EnvironmentModifications.from_sourcing_file(f, 'intel64'))

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
        '''Provide license-related tokens for ``silent.cfg``.'''
        # See also: ./README-intel.rst, section "licensing tokens"

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
        """Writes the ``silent.cfg`` file used to configure the installation.

        See https://software.intel.com/en-us/articles/configuration-file-format
        """
        # Patterns used to check silent configuration file
        #
        # anythingpat - any string
        # filepat     - the file location pattern (/path/to/license.lic)
        # lspat       - the license server address pattern (0123@hostname)
        # snpat       - the serial number pattern (ABCD-01234567)

        components_joined = ';'.join(self._filtered_components)
        config = {
            'ACCEPT_EULA':                          'accept',
            'CONTINUE_WITH_OPTIONAL_ERROR':         'yes',
            'PSET_INSTALL_DIR':                     prefix,
            'CONTINUE_WITH_INSTALLDIR_OVERWRITE':   'yes',
            'COMPONENTS':                           components_joined,
            'PSET_MODE':                            'install',
            'NONRPM_DB_DIR':                        prefix,
            'SIGNING_ENABLED':                      'no',
            'ARCH_SELECTED':                        'ALL',
        }

        # Not all Intel software requires a license. Trying to specify
        # one anyway will cause the installation to fail.
        # Ditto for PHONEHOME_SEND_USAGE_DATA.
        if self.license_required:
            config.update(self._determine_license_type)
            config.update({'PHONEHOME_SEND_USAGE_DATA': 'no'})

        with open('silent.cfg', 'w') as cfg:
            for key in config:
                cfg.write('{0}={1}\n'.format(key, config[key]))

    def install(self, spec, prefix):
        """Runs the ``install.sh`` installation script."""

        install_script = Executable('./install.sh')
        install_script('--silent', 'silent.cfg')

    @run_after('install')
    def save_silent_cfg(self):
        """Copies the silent.cfg configuration file to ``<prefix>/.spack``."""
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

        f = join_path(self.studio_dir, 'ism', 'uninstall.sh')
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
