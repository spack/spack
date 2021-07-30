# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Rnpletal(Package):
    """The acronym RNPL stands for Rapid Numerical Prototyping Language. It is
    a language for expressing time-dependent systems of partial differential
    equations and the information necessary for solving them using
    finite-difference techniques. It has advantages over traditional
    programming languages such as C and FORTRAN because it only requires the
    user to enter the essential structure of the program while it fills in the
    details."""

    homepage = "http://laplace.physics.ubc.ca/People/matt/Rnpl/index.html"
    url      = "ftp://laplace.physics.ubc.ca/pub/rnpletal/rnpletal.tar.gz"

    # RNPL is distributed via tarballs that are updated from time to time, but
    # which carry no version number. We arbitrarily choose "1.0.0".
    version('1.0.0', sha256='2886f96393b64703fccf61b3dbc34e0fa45a79297232be76352f29cb83863d4d')

    maintainers = ['eschnett']

    patch("corrections.diff")

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    # depends_on('xforms')

    parallel = False

    def install(self, spec, prefix):
        packages = [
            # "rvs",
            # "cliser",
            "rnpl",
            # "svs",
            # "vutil",
            # "utilmath",
            # "visutil",
            # "utilio",
            # "cvtestsdf",
            # "netlib_linpack",
            # "netlib_odepack",
            # "netlib_fftpack",
            # "netlib_lapack3.0",
        ]

        configure_args = [
            "--prefix=" + prefix,
            # "CFLAGS=-Wno-error,-Wimplicit-function-declaration",
        ]

        for package in packages:
            with working_dir(package):
                configure = which("./configure")
                configure(*configure_args)
                make("install")

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            ["libbbhutil", "librnpl"],
            root=self.prefix, shared=shared, recursive=True
        )
