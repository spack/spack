# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Silo(AutotoolsPackage):
    """Silo is a library for reading and writing a wide variety of scientific
       data to binary, disk files."""

    homepage = "http://wci.llnl.gov/simulation/computer-codes/silo"
    url      = "https://wci.llnl.gov/content/assets/docs/simulation/computer-codes/silo/silo-4.10.2/silo-4.10.2.tar.gz"

    version('4.10.2', sha256='3af87e5f0608a69849c00eb7c73b11f8422fa36903dd14610584506e7f68e638', preferred=True)
    version('4.10.2-bsd', sha256='4b901dfc1eb4656e83419a6fde15a2f6c6a31df84edfad7f1dc296e01b20140e',
            url="https://wci.llnl.gov/content/assets/docs/simulation/computer-codes/silo/silo-4.10.2/silo-4.10.2-bsd.tar.gz")
    version('4.9', sha256='90f3d069963d859c142809cfcb034bc83eb951f61ac02ccb967fc8e8d0409854')
    version('4.8', sha256='c430c1d33fcb9bc136a99ad473d535d6763bd1357b704a915ba7b1081d58fb21')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('shared', default=True, description='Build shared libraries')
    variant('silex', default=False,
            description='Builds Silex, a GUI for viewing Silo files')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('mpi', default=True,
            description='Compile with MPI Compatibility')

    depends_on('hdf5~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('qt', when='+silex')
    depends_on('zlib')

    patch('remove-mpiposix.patch', when='@4.8:4.10.2')

    def flag_handler(self, name, flags):
        if name == 'ldflags' and self.spec['hdf5'].satisfies('~shared'):
            flags.append('-ldl')
        return (flags, None, None)

    @when('%clang@9:')
    def patch(self):
        # Clang 9 and later include macro definitions in <math.h> that conflict
        # with typedefs DOMAIN and RANGE used in Silo plugins.
        # It looks like the upstream fpzip repo has been fixed, but that change
        # hasn't yet made it into silo.
        # https://github.com/LLNL/fpzip/blob/master/src/pcmap.h

        def repl(match):
            # Change macro-like uppercase to title-case.
            return match.group(1).title()

        files_to_filter = [
            "src/fpzip/codec.h",
            "src/fpzip/pcdecoder.inl",
            "src/fpzip/pcencoder.inl",
            "src/fpzip/pcmap.h",
            "src/fpzip/pcmap.inl",
            "src/fpzip/read.cpp",
            "src/fpzip/write.cpp",
            "src/hzip/hzmap.h",
            "src/hzip/hzresidual.h",
        ]

        filter_file(r'\b(DOMAIN|RANGE|UNION)\b', repl, *files_to_filter)

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--with-hdf5=%s,%s' % (spec['hdf5'].prefix.include,
                                   spec['hdf5'].prefix.lib),
            '--with-zlib=%s,%s' % (spec['zlib'].prefix.include,
                                   spec['zlib'].prefix.lib),
            '--enable-install-lite-headers',
            '--enable-fortran' if '+fortran' in spec else '--disable-fortran',
            '--enable-silex' if '+silex' in spec else '--disable-silex',
            '--enable-shared' if '+shared' in spec else '--disable-shared',
        ]

        if '+silex' in spec:
            config_args.append('--with-Qt-dir=%s' % spec['qt'].prefix)

        if '+pic' in spec:
            config_args += [
                'CFLAGS={0}'.format(self.compiler.pic_flag),
                'CXXFLAGS={0}'.format(self.compiler.pic_flag),
                'FCFLAGS={0}'.format(self.compiler.pic_flag)]

        if '+mpi' in spec:
            config_args.append('CC=%s' % spec['mpi'].mpicc)
            config_args.append('CXX=%s' % spec['mpi'].mpicxx)
            config_args.append('FC=%s' % spec['mpi'].mpifc)

        return config_args
