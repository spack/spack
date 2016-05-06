from spack import *

class Antlr(Package):
    
    homepage = "http://www.antlr.org"
    url      = "https://github.com/antlr/antlr/tarball/v2.7.7"

    # NOTE: This requires that a system Java be available.
    # Spack does not yet know how to install Java compilers

    # Notes from http://nco.sourceforge.net/#bld
    # The first steps to build (i.e., compile, for the most part) NCO from
    # source code are to install the pre-requisites: ANTLR version 2.7.7
    # (like this one not version 3.x or 4.x!) (required for ncap2)... ANTLR
    # binaries from major distributions are pre-built with the source patch
    # necessary to allow NCO to link to ANTLR... The ANTLR source file
    # CharScanner.hpp must include this line: #include <cstring> or else
    # ncap2 will not compile (this tarball is already patched).
    version('2.7.7', '914865e853fe8e1e61a9f23d045cb4ab',
        # Patched version as described above
        url='http://dust.ess.uci.edu/tmp/antlr-2.7.7.tar.gz')
        # Unpatched version
        # url='http://dust.ess.uci.edu/nco/antlr-2.7.7.tar.gz')

    variant('cxx', default=False, description='Enable ANTLR for C++')
    variant('java', default=False, description='Enable ANTLR for Java')
    variant('python', default=False, description='Enable ANTLR for Python')
    variant('csharp', default=False, description='Enable ANTLR for Csharp')


    def install(self, spec, prefix):
        # Check for future enabling of variants
        for v in ('+java', '+python', '+csharp'):
            if v in spec:
                raise Error('Illegal variant %s; for now, Spack only knows how to build antlr or antlr+cxx')

        config_args = [
            '--prefix=%s' % prefix,
            '--%s-cxx' % ('enable' if '+cxx' in spec else 'disable'),
            '--%s-java' % ('enable' if '+java' in spec else 'disable'),
            '--%s-python' % ('enable' if '+python' in spec else 'disable'),
            '--%s-csharp' % ('enable' if '+csharp' in spec else 'disable')]

        # which('autoreconf')('-iv')
        configure(*config_args)
        make()
        make("install")
