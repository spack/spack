# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cgm(AutotoolsPackage):
    """The Common Geometry Module, Argonne (CGMA) is a code library
       which provides geometry functionality used for mesh generation and
       other applications."""
    homepage = "http://sigma.mcs.anl.gov/cgm-library"
    url = "http://ftp.mcs.anl.gov/pub/fathom/cgm-16.0.tar.gz"

    version('16.0', 'a68aa5954d82502ff75d5eb91a29a01c')
    version('13.1.1', '4e8dbc4ba8f65767b29f985f7a23b01f')
    version('13.1.0', 'a6c7b22660f164ce893fb974f9cb2028')
    version('13.1', '95f724bda04919fc76818a5b7bc0b4ed')

    variant("mpi", default=True, description='enable mpi support')
    variant("oce", default=False, description='enable oce geometry kernel')
    variant("debug", default=False, description='enable debug symbols')
    variant("shared", default=False, description='enable shared builds')

    depends_on('mpi', when='+mpi')
    depends_on('oce+X11', when='+oce')

    def configure_args(self):
        spec = self.spec
        args = []

        if '+mpi' in spec:
            args.extend([
                "--with-mpi",
                "CC={0}".format(spec['mpi'].mpicc),
                "CXX={0}".format(spec['mpi'].mpicxx)
            ])
        else:
            args.append("--without-mpi")

        if '+oce' in spec:
            args.append("--with-occ={0}".format(spec['oce'].prefix))
        else:
            args.append("--without-occ")

        if '+debug' in spec:
            args.append("--enable-debug")

        if '+shared' in spec:
            args.append("--enable-shared")

        return args
