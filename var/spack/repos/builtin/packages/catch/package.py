from spack import *

class Catch(Package):
    """Catch tests"""

    homepage = "https://github.com/philsquared/Catch"
    url      = "https://github.com/philsquared/Catch/archive/v1.3.0.tar.gz"

    version('1.3.0', 'e13694aaff72817d02af8ed27d077cd261b6e857')

    def install(self, spec, prefix):
        from os.path import join
        mkdirp(prefix.include)
        install(join('single_include', 'catch.hpp'), prefix.include)
        # fakes out spack so it installs a module file
        mkdirp(join(prefix, 'bin'))
