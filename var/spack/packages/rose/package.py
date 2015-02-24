#------------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
#------------------------------------------------------------------------------

from spack import *

class Rose(Package):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url      = "https://github.com/rose-compiler/edg4x-rose"

    version('master', branch='master', git='https://github.com/rose-compiler/edg4x-rose.git')

    patch('add_spack_compiler_recognition.patch')

    depends_on("autoconf@2.69")
    depends_on("automake@1.14")
    depends_on("libtool@2.4")
    depends_on("boost@1.54.0")
    depends_on("jdk@8u25-linux-x64")

    def install(self, spec, prefix):
        # Bootstrap with autotools
        bash = which('bash')
        bash('build')

        # Configure, compile & install
        with working_dir('rose-build', create=True):
            boost = spec['boost']

            configure = Executable('../configure')
            configure("--prefix=" + prefix,
                      "--with-boost=" + boost.prefix,
                      "--disable-boost-version-check")
            make("install-core")

