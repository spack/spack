# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os
import sys
from llnl.util.filesystem import fix_darwin_install_name


class Papi(Package):
    """PAPI provides the tool designer and application engineer with a
       consistent interface and methodology for use of the performance
       counter hardware found in most major microprocessors. PAPI
       enables software engineers to see, in near real time, the
       relation between software performance and processor events.  In
       addition Component PAPI provides access to a collection of
       components that expose performance measurement opportunites
       across the hardware and software stack."""
    homepage = "http://icl.cs.utk.edu/papi/index.html"

    url      = "http://icl.cs.utk.edu/projects/papi/downloads/papi-5.4.1.tar.gz"
    version('5.7.0', 'd1a3bb848e292c805bc9f29e09c27870e2ff4cda6c2fba3b7da8b4bba6547589')
    version('5.6.0', 'fdd075860b2bc4b8de8b8b5c3abf594a')
    version('5.5.1', '86a8a6f3d0f34cd83251da3514aae15d')
    version('5.5.0', '5e1244a04ca031d4cc29b46ce3dd05b5')
    version('5.4.3', '3211b5a5bb389fe692370f5cf4cc2412')
    version('5.4.1', '9134a99219c79767a11463a76b0b01a2')
    version('5.3.0', '367961dd0ab426e5ae367c2713924ffb')

    # Does not build with newer versions of gcc, see
    # https://bitbucket.org/icl/papi/issues/46/cannot-compile-on-arch-linux
    patch('https://bitbucket.org/icl/papi/commits/53de184a162b8a7edff48fed01a15980664e15b1/raw', sha256='64c57b3ad4026255238cc495df6abfacc41de391a0af497c27d0ac819444a1f8', when='@5.4.0:5.6.99%gcc@8:')

    def install(self, spec, prefix):
        with working_dir("src"):

            configure_args = ["--prefix=%s" % prefix]

            # PAPI uses MPI if MPI is present; since we don't require
            # an MPI package, we ensure that all attempts to use MPI
            # fail, so that PAPI does not get confused
            configure_args.append('MPICC=:')

            configure(*configure_args)

            # Don't use <malloc.h>
            for level in [".", "*", "*/*"]:
                files = glob.iglob(join_path(level, "*.[ch]"))
                filter_file(r"\<malloc\.h\>", "<stdlib.h>", *files)

            make()
            make("install")

            # The shared library is not installed correctly on Darwin
            if sys.platform == 'darwin':
                os.rename(join_path(prefix.lib, 'libpapi.so'),
                          join_path(prefix.lib, 'libpapi.dylib'))
                fix_darwin_install_name(prefix.lib)
