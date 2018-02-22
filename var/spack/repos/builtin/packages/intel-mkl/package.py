##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os
import sys

from spack import *
from spack.environment import EnvironmentModifications
from spack.util.prefix import Prefix
from llnl.util.filesystem import join_path, ancestor
import llnl.util.tty as tty


class IntelMkl(IntelPackage):
    """Intel Math Kernel Library."""

    homepage = "https://software.intel.com/en-us/intel-mkl"

    version('2018.1.163', 'f1f7b6ddd7eb57dfe39bd4643446dc1c',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mkl_2018.1.163.tgz")
    version('2018.0.128', '0fa23779816a0f2ee23a396fc1af9978',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12070/l_mkl_2018.0.128.tgz")
    version('2017.4.239', '3066272dd0ad3da7961b3d782e1fab3b',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12147/l_mkl_2017.4.239.tgz")
    version('2017.3.196', '4a2eb4bee789391d9c07d7c348a80702',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11544/l_mkl_2017.3.196.tgz")
    version('2017.2.174', 'ef39a12dcbffe5f4a0ef141b8759208c',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11306/l_mkl_2017.2.174.tgz")
    version('2017.1.132', '7911c0f777c4cb04225bf4518088939e',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11024/l_mkl_2017.1.132.tgz")
    version('2017.0.098', '3cdcb739ab5ab1e047eb130b9ffdd8d0',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9662/l_mkl_2017.0.098.tgz")
    version('11.3.3.210', 'f72546df27f5ebb0941b5d21fd804e34',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9068/l_mkl_11.3.3.210.tgz")
    version('11.3.2.181', '536dbd82896d6facc16de8f961d17d65',
            url="http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8711/l_mkl_11.3.2.181.tgz")

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False, description='64 bit integers')
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )

    provides('blas')
    provides('lapack')
    provides('scalapack')
    provides('mkl')

    if sys.platform == 'darwin':
        # there is no libmkl_gnu_thread on macOS
        conflicts('threads=openmp', when='%gcc')

    @property
    def license_required(self):
        # The Intel libraries are provided without requiring a license as of
        # version 2017.2. Trying to specify the license will fail. See:
        # https://software.intel.com/en-us/articles/free-ipsxe-tools-and-libraries
        return self.version < Version('2017.2')

    @property
    def _want_shared(self):
        return ('+shared' in self.spec)

    @property
    def _mkl_int_suffix(self):
        if '+ilp64' in self.spec:
            return '_ilp64'
        else:
            return '_lp64'

#--------------------------------------------------------------------
# Analysis of the directory layout for a Spack-born installation of:
# intel-mkl@2018.1.163
#--------------------------------------------------------------------
#
#   $ ls -l <prefix>
#     # Unix metadata removed, entries rearranged, "->" still means symlink.
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
#       [.] bin           - actual compilervars.*sh (reg. files) ONLY
#       [.] documentation -> ../../documentation_2018/
#       [.] lib -> ../../compilers_and_libraries_2018.1.163/linux/compiler/lib/
#       [.] mkl -> ../../compilers_and_libraries_2018.1.163/linux/mkl/
#       [.] pkg_bin -> ../../compilers_and_libraries_2018.1.163/linux/bin/
#       [.] samples -> ../../samples_2018/
#       [.] tbb -> ../../compilers_and_libraries_2018.1.163/linux/tbb/
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
#       compilers_and_libraries_2018 -> <full_path_prefix>/comp..._2018.1.163
#       documentation_2018 -> <full_path_prefix>/documentation_2018
#       samples_2018 -> <full_path_prefix>/samples_2018
#       ...
#
#   documentation_2018/
#   samples_2018/
#   lib -> compilers_and_libraries/linux/lib/
#   mkl -> compilers_and_libraries/linux/mkl/
#   tbb -> compilers_and_libraries/linux/tbb/
#                                   - auxiliaries and convenience links
#
#--------------------------------------------------------------------

    @property
    def mklroot(self):
        '''Returns the effective toplevel product directory, i.e., the
        directory that is to be presented to users in the MKLROOT environment
        variable.
        '''
        # Similar code in ../intel-mpi/package.py:_mpi_root()
        d = self.prefix
        if sys.platform == 'darwin':
            # TODO: Verify on Mac.
            return d.mkl

        if 'compilers_and_libraries_' in d and '.' in d:
            # When MKL was installed outside of Spack (a "ghost package"
            # integrated via packages.yaml), the prefix will inevitably point
            # to a directory that is specific to MKL as one Intel *product*
            # among possibly others that are installed in sibling or cousin
            # directories. This product-specific and (preferably fully)
            # version-specific directory is what we want and need.
            pass
        elif 'compilers_and_libraries' in d:
            # A non-qualified install dir (likely a symlink) is fragile and
            # bound to change outside of Spack's purview. That could be
            # acceptable but it does affect reproducibility in Spack and may
            # alter the outcome of subsequent builds of dependent packages. I'm
            # not sure if Spack's package hashing senses this.
            tty.warn('Intel-MKL found in a version-neutral directory - '
                     'future builds may not be reproducible.')
            pass
        else:
            # By contrast, a Spack-born MKL installation will inherit its
            # prefix from install.sh of Intel's package distribution, where it
            # means the high-level installation directory that is specific to
            # the *vendor* (illustrated by the default "/opt/intel"). We must
            # now step down into the *product* directory to get the usual
            # hierarchy, but let's not do that in haste ...
            d = d.compilers_and_libraries

            # For a Spack-born install, using the fully-qualified release
            # directory that is so desired above is possible but far less
            # important since product upgrades won't land in the same parent.
            # To force it nonetheless, uncomment the following:
            #d = Prefix(d.append('_' + self.version))

            # Alright, now the final flight of stairs.
            d = d.linux.mkl

        # On my system, using a ghosted MKL, self.prefix showed up as ending
        # with "/compiler". I think this is because I provide that MKL by means
        # of the side effect of loading an env. module for the Intel
        # *compilers*, and Spack inspects $PATH(?) Well, I can live with that!
        # It's just a jump to the left, and then a step to the right; let's do
        # the time warp again:
        if d.endswith('compiler'):
            d = Prefix(ancestor(d)).mkl

        _debug_print('mkl_prefix', d)
        return d

    @property
    def _mkl_libdir(self):
        # Provide starting directory for find_libraries() and for
        # SPACK_COMPILER_EXTRA_RPATHS.
        if sys.platform == 'darwin':
            d = self.mklroot.lib
        else:
            d = self.mklroot.lib.intel64
        _debug_print('mkl_libdir', d)
        return d

    @property
    def blas_libs(self):
        mkl_libnames = ['libmkl_intel' + self._mkl_int_suffix]

        if self.spec.satisfies('threads=openmp'):
            if '%intel' in self.spec:
                # The directory "$MKLROOT/../compiler" will be present even for
                # an MKL-only install (as opposed to being ghosted via
                # packages.yaml), specificially to provide the 'iomp5' libs.
                omp_libnames = ['libiomp5']
                omp_libs = find_libraries(
                    omp_libnames,
                    root=Prefix(ancestor(self.mklroot)).compiler,
                    shared=self._want_shared)
                mkl_libnames.append('libmkl_intel_thread')

            elif '%gcc' in self.spec:
                gcc = Executable(self.compiler.cc)
                omp_libnames = gcc('--print-file-name',
                                   'libgomp.{0}'.format(dso_suffix),
                                   output=str)
                omp_libs = LibraryList(omp_libnames)
                mkl_libnames.append('libmkl_gnu_thread')

            if len(omp_libs) < 1:
                _raise_install_error(
                    'Cannot locate OpenMP libraries:', omp_libnames)
        else:
            omp_libs = LibraryList([])
            mkl_libnames.append('libmkl_sequential')

        _debug_print('omp_libs', omp_libs)
        mkl_libnames.append('libmkl_core')

        # TODO: TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']

        mkl_libs = find_libraries(
            mkl_libnames,
            root=self._mkl_libdir,
            shared=self._want_shared)
        _debug_print('mkl_libs', mkl_libs)

        if len(mkl_libs) < 3:
            _raise_install_error(
                'Cannot locate core MKL libraries:', mkl_libnames)

        # Intel MKL link line advisor recommends these system libraries
        system_libs = find_system_libraries(
            'libpthread libm libdl'.split(),
            shared=self._want_shared)
        _debug_print('system_libs', system_libs)

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
            blacs_variant = '_mpich'
        elif '^openmpi' in spec_root:
            blacs_variant = '_openmpi'
        elif '^mpich@1' in spec_root:
            # Was supported only up to 2015.
            blacs_variant = ''
        elif ('^mpich@2:' in spec_root
              or '^mvapich2' in spec_root
              or '^intel-mpi' in spec_root):
            blacs_variant = '_intelmpi'
        elif '^mpt' in spec_root:
            blacs_variant = '_sgimpt'
        else:
            _raise_install_error(
                'Cannot determine a BLACS variant for the given MPI.')

        scalapack_libnames = [
            'libmkl_scalapack' + self._mkl_int_suffix,
            'libmkl_blacs' + blacs_variant + self._mkl_int_suffix,
        ]
        sca_libs = find_libraries(
            scalapack_libnames,
            root=self._mkl_libdir,
            shared=self._want_shared)
        _debug_print('scalapack_libs', sca_libs)

        if len(sca_libs) < 2:
            _raise_install_error(
                'Cannot locate ScaLapack/BLACS libraries:', scalapack_libnames)

        return sca_libs

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # BTW: The name and meaning of the 'root=' keyword arg of
        # find_libraries() entices us to feed it an "mkl_root" variable, but
        # that is a siren song that pulls us down and under from the true
        # MKLROOT. Hence, such a variable name is not used here [anymore].
        spack_env.set('MKLROOT', self.mklroot)
        spack_env.append_path('SPACK_COMPILER_EXTRA_RPATHS', self._mkl_libdir)

    def setup_environment(self, spack_env, run_env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source mkl/bin/mklvars.sh intel64
        """
        # NOTE: Spack runs setup_environment twice, once pre-build to set up
        # the build environment, and once post-installation to determine
        # the environment variables needed at run-time to add to the module
        # file. The script we need to source is only present post-installation,
        # so check for its existence before sourcing.
        # TODO: At some point we should split setup_environment into
        # setup_build_environment and setup_run_environment to get around
        # this problem.
        mklvars = join_path(self.mklroot.bin, 'mklvars.sh')
        if os.path.isfile(mklvars):
            if sys.platform == 'darwin':
                run_env.extend(
                    EnvironmentModifications.from_sourcing_file(
                        mklvars))
            else:
                run_env.extend(
                    EnvironmentModifications.from_sourcing_file(
                        mklvars, 'intel64'))


# A couple of utility functions that might be useful in general. If so, they
# should really be defined elsewhere, unless deemed heretical.
# (Or na"ive on my part).

import inspect


def _debug_print(label, value, *args, **kwargs):
    '''Prints a variable, labeled, along with the caller's caller
    function name (for more context).
    '''
    # See also: https://docs.python.org/2/library/inspect.html#the-interpreter-stack
    traceback = 2
    func_name = inspect.stack()[traceback][3]
    tty.debug("{0}.{1}:\t'{2}'".format(func_name, label, value),
              *args, **kwargs)


def _raise_install_error(*args):
    '''Issues a possibly multi-line error message, then bail out.
    Indents all args after the first, which is useful to have long paths
    stand out.
    '''
    raise InstallError("\n\t".join(str(i) for i in list(*args)))
