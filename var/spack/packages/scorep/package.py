# FIXME: Add copyright statement

from spack import *

class Scorep(Package):
    """The Score-P measurement infrastructure is a highly scalable and 
       easy-to-use tool suite for profiling, event tracing, and online 
       analysis of HPC applications."""

    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "http://www.vi-hps.org/upload/packages/scorep/scorep-1.2.3.tar.gz"

    version('1.2.3', '4978084e7cbd05b94517aa8beaea0817')

    depends_on("mpi")
    depends_on("papi")
    depends_on("otf2@1.2:1.2.1") 
    depends_on("opari2")
    depends_on("cube")

    def install(self, spec, prefix):
        configure_args = ["--prefix=%s" % prefix,
                          "--with-otf2=%s" % spec['otf2'].prefix.bin,
                          "--with-opari2=%s" % spec['opari2'].prefix.bin,
                          "--with-cube=%s" % spec['cube'].prefix.bin,
                          "--with-papi-header=%s" % spec['papi'].prefix.include,
                          "--with-papi-lib=%s" % spec['papi'].prefix.lib,
                          "--enable-shared"]

        if spec.satisfies('%gcc'):
            configure_args.append('--with-nocross-compiler-suite=gcc')
        if spec.satisfies('%intel'):
            configure_args.append('--with-nocross-compiler-suite=intel')
        if spec.satisfies('%pgi'):
            configure_args.append('--with-nocross-compiler-suite=pgi')

        configure(*configure_args)

        make()
        make("install")
