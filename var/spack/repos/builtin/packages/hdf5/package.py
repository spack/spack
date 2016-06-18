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


class Hdf5(Package):
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
    version('1.8.16', 'b8ed9a36ae142317f88b0c7ef4b9c618', preferred=True)
    version('1.8.15', '03cccb5b33dbe975fdcd8ae9dc021f24')
    version('1.8.13', 'c03426e9e77d7766944654280b467289')

    variant('debug', default=False, description='Builds a debug version of the library')
    variant('shared', default=True, description='Builds a shared version of the library')

    variant('cxx', default=True, description='Enable C++ support')
    variant('fortran', default=True, description='Enable Fortran support')

    variant('mpi', default=False, description='Enable MPI support')
    variant('szip', default=False, description='Enable szip support')
    variant('threadsafe', default=False, description='Enable thread-safe capabilities')

    depends_on("mpi", when='+mpi')
    depends_on("szip", when='+szip')
    depends_on("zlib")

    def validate(self, spec):
        """
        Checks if incompatible variants have been activated at the same time

        :param spec: spec of the package
        :raises RuntimeError: in case of inconsistencies
        """
        if '+fortran' in spec and not self.compiler.fc:
            msg = 'cannot build a fortran variant without a fortran compiler'
            raise RuntimeError(msg)

        if '+threadsafe' in spec and ('+cxx' in spec or '+fortran' in spec):
                raise RuntimeError("cannot use variant +threadsafe with either +cxx or +fortran")

    def install(self, spec, prefix):
        self.validate(spec)
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

        if '+mpi' in spec:
            # The HDF5 configure script warns if cxx and mpi are enabled
            # together. There doesn't seem to be a real reason for this, except
            # that parts of the MPI interface are not accessible via the C++
            # interface. Since they are still accessible via the C interface,
            # this is not actually a problem.
            extra_args.extend([
                "--enable-parallel",
                "CC=%s" % join_path(spec['mpi'].prefix.bin, "mpicc"),
            ])

            if '+cxx' in spec:
                extra_args.append("CXX=%s" % join_path(spec['mpi'].prefix.bin,
                                                       "mpic++"))

            if '+fortran' in spec:
                extra_args.append("FC=%s" % join_path(spec['mpi'].prefix.bin,
                                                      "mpifort"))

        if '+szip' in spec:
            extra_args.append("--with-szlib=%s" % spec['szip'].prefix)

        if '+threadsafe' in spec:
            extra_args.extend([
                '--enable-threadsafe',
                '--disable-hl',
            ])

        configure(
            "--prefix=%s" % prefix,
            "--with-zlib=%s" % spec['zlib'].prefix,
            *extra_args)
        make()
        make("install")
        self.check_install(spec)

    def check_install(self, spec):
        "Build and run a small program to test the installed HDF5 library"
        print "Checking HDF5 installation..."
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
""".format(version=str(spec.version))
            with open("check.c", 'w') as f:
                f.write(source)
            if '+mpi' in spec:
                cc = which(join_path(spec['mpi'].prefix.bin, "mpicc"))
            else:
                cc = which('cc')
            # TODO: Automate these path and library settings
            cc('-c', "-I%s" % join_path(spec.prefix, "include"), "check.c")
            cc('-o', "check", "check.o",
               "-L%s" % join_path(spec.prefix, "lib"), "-lhdf5",
               "-lz")
            try:
                check = Executable('./check')
                output = check(return_output=True)
            except:
                output = ""
            success = output == expected
            if not success:
                print "Produced output does not match expected output."
                print "Expected output:"
                print '-'*80
                print expected
                print '-'*80
                print "Produced output:"
                print '-'*80
                print output
                print '-'*80
                raise RuntimeError("HDF5 install check failed")
        shutil.rmtree(checkdir)

    def url_for_version(self, version):
        v = str(version)

        if version == Version("1.2.2"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + ".tar.gz"
        elif version < Version("1.7"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + version.up_to(2) + "/hdf5-" + v + ".tar.gz"
        elif version < Version("1.10"):
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + v + "/src/hdf5-" + v + ".tar.gz"
        else:
            return "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-" + version.up_to(2) + "/hdf5-" + v + "/src/hdf5-" + v + ".tar.gz"
