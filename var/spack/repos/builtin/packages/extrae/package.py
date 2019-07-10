# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

# typical working line with extrae 3.0.1
# ./configure
#   --prefix=/usr/local
#   --with-mpi=/usr/lib64/mpi/gcc/openmpi
#   --with-unwind=/usr/local
#   --with-papi=/usr
#   --with-dwarf=/usr
#   --with-elf=/usr
#   --with-dyninst=/usr
#   --with-binutils=/usr
#   --with-xml-prefix=/usr
#   --enable-openmp
#   --enable-nanos
#   --enable-pthread
#   --disable-parallel-merge
#
# LDFLAGS=-pthread


class Extrae(Package):
    """Extrae is the package devoted to generate tracefiles which can
       be analyzed later by Paraver. Extrae is a tool that uses
       different interposition mechanisms to inject probes into the
       target application so as to gather information regarding the
       application performance. The Extrae instrumentation package can
       instrument the MPI programin model, and the following parallel
       programming models either alone or in conjunction with MPI :
       OpenMP, CUDA, OpenCL, pthread, OmpSs"""
    homepage = "https://tools.bsc.es/extrae"
    url      = "https://ftp.tools.bsc.es/extrae/extrae-3.4.1-src.tar.bz2"
    version('3.7.1', sha256='95810b057f95e91bfc89813eb8bd320dfe40614fc8e98c63d95c5101c56dd213', preferred=True)
    version('3.4.1', '69001f5cfac46e445d61eeb567bc8844')

    depends_on("mpi")
    depends_on("libunwind")
    depends_on("boost")
    depends_on("libdwarf")
    depends_on("papi")
    depends_on("elf", type="link")
    depends_on("libxml2")

    variant('dyninst', default=False, description="Use dyninst for dynamic code installation")
    depends_on('dyninst@:9.9.99', type=('build', 'link'), when='+dyninst')

    variant('papi', default=True, description="Use PAPI to collect performance counters")
    depends_on('papi', type=('build', 'link'), when='+papi')

    # gettext dependency added to find -lintl
    # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
    depends_on("gettext")
    depends_on("binutils+libiberty")

    def install(self, spec, prefix):
        if 'openmpi' in spec:
            mpi = spec['openmpi']
        elif 'mpich' in spec:
            mpi = spec['mpich']
        elif 'mvapich2' in spec:
            mpi = spec['mvapich2']

        config_args = ["--prefix=%s" % prefix,
                       "--with-mpi=%s" % mpi.prefix,
                       "--with-unwind=%s" % spec['libunwind'].prefix,
                       "--with-boost=%s" % spec['boost'].prefix,
                       "--with-dwarf=%s" % spec['libdwarf'].prefix,
                       "--with-elf=%s" % spec['elf'].prefix,
                       "--with-xml-prefix=%s" % spec['libxml2'].prefix,
                       "--with-binutils=%s" % spec['binutils'].prefix]

        config_args += (["--with-papi=%s" % spec['papi'].prefix]
                        if '+papi' in self.spec else
                        ["--without-papi"])

        config_args += (["--with-dyninst=%s" % spec['dyninst'].prefix,
                         "--with-dyninst-headers=%s" %
                         spec['dyninst'].prefix.include,
                         "--with-dyninst-libs=%s" % spec['dyninst'].prefix.lib]
                        if '+dyninst' in self.spec else
                        ["--without-dyninst"])

        if spec.satisfies("^dyninst@9.3.0:"):
            make.add_default_arg('CXXFLAGS=-std=c++11')
            config_args.append('CXXFLAGS=-std=c++11')

        # This was added due to configure failure
        # https://www.gnu.org/software/gettext/FAQ.html#integrating_undefined
        config_args.append('LDFLAGS=-lintl')

        configure(*config_args)

        make()
        make("install", parallel=False)
