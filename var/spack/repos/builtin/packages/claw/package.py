from spack import *


class Claw(CMakePackage):
    """CLAW Compiler targets performance portability problem in climate and
       weather application written in Fortran. From a single source code, it
       generates architecture specific code decorated with OpenMP or OpenACC"""

    homepage = 'https://claw-project.github.io/'
    git      = 'https://github.com/claw-project/claw-compiler.git'

    version('1.1.0', tag='v1.1.0', submodules=True)

    depends_on('cmake@3.0:', type='build')
    depends_on('java@7:')
    depends_on('ant@1.9:')
    depends_on('libxml2')

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append('-DOMNI_CONF_OPTION=--with-libxml2={0}'.
                    format(spec['libxml2'].prefix))

        return args
