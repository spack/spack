from spack import *

class Googletest(Package):
    """Google test framework for C++.  Also called gtest."""
    homepage = "https://github.com/google/googletest"
    url      = "https://github.com/google/googletest/tarball/release-1.7.0"

    version('1.7.0', '5eaf03ed925a47b37c8e1d559eb19bc4')

    depends_on("cmake")

    def install(self, spec, prefix):
        which('cmake')('.', *std_cmake_args)

        make()

        # Google Test doesn't have a make install
        # We have to do our own install here.
	install_tree('include', prefix.include)

        mkdirp(prefix.lib)
	install('./libgtest.a', '%s' % prefix.lib)
	install('./libgtest_main.a', '%s' % prefix.lib)

