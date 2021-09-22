# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pgplot(MakefilePackage):
    """PGPLOT Graphics Subroutine Library

    The PGPLOT Graphics Subroutine Library is a Fortran- or
    C-callable, device-independent graphics package for making
    simple scientific graphs. It is intended for making
    graphical images of publication quality with minimum effort
    on the part of the user. For most applications, the program
    can be device-independent, and the output can be directed to
    the appropriate device at run time."""

    homepage = "https://sites.astro.caltech.edu/~tjp/pgplot/"
    url      = "ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot5.2.tar.gz"

    maintainers = ['eschnett']

    version('5.2.2',
            url="ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot5.2.tar.gz",
            sha256='a5799ff719a510d84d26df4ae7409ae61fe66477e3f1e8820422a9a4727a5be4')

    # Replace hard-coded compilers and options by tokens, so that Spack can
    # edit the file more easily
    patch('g77_gcc.conf.patch')

    parallel = False

    def edit(self, spec, prefix):
        substitutions = [
            ('@CCOMPL@', self.compiler.cc),
            ('@CFLAGC@', ("-Wall -fPIC -DPG_PPU -O -std=c89 " +
                          "-Wno-error=implicit-function-declaration")),
            ('@FCOMPL@', self.compiler.f77),
            ('@FFLAGC@', "-Wall -fPIC -O -ffixed-line-length-none" +
                (" -fallow-invalid-boz" if spec.satisfies('%gcc@10:') else "")),
            ('@LIBS@', "-lgfortran"),
            ('@SHARED_LD@', self.compiler.cc + " -shared -o $SHARED_LIB -lgfortran"),
        ]
        conf = join_path(
            self.stage.source_path, 'sys_linux/g77_gcc.conf'
        )
        for key, value in substitutions:
            filter_file(key, value, conf)

    def build(self, spec, prefix):
        makemake = which('./makemake')
        makemake(self.build_directory, 'linux', 'g77_gcc')
        make()
        make('clean')
        make('cpg')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('cpgdemo', prefix.bin)
        install('pgbind', prefix.bin)
        install('pgdemo1', prefix.bin)
        install('pgdemo2', prefix.bin)
        install('pgdemo3', prefix.bin)
        install('pgdemo4', prefix.bin)
        install('pgdemo5', prefix.bin)
        install('pgdemo6', prefix.bin)
        install('pgdemo7', prefix.bin)
        install('pgdemo8', prefix.bin)
        install('pgdemo9', prefix.bin)
        install('pgdemo10', prefix.bin)
        install('pgdemo11', prefix.bin)
        install('pgdemo12', prefix.bin)
        install('pgdemo13', prefix.bin)
        install('pgdemo14', prefix.bin)
        install('pgdemo15', prefix.bin)
        install('pgdemo16', prefix.bin)
        install('pgdemo17', prefix.bin)
        mkdirp(prefix.include)
        install('cpgplot.h', prefix.include)
        mkdirp(prefix.lib)
        install('libcpgplot.a', prefix.lib)
        install('libpgplot.a', prefix.lib)
        install('libpgplot.so', prefix.lib)

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            "lib*pgplot", root=self.prefix, shared=shared, recursive=True
        )
