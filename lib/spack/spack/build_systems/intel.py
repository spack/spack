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
import inspect
import xml.etree.ElementTree as ET
import llnl.util.tty as tty

from llnl.util.filesystem import \
    install, join_path, ancestor, \
    LibraryList, find_headers, find_libraries, find_system_libraries

from spack.package import PackageBase, run_after, InstallError
from spack.util.executable import Executable
from spack.util.prefix import Prefix
from spack.build_environment import dso_suffix
from spack.environment import EnvironmentModifications


# A couple of utility functions that might be useful in general. If so, they
# should really be defined elsewhere, unless deemed heretical.
# (Or na"ive on my part).

def debug_print(msg):
    '''Prints a message (usu. a variable) and the callers' names for a couple
    of stack frames.
    '''
    # https://docs.python.org/2/library/inspect.html#the-interpreter-stack
    stack = inspect.stack()
    _func_name = 3
    tty.debug("%s.%s:\t%s" % (stack[2][_func_name], stack[1][_func_name], msg))


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
        application's int size.

            ilp64: all of int, long, and pointer are 64 bit.
             lp64: only long and pointer are 64 bit; int will be 32bit.
        '''
        if '+ilp64' in self.spec:
            return 'ilp64'
        else:
            return 'lp64'

    #--------------------------------------------------------------------
    # Analysis of the directory layout for a Spack-born installation of
    # intel-mkl@2018.1.163
    #--------------------------------------------------------------------
    #
    #   $ ls -l <prefix>
    #   # Unix metadata removed, entries rearranged, "->" still means symlink.
    #
    #   bin/
    #       - compilervars.*sh (symlinked) ONLY
    #
    #   compilers_and_libraries -> compilers_and_libraries_2018
    #       - generically-named entry point, stable across versions (one hopes)
    #
    #   compilers_and_libraries_2018/
    #       - vaguely-versioned dirname, holding a stub hierarchy --ignorable
    #
    #       $ ls -l compilers_and_libraries_2018/linux/
    #       bin         - actual compilervars.*sh (reg. files) ONLY
    #       documentation -> ../../documentation_2018/
    #       lib -> ../../compilers_and_libraries_2018.1.163/linux/compiler/lib/
    #       mkl -> ../../compilers_and_libraries_2018.1.163/linux/mkl/
    #       pkg_bin -> ../../compilers_and_libraries_2018.1.163/linux/bin/
    #       samples -> ../../samples_2018/
    #       tbb -> ../../compilers_and_libraries_2018.1.163/linux/tbb/
    #
    #   compilers_and_libraries_2018.1.163/
    #       - Main "product" + a minimal set of libs from related products
    #
    #       $ ls -l compilers_and_libraries_2018.1.163/linux/
    #       bin/        - compilervars.*sh, link_install*sh  ONLY
    #       mkl/        - Main Product ==> to be assigned to MKLROOT
    #       compiler/   - lib/intel64_lin/libiomp5*  ONLY
    #       tbb/        - tbb/lib/intel64_lin/gcc4.[147]/libtbb*.so* ONLY
    #
    #   parallel_studio_xe_2018 -> parallel_studio_xe_2018.1.038/
    #   parallel_studio_xe_2018.1.038/
    #       - Alternate product packaging - ignorable
    #
    #       $ ls -l parallel_studio_xe_2018.1.038/
    #       bin/               - actual psxevars.*sh (reg. files)
    #       compilers_and_libraries_2018 -> <full_path>/comp...aries_2018.1.163
    #       documentation_2018 -> <full_path_prefix>/documentation_2018
    #       samples_2018 -> <full_path_prefix>/samples_2018
    #       ...
    #
    #   documentation_2018/
    #   samples_2018/
    #   lib -> compilers_and_libraries/linux/lib/
    #   mkl -> compilers_and_libraries/linux/mkl/
    #   tbb -> compilers_and_libraries/linux/tbb/
    #                   - auxiliaries and convenience links
    #
    #--------------------------------------------------------------------
    # Directory analysis for intel-mpi@2018.1.163
    #--------------------------------------------------------------------
    # For MPI, the layout is slightly different than MKL. The prefix will have
    # to include the sub-arch, which contains bin/, lib/, ..., all without
    # further arch splits. I_MPI_ROOT, however, must be the package dir.
    #
    # FIXME: For MANPATH, need the parent dir.
    #
    #   $ ls -lF /opt/intel/compilers_and_libraries_2018.1.163/linux/mpi/
    #   bin64 -> intel64/bin/
    #   etc64 -> intel64/etc/
    #   include64 -> intel64/include/
    #   lib64 -> intel64/lib/
    #
    #   benchmarks/
    #   binding/
    #   intel64/
    #   man/
    #   test/
    #
    #   MPI-2019 preview; Relnotes contain: "File structure clean-up."
    #   https://software.intel.com/en-us/articles/restoring-legacy-path-structure-on-intel-mpi-library-2019
    #
    #   $ ls -lF /opt/intel/compilers_and_libraries_2018.1.163/linux/mpi_2019/
    #   binding/
    #   doc/
    #   imb/
    #   intel64/
    #   man/
    #   test/
    #
    #--------------------------------------------------------------------
    # Spack-external installation of intel-parallel-studio :
    #--------------------------------------------------------------------
    #
    # This is a product bundle whose install dir mostly holds merely symlinks
    # to components installed in sibling dirs:i
    #
    #   $ ls -lF /opt/intel/parallel_studio_xe_2018.1.038/
    #   advisor_2018		 -> /opt/intel/advisor_2018/
    #   clck_2018		 -> /opt/intel/clck/2018.1/
    #   compilers_and_libraries_2018 -> /opt/intel/comp....aries_2018.1.163/
    #   documentation_2018	 -> /opt/intel/documentation_2018/
    #   ide_support_2018	 -> /opt/intel/ide_support_2018/
    #   inspector_2018		 -> /opt/intel/inspector_2018/
    #   itac_2018		 -> /opt/intel/itac/2018.1.017/
    #   man		         -> /opt/intel/man/
    #   samples_2018		 -> /opt/intel/samples_2018/
    #   vtune_amplifier_2018	 -> /opt/intel/vtune_amplifier_2018/
    #
    #   psxevars.csh		 -> ./bin/psxevars.csh*
    #   psxevars.sh		 -> ./bin/psxevars.sh*
    #   bin/            - *vars.*sh scripts + sshconnectivity.exp ONLY
    #
    #   licensing/
    #   uninstall*
    #
    # The only relevant regular files are *vars.*sh, but those also just churn
    # through the subordinate vars files of the components.
    #
    #--------------------------------------------------------------------
    #
    # Note on macOS support, i.e., sys.platform == 'darwin':
    #
    # - On macOS, the Spack methods here only include support to integrate an
    #   externally installed MKL.
    #
    # - URLs in child packages will be Linux-specific; macOS download packages
    #   are located in differently numbered dirs and are named m_*.dmg.
    #
    #--------------------------------------------------------------------

    @property
    def compilers_dir(self):
        '''Returns the version-specific directory of an Intel product release,
        holding the main product and auxiliary files from other products.
        '''
        # NB: The grab-baggish "intel-parallel-studio" overwrites this method.
        d = self.prefix
        if sys.platform == 'darwin':
            # TODO: Verify on Mac.
            return d

        # Distinguish between product installations that were done outside of
        # Spack (as "ghost package" integrated via packages.yaml) and
        # Spack-native ones. The key issue is that their prefixes will
        # qualitatively differ in directory depth.
        if 'compilers_and_libraries_' in d and '.' in d:
            # When MKL was installed outside of Spack, it is likely just one
            # product or product component among possibly many other Intel
            # products and their releases that were installed in sibling or
            # cousin directories.  In such cases, the prefix given to Spack
            # will inevitably be a highly product-specific and preferably fully
            # version-specific directory.  This is what we want and need.
            pass
        elif 'compilers_and_libraries' in d:
            # The Intel installer scripts try hard to place compatibility links
            # named like this in the install dir to convey upgrade benefits to
            # traditional client apps. But such a generic name can be trouble
            # when given to Spack: the link target is bound to change outside
            # of Spack's purview and when it does, the outcome of subsequent
            # builds of dependent packages may be affected. (Though Intel has
            # been remarkably good at backward compatibility.)
            # I'm not sure if Spack's package hashing includes link targets.
            # NB: Code may never be reached if self.prefix is abspath()'ed!?
            tty.warn('Intel product found in a version-neutral directory - '
                     'future builds may not be reproducible.')
            pass
        else:
            # By contrast, a Spack-born MKL installation will inherit its
            # prefix from install.sh of Intel's package distribution, where it
            # means the high-level installation directory that is specific to
            # the *vendor* (think of the default "/opt/intel"). We must now
            # step down into the *product* directory to get the usual
            # hierarchy, but let's not do that in haste ...
            d = d.compilers_and_libraries

            # For a Spack-born install, using the fully-qualified release
            # directory that is so desired above is possible but far less
            # important since product upgrades won't land in the same parent.
            # To force it nonetheless, uncomment the following:
            #d = Prefix(d.append('_' + self.version))

            # Alright, now the final flight of stairs.
            d = d.linux

        # TODO? accomodate other platforms(?)

        # On my system, using a ghosted MKL, self.prefix showed up as ending
        # with "/compiler". I think this is because I provide that MKL by means
        # of the side effect of loading an env. module for the Intel
        # *compilers*, and Spack inspects $PATH(?) Well, I can live with that!
        # It's just a jump to the left, and then a step to the right; let's do
        # the time warp again:
        #
        # Ahem, apparently, the Prefix class lacks a native parent() method
        # (kinda understandably so), and the syntax blows up on trying "..".
        #
        # NB: Searching by platform, we can indulge in hardcoding the path sep.
        while '/linux' in d and not d.endswith('/linux'):
            d = Prefix(ancestor(d))

        debug_print(d)
        return d

    @property
    def studio_dir(self):
        # The Parallel Studio dir as such holds mostly symlinks to other
        # components, so it's rarely needed, except for, ta-da, psxevars.sh.
        d = self.prefix
        if sys.platform == 'darwin':
            # TODO: verify (if even applicable)
            return d

        if 'parallel_studio' in d:
            # Package was likely installed outside of Spack; see lenghty
            # explanation in parent's compilers_dir().
            pass
        else:
            # Spack-born installation
            year = str(self.version[1])
            update_num = str(self.version[2])
            # Further version components in the full directory name (Intel's
            # internal build number and possibly more) are usually not in the
            # user-declared version and are not easily apparent either.
            v_dir_fuzzy = 'parallel_studio_xe_%s' % year
            v_dir_glob = '%s.%s*' % (v_dir_fuzzy, update_num)

            version_dirs = glob.glob(join_path(d, v_dir_glob))
            if version_dirs:
                # Take highest match, hopefully being the sole one or at least
                # the newest.
                d = Prefix(version_dirs[-1])
            else:
                # Will happen during pre-build call of setup_environment()
                d = Prefix(join_path(d, v_dir_fuzzy))
        debug_print(d)
        return d

    def component_dir(self, component=None):
        '''Returns the directory of a product component, appropriate for
        presenting to users in environment variables like MKLROOT and
        I_MPI_ROOT, or the product dir itself (when the component not evident
        from the package name and wasn't specified).
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
            if 'intel-mkl' in self.name:
                component = 'mkl'
            elif 'intel-mpi' in self.name:
                component = 'mpi'
                # Note analysis of MPI dir above:  Since both I_MPI_ROOT and
                # MANPATH need the 'mpi' dir, do NOT qualify further.
                #NODO: d = d.intel64
            #elif ...
            #    component = ...
            else:
                component = 'compiler'

        d = Prefix(join_path(d, component))
        debug_print(d)
        return d

    def component_bin_dir(self, component=None):
        d = self.component_dir(component)

        if sys.platform == 'darwin':
            # TODO: verify
            d = d.bin
        else:
            if component == 'mpi' or 'intel-mpi':
                d = d.intel64.bin
            elif component == 'compiler' or 'parallel-studio' in self.name:
                d = Prefix(ancestor(d)).bin.intel64
                # NB: psxevars.sh is wrested specially from studio_dir, in
                # intel-parallel-studio/package.py:file_to_source
            else:
                d = d.bin

        debug_print(d)
        return d

    def component_lib_dir(self, component=None):
        # Provide starting directory for find_libraries() and
        # SPACK_COMPILER_EXTRA_RPATHS.
        d = self.component_dir(component)

        if sys.platform == 'darwin':
            d = d.lib
        else:
            if component == 'mpi' or 'intel-mpi' in self.name:
                d = d.intel64.lib
            else:
                d = d.lib.intel64
            # A bit weird, but  I'm sure there are good reasons for it.

        debug_print(d)
        return d

    @property
    def component_include_dir(self, component=None):
        d = self.component_dir(component)

        if component == 'mpi' or 'intel-mpi' in self.name:
            d = d.intel64
        d = d.include

        debug_print(d)
        return d

    @property
    def omp_libs(self):
        # Supply LibraryList for linking OpenMP

        # FIXME  if sys.platform == 'darwin' ....

        # TODO?  Across Spack packages for "client" applications, are variants
        #   named consistently enough to determine if OpenMP is even needed?

        if '%intel' in self.spec:
            omp_libnames = ['libiomp5']

            # Note about search root: For MKL, the directory
            # "$MKLROOT/../compiler" will be present even for an MKL-only
            # product installation (as opposed to one being ghosted via
            # packages.yaml), specificially to provide the 'iomp5' libs.

            omp_libs = find_libraries(
                omp_libnames,
                root=self.component_lib_dir(component='compiler'),
                shared=self._want_shared)

        elif '%gcc' in self.spec:
            gcc = Executable(self.compiler.cc)
            omp_libnames = gcc('--print-file-name',
                               'libgomp.{0}'.format(dso_suffix),
                               output=str)
            omp_libs = LibraryList(omp_libnames)

        if len(omp_libs) < 1:
            raise_lib_error('Cannot locate OpenMP libraries:', omp_libnames)

        debug_print(omp_libs)
        return omp_libs

    @property
    def blas_libs(self):
        # Main magic here.
        # For reference, see The Intel Math Kernel Library Link Line Advisor:
        # https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor/

        mkl_libnames = ['libmkl_intel_' + self.intel64_int_suffix]
        if not self.spec.satisfies('threads=openmp'):
            mkl_libnames.append('libmkl_sequential')
        elif '%intel' in self.spec:
            mkl_libnames.append('libmkl_intel_thread')
        elif '%gcc' in self.spec:
            mkl_libnames.append('libmkl_gnu_thread')
        else:
            raise_lib_error('Cannot determine MKL threading libraries.')
        mkl_libnames.append('libmkl_core')

        mkl_libs = find_libraries(
            mkl_libnames,
            root=self.component_lib_dir,
            shared=self._want_shared)
        debug_print(mkl_libs)

        if len(mkl_libs) < 3:
            raise_lib_error('Cannot locate core MKL libraries:', mkl_libnames)

        # TODO? TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']
        #
        # NB: TBB is C++, and I don't think here is the right place to try
        # messing with compiler specifics to spit out the right libtbb and
        # libstdc++. Can't a user now use the Spack 'tbb' provider concept?

        if self.spec.satisfies('threads=openmp'):
            omp_libs = self.omp_libs()
        else:
            omp_libs = LibraryList([])

        # The Intel MKL link line advisor recommends these system libraries
        system_libs = find_system_libraries(
            'libpthread libm libdl'.split(),
            shared=self._want_shared)
        debug_print(system_libs)

        return mkl_libs + omp_libs + system_libs

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
        elif ('^mpich@2:' in spec_root
              or '^mvapich2' in spec_root
              or '^intel-mpi' in spec_root):
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
            root=self.component_lib_dir,
            shared=self._want_shared)
        debug_print(sca_libs)

        if len(sca_libs) < 2:
            raise_lib_error(
                'Cannot locate ScaLapack/BLACS libraries:', scalapack_libnames)

        return sca_libs

    @property
    def mpi_libs(self):
        # If prefix is too general, recursive searches may get file variants
        # from supported but inappropriate sub-architectures like 'mic'.
        libnames = ['libmpifort', 'libmpi']
        if 'cxx' in self.spec.last_query.extra_parameters:
            libnames = ['libmpicxx'] + libnames
        return find_libraries(libnames,
                              root=self.component_lib_dir,
                              shared=True, recursive=True)

    @property
    def mpi_headers(self):
        return find_headers('mpi',
                            root=self.component_include_dir,
                            recursive=False)

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
        f = self.file_to_source
        debug_print(f)
        if not os.path.isfile(f):
            return

        if sys.platform == 'darwin':
            run_env.extend(
                EnvironmentModifications.from_sourcing_file(f))
        else:
            run_env.extend(
                EnvironmentModifications.from_sourcing_file(f, 'intel64'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '+mpi' in self.spec or 'intel-mpi' in self.name:
            spack_env.set('I_MPI_CC', spack_cc)
            spack_env.set('I_MPI_CXX', spack_cxx)
            spack_env.set('I_MPI_F77', spack_fc)
            spack_env.set('I_MPI_F90', spack_f77)
            spack_env.set('I_MPI_FC', spack_fc)

            # Convenience variable.
            spack_env.set('I_MPI_ROOT', self.component_dir(component='mpi'))

        elif '+mkl' in self.spec or 'intel-mkl' in self.name:
            # BTW: The name and meaning of the 'root=' keyword arg of
            # find_libraries() entices us to feed it an "mkl_root" variable,
            # but that is a siren song that pulls us down and under from the
            # true MKLROOT. Hence, such a variable name is not used here
            # [anymore].
            spack_env.set('MKLROOT', self.component_dir(component='mkl'))
            spack_env.append_path('SPACK_COMPILER_EXTRA_RPATHS',
                                  self.component_lib_dir(component='mkl'))

        # For other Intel packages, either not needed or not implemented.

    def setup_dependent_package(self, module, dep_spec):
        if '+mpi' in self.spec or 'intel-mpi' in self.name:
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

        # For other Intel packages, either not needed or not implemented.

    #--------------------------------------------------------------------
    # https://software.intel.com/en-us/articles/configuration-file-format
    #
    # ...
    # ACTIVATION=exist_lic
    #
    #    This directive tells the install program to look for an existing
    #    license during the install process.  This is the preferred method for
    #    silent installs.  Take the time to register your serial number and get
    #    a license file (see below).  Having a license file on the system
    #    simplifies the process.  In addition, as an administrator it is good
    #    practice to know WHERE your licenses are saved on your system.
    #    License files are plain text files with a .lic extension.  By default
    #    these are saved in /opt/intel/licenses which is searched by default.
    #    If you save your license elsewhere, perhaps under an NFS folder, set
    #    environment variable INTEL_LICENSE_FILE to the full path to your
    #    license file prior to starting the installation or use the
    #    configuration file directive ACTIVATION_LICENSE_FILE to specify the
    #    full pathname to the license file.
    #
    #    Options for ACTIVATION are { exist_lic, license_file, server_lic,
    #    serial_number, trial_lic }
    #
    # exist_lic
    #    directs the installer to search for a valid license on the server.
    #    Searches will utilize the environment variable INTEL_LICENSE_FILE,
    #    search the default license directory /opt/intel/licenses, or use the
    #    ACTIVATION_LICENSE_FILE directive to find a valid license file.
    #
    # license_file
    #    is similar to exist_lic but directs the installer to use
    #    ACTIVATION_LICENSE_FILE to find the license file.
    #
    # server_lic
    #    is similar to exist_lic and exist_lic but directs the installer that
    #    this is a client installation and a floating license server will be
    #    contacted to active the product.  This option will contact your
    #    floating license server on your network to retrieve the license
    #    information.  BEFORE using this option make sure your client is
    #    correctly set up for your network including all networking, routing,
    #    name service, and firewall configuration.  Insure that your client has
    #    direct access to your floating license server and that firewalls are
    #    set up to allow TCP/IP access for the 2 license server ports.
    #    server_lic will use INTEL_LICENSE_FILE containing a port@host format
    #    OR a client license file.  The formats for these are described here
    #    https://software.intel.com/en-us/articles/licensing-setting-up-the-client-floating-license
    #
    # serial_number
    #    directs the installer to use directive ACTIVATION_SERIAL_NUMBER for
    #    activation.  This method will require the installer to contact an
    #    external Intel activation server over the Internet to confirm your
    #    serial number.  Due to user and company firewalls, this method is more
    #    complex and hence error prone of the available activation methods.  We
    #    highly recommend using a license file or license server for activation
    #    instead.
    #
    # trial_lic
    #    is used only if you do not have an existing license and intend to
    #    temporarily evaluate the compiler.  This method creates a temporary
    #    trial license in Trusted Storage on your system.
    #
    # No license file but you have a serial number?
    #    If you have only a serial number, please visit
    #    https://registrationcenter.intel.com to register your serial number.
    #    As part of registration, you will receive email with an attached
    #    license file.  If your serial is already registered and you need to
    #    retrieve a license file, read this:
    #    https://software.intel.com/en-us/articles/how-do-i-manage-my-licenses
    #
    #    Save the license file in /opt/intel/licenses/ directory, or in your
    #    preferred directory and set INTEL_LICENSE_FILE environment variable to
    #    this non-default location.  If you have already registered your serial
    #    number but have lost the license file, revisit
    #    https://registrationcenter.intel.com and click on the hyperlinked
    #    product name to get to a screen where you can cut and paste or mail
    #    yourself a copy of your registered license file.
    #--------------------------------------------------------------------

    # See also:  lib/spack/spack/hooks/licensing.py

    @property
    def determine_license_type(self):
        # Try file within Spack first, then Intel defaults.
        # fall back to Spack-internal if needed.
        #
        # Hmm - Spack brings up: $EDITOR self.global_license_file

        #if not os.path.isfile(self.global_license_file):
            #if 'INTEL_LICENSE_FILE' in os.environ:
            #    return { 'ACTIVATION_TYPE': 'exist_lic', }

        # TODO: Base decision on whether "self.global_license_file" has
        # actually been populated, viz.  grep '^[^#]'

        if glob.glob('/opt/intel/licenses/*.lic'):
            return {
                'ACTIVATION_TYPE': 'exist_lic',
            }

        return {
            'ACTIVATION_TYPE': 'license_file',
            'ACTIVATION_LICENSE_FILE': self.global_license_file,
        }

    @property
    def global_license_file(self):
        """Returns the path where a global license file should be stored.

        All Intel software shares the same license, so we store it in a
        common 'intel' directory."""
        return join_path(self.global_license_dir, 'intel',
                         os.path.basename(self.license_files[0]))

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
        config = {
            # Accept EULA, valid values are: {accept, decline}
            'ACCEPT_EULA': 'accept',

            # Optional error behavior, valid values are: {yes, no}
            'CONTINUE_WITH_OPTIONAL_ERROR': 'yes',

            # Install location, valid values are: {/opt/intel, filepat}
            'PSET_INSTALL_DIR': prefix,

            # Continue with overwrite of existing installation directory,
            # valid values are: {yes, no}
            'CONTINUE_WITH_INSTALLDIR_OVERWRITE': 'yes',

            # List of components to install,
            # valid values are: {ALL, DEFAULTS, anythingpat}
            'COMPONENTS': ';'.join(self._filtered_components),

            # Installation mode, valid values are: {install, repair, uninstall}
            'PSET_MODE': 'install',

            # Directory for non-RPM database, valid values are: {filepat}
            'NONRPM_DB_DIR': prefix,

            # Perform validation of digital signatures of RPM files,
            # valid values are: {yes, no}
            'SIGNING_ENABLED': 'no',

            # Select target architecture of your applications,
            # valid values are: {IA32, INTEL64, ALL}
            'ARCH_SELECTED': 'ALL',

            # Intel(R) Software Improvement Program opt-in,
            # valid values are: {yes, no}
            'PHONEHOME_SEND_USAGE_DATA': 'no',
        }

        # Not all Intel software requires a license. Trying to specify
        # one anyway will cause the installation to fail.
        if self.license_required:
            config.update(self.determine_license_type)

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

        #TODO: try one of:
        #   ~/intel/ism/uninstall --silent
        #   self.prefix/ism/uninstall --silent
        #
        #if os.path.isfile(self.studio_dir) ...
        #   uninstall_phone_home = Executable( ...

        debug_print(os.getcwd())
        return

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
