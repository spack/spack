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
import inspect
import xml.etree.ElementTree as ET
import llnl.util.tty as tty

from llnl.util.filesystem \
    import install, join_path, ancestor, LibraryList, find_libraries

from spack.package import PackageBase, run_after, InstallError
from spack.util.executable import Executable
from spack.util.prefix import Prefix
from spack.build_environment import dso_suffix


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

#--------------------------------------------------------------------
# Analysis of the directory layout for a Spack-born installation of
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
#                   - auxiliaries and convenience links
#
#--------------------------------------------------------------------
# Directory analysis for intel-mpi@2018.1.163
#--------------------------------------------------------------------
# For MPI, the layout is slightly different than MKL. The prefix will have to
# include the sub-arch, which contains bin/, lib/, ..., all without further
# arch splits. I_MPI_ROOT, however, must be the package dir.
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
#
# Note on macOS support, i.e., sys.platform == 'darwin':
#
# - On macOS, the Spack methods here only include support to integrate an
#   externally installed MKL.
#
# - URLs in child packages will be Linux-specific; macOS download packages are
#   located in differently numbered dirs and are named m_*.dmg.
#
#--------------------------------------------------------------------

    @property
    def product_os_dir(self):
        '''Returns the version-specific directory of an Intel product release,
        holding the main product and auxiliary files from other products.
        '''
        d = self.prefix
        if sys.platform == 'darwin':
            # TODO: Verify on Mac.
            return d

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
            #
            # Code may never be reached is self.prefix has been abspath()'ed.
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
            d = d.linux

        # On my system, using a ghosted MKL, self.prefix showed up as ending
        # with "/compiler". I think this is because I provide that MKL by means
        # of the side effect of loading an env. module for the Intel
        # *compilers*, and Spack inspects $PATH(?) Well, I can live with that!
        # It's just a jump to the left, and then a step to the right; let's do
        # the time warp again:
        #
        # Ahem, apparently, the Prefix class lacks a native parent() method
        # (kinda understandably so), but the syntax blows up on trying "..".
        #
        # TODO? accomodate other platforms(?)
        # NB: Searching by platform, we can indulge in hardcoding the path sep.
        #
        while '/linux' in d and not d.endswith('/linux'):
            d = Prefix(ancestor(d))

        debug_print(d)
        return d

    def product_component_dir(self, component=None):
        '''Returns the directory of a product component, appropriate for
        presenting to users in environment variables like MKLROOT and
        I_MPI_ROOT.
        '''
        d = component
        if component is None:
            # For ref.: Intel packages in Spack-0.11:
            #  intel/
            #  intel-daal/
            #  intel-gpu-tools/
            #  intel-ipp/
            #  intel-mkl/
            #  intel-mkl-dnn/
            #  intel-mpi/
            #  intel-parallel-studio
            #  intel-tbb/
            if self.name.startswith('intel-mkl'):
                d = 'mkl'
            elif self.name.startswith('intel-mpi'):
                d = 'mpi'
            else:
                raise_lib_error('Cannot determine product component dir.')

        # Note analysis of MPI dir above:  Since both I_MPI_ROOT and MANPATH
        # need the 'mpi' dir, do NOT qualify the retval further.
        #NODO: d = d.intel64 if ... 'mpi' ...

        d = Prefix(join_path(self.product_os_dir, d))
        debug_print(d)
        return d

    @property
    def component_bindir(self, component=None):
        d = self.product_component_dir(component)
        if sys.platform == 'darwin':
            d = d.bin
        else:
            if self.name.startswith('intel-mpi') or component == 'mpi':
                d = d.intel64.bin
            # TODO: eval if needed
            #elif ... 'compiler'
            #    d = Prefix(ancestor(d)).bin.intel64
            else:
                d = d.bin

        debug_print(d)
        return d

    @property
    def component_libdir(self, component=None):
        # Provide starting directory for find_libraries() and for
        # SPACK_COMPILER_EXTRA_RPATHS.

        d = self.product_component_dir(component)
        if sys.platform == 'darwin':
            d = d.lib
        else:
            if self.name.startswith('intel-mpi') or component == 'mpi':
                d = d.intel64.lib
            else:
                d = d.lib.intel64
            # A bit weird, but  I'm sure there are good reasons for it.

        debug_print(d)
        return d

    @property
    def component_includedir(self, component=None):
        d = self.product_component_dir(component)
        if self.name.startswith('intel-mpi') or component == 'mpi':
            d = d.intel64
        d = d.include

        debug_print(d)
        return d

    @property
    def omp_libs(self):
        # Supply LibraryList for linking OpenMP

        # FIXME  if sys.platform == 'darwin' ....

        # TODO?  Are variants named consistently enough in Spack to determine
        # that OpenMP is NOT needed and then return an empty list?

        if '%intel' in self.spec:
            omp_libnames = ['libiomp5']

            # Note about search root: For MKL, the directory
            # "$MKLROOT/../compiler" will be present even for an MKL-only
            # product installation (as opposed to one being ghosted via
            # packages.yaml), specificially to provide the 'iomp5' libs.

            omp_libs = find_libraries(
                omp_libnames,
                root=self.component_libdir(component='compiler'),
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
        }

        # Not all Intel software requires a license. Trying to specify
        # one anyway will cause the installation to fail.
        if self.license_required:
            config.update({
                # License file or license server,
                # valid values are: {lspat, filepat}
                'ACTIVATION_LICENSE_FILE': self.global_license_file,

                # Activation type, valid values are: {exist_lic,
                # license_server, license_file, trial_lic, serial_number}
                'ACTIVATION_TYPE': 'license_file',

                # Intel(R) Software Improvement Program opt-in,
                # valid values are: {yes, no}
                'PHONEHOME_SEND_USAGE_DATA': 'no',
            })

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

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
