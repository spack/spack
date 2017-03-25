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
import shutil


class Hdf5(AutotoolsPackage):
    """HDF5 is a data model, library, and file format for storing and managing
    data. It supports an unlimited variety of datatypes, and is designed for
    flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "http://www.hdfgroup.org/HDF5/"
    url = "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.13/src/hdf5-1.8.13.tar.gz"
    list_url = "http://www.hdfgroup.org/ftp/HDF5/releases"
    list_depth = 3

    version('1.10.0-patch1', '9180ff0ef8dc2ef3f61bd37a7404f295')
    version('1.10.0', 'bdc935337ee8282579cd6bc4270ad199')
    version('1.8.18', 'dd2148b740713ca0295442ec683d7b1c',
            # The link for the latest version differs from the links for
            # the previous releases. Do not forget to remove this once
            # the version 1.8.18 is not the latest one for the 1.8.* branch.
            url='http://hdfgroup.org/ftp/HDF5/current18/src/hdf5-1.8.18.tar.gz')
    version('1.8.17', '7d572f8f3b798a628b8245af0391a0ca')
    version('1.8.16', 'b8ed9a36ae142317f88b0c7ef4b9c618')
    version('1.8.15', '03cccb5b33dbe975fdcd8ae9dc021f24')
    version('1.8.14', 'a482686e733514a51cde12d6fe5c5d95')
    version('1.8.13', 'c03426e9e77d7766944654280b467289')
    version('1.8.12', 'd804802feb99b87fc668a90e6fa34411')

    variant('debug', default=False,
            description='Builds a debug version of the library')
    variant('shared', default=True,
            description='Builds a shared version of the library')

    variant('cxx', default=True, description='Enable C++ support')
    variant('fortran', default=True, description='Enable Fortran support')

    variant('mpi', default=True, description='Enable MPI support')
    variant('szip', default=False, description='Enable szip support')
    variant('threadsafe', default=False,
            description='Enable thread-safe capabilities')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    depends_on('mpi', when='+mpi')
    depends_on('szip', when='+szip')
    depends_on('zlib@1.1.2:')

    @run_before('configure')
    def validate(self):
        """
        Checks if incompatible variants have been activated at the same time

        :param spec: spec of the package
        :raises RuntimeError: in case of inconsistencies
        """
        spec = self.spec
        if '+fortran' in spec and not self.compiler.fc:
            msg = 'cannot build a fortran variant without a fortran compiler'
            raise RuntimeError(msg)

        if '+threadsafe' in spec and ('+cxx' in spec or '+fortran' in spec):
            msg = 'cannot use variant +threadsafe with either +cxx or +fortran'
            raise RuntimeError(msg)

    def configure_args(self):
        spec = self.spec
        # Handle compilation after spec validation
        extra_args = []

        # Always enable this option. This does not actually enable any
        # features: it only *allows* the user to specify certain
        # combinations of other arguments. Enabling it just skips a
        # sanity check in configure, so this doesn't merit a variant.
        extra_args.append("--enable-unsupported")

        if spec.satisfies('@1.10:'):
            if '+debug' in spec:
                extra_args.append('--enable-build-mode=debug')
            else:
                extra_args.append('--enable-build-mode=production')
        else:
            if '+debug' in spec:
                extra_args.append('--enable-debug=all')
            else:
                extra_args.append('--enable-production')

        if '+shared' in spec:
            extra_args.append('--enable-shared')
        else:
            extra_args.append('--enable-static-exec')

        if '+cxx' in spec:
            extra_args.append('--enable-cxx')

        if '+fortran' in spec:
            extra_args.append('--enable-fortran')
            # '--enable-fortran2003' no longer exists as of version 1.10.0
            if spec.satisfies('@:1.8.16'):
                extra_args.append('--enable-fortran2003')

        if '+pic' in spec:
            extra_args.append('CFLAGS={0}'.format(self.compiler.pic_flag))
            extra_args.append('CXXFLAGS={0}'.format(self.compiler.pic_flag))
            extra_args.append('FCFLAGS={0}'.format(self.compiler.pic_flag))

        if '+mpi' in spec:
            # The HDF5 configure script warns if cxx and mpi are enabled
            # together. There doesn't seem to be a real reason for this, except
            # that parts of the MPI interface are not accessible via the C++
            # interface. Since they are still accessible via the C interface,
            # this is not actually a problem.
            extra_args.extend([
                "--enable-parallel",
                "CC=%s" % spec['mpi'].mpicc
            ])

            if '+cxx' in spec:
                extra_args.append("CXX=%s" % spec['mpi'].mpicxx)

            if '+fortran' in spec:
                extra_args.append("FC=%s" % spec['mpi'].mpifc)

        if '+szip' in spec:
            extra_args.append("--with-szlib=%s" % spec['szip'].prefix)

        if '+threadsafe' in spec:
            extra_args.extend([
                '--enable-threadsafe',
                '--disable-hl',
            ])

        return ["--with-zlib=%s" % spec['zlib'].prefix] + extra_args

    def configure(self, spec, prefix):
        # Run the default autotools package configure
        super(Hdf5, self).configure(spec, prefix)

        if '@:1.8.14' in spec:
            # On Ubuntu14, HDF5 1.8.12 (and maybe other versions)
            # mysteriously end up with "-l -l" in the postdeps in the
            # libtool script.  Patch this by removing the spurious -l's.
            filter_file(
                r'postdeps="([^"]*)"',
                lambda m: 'postdeps="%s"' % ' '.join(
                    arg for arg in m.group(1).split(' ') if arg != '-l'),
                'libtool')

    @run_after('install')
    def check_install(self):
        # Build and run a small program to test the installed HDF5 library
        spec = self.spec
        print("Checking HDF5 installation...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""
#include <hdf5.h>
#include <assert.h>
#include <stdio.h>
int main(int argc, char **argv) {
  unsigned majnum, minnum, relnum;
  herr_t herr = H5get_libversion(&majnum, &minnum, &relnum);
  assert(!herr);
  printf("HDF5 version %d.%d.%d %u.%u.%u\n", H5_VERS_MAJOR, H5_VERS_MINOR,
         H5_VERS_RELEASE, majnum, minnum, relnum);
  return 0;
}
"""
            expected = """\
HDF5 version {version} {version}
""".format(version=str(spec.version.up_to(3)))
            with open("check.c", 'w') as f:
                f.write(source)
            if '+mpi' in spec:
                cc = Executable(spec['mpi'].mpicc)
            else:
                cc = Executable(self.compiler.cc)
            cc(*(['-c', "check.c"] + spec['hdf5'].cppflags.split()))
            cc(*(['-o', "check", "check.o"] +
                 spec['hdf5'].libs.ld_flags.split()))
            try:
                check = Executable('./check')
                output = check(return_output=True)
            except:
                output = ""
            success = output == expected
            if not success:
                print("Produced output does not match expected output.")
                print("Expected output:")
                print('-' * 80)
                print(expected)
                print('-' * 80)
                print("Produced output:")
                print('-' * 80)
                print(output)
                print('-' * 80)
                raise RuntimeError("HDF5 install check failed")
        shutil.rmtree(checkdir)

    def url_for_version(self, version):
        # If we have a specific URL for this version, return it.
        version_urls = self.version_urls()
        if version in version_urls:
            return version_urls[version]

        base_url = "http://www.hdfgroup.org/ftp/HDF5/releases"

        if version == Version("1.2.2"):
            return "{0}/hdf5-{1}.tar.gz".format(base_url, version)
        elif version < Version("1.6.6"):
            return "{0}/hdf5-{1}/hdf5-{2}.tar.gz".format(
                base_url, version.up_to(2), version)
        elif version < Version("1.7"):
            return "{0}/hdf5-{1}/hdf5-{2}/src/hdf5-{2}.tar.gz".format(
                base_url, version.up_to(2), version)
        elif version < Version("1.10"):
            return "{0}/hdf5-{1}/src/hdf5-{1}.tar.gz".format(
                base_url, version)
        else:
            return "{0}/hdf5-{1}/hdf5-{2}/src/hdf5-{2}.tar.gz".format(
                base_url, version.up_to(2), version)
