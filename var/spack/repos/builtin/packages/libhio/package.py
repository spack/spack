# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Libhio(AutotoolsPackage):
    """libHIO is a flexible, high-performance parallel IO package developed
       at LANL.  libHIO supports IO to either a conventional PFS or to Cray
       DataWarp with management of Cray DataWarp space and stage-in and
       stage-out from and to the PFS.
    """

    homepage = "https://github.com/hpc/libhio"
    url      = "https://github.com/hpc/libhio/releases/download/hio.1.4.1.0/libhio-1.4.1.0.tar.bz2"

    #
    # We don't include older versions since they are missing features
    # needed by current and future consumers of libhio
    #
    version('1.4.1.2', '38c7d33210155e5796b16d536d1b5cfe')
    version('1.4.1.0', '6ef566fd8cf31fdcd05fab01dd3fae44')

    #
    # main users of libhio thru spack will want to use HFDF5 plugin,
    # so make hdf5 variant a default
    #
    variant('hdf5', default=True, description='Enable HDF5 support')

    depends_on("json-c")
    depends_on("bzip2")
    depends_on("pkgconfig", type="build")
    depends_on('mpi')

    #
    # libhio depends on hdf5+mpi if hdf5 is being used since it
    # autodetects the presence of an MPI and/or uses mpicc by default to build
    depends_on('hdf5+mpi', when='+hdf5')

    #
    # wow, we need to patch libhio
    #
    patch('0001-configury-fix-a-problem-with-bz2-configury.patch', when="@1.4.1.0")
    patch('0001-hdf5-make-docs-optional.patch', when="@1.4.1.0")
    patch('0001-spack-fix-for-spack-to-work-on-non-cray-systems.patch', when="@1.4.1.2")

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')
        autoreconf('-ifv')

    def configure_args(self):
        spec = self.spec
        args = []

        args.append('--with-external_bz2={0}'.format(spec['bzip2'].prefix))
        if '+hdf5' in spec:
            args.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))

        return args
