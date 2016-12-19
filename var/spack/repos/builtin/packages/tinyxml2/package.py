from spack import *

class Tinyxml2(Package):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml2/"
    url      = "https://github.com/leethomason/tinyxml2/archive/3.0.0.tar.gz"

    version('4.0.1', '08570d385788f6b02f50f5fd9df32a9d4f8482cc')
    version('4.0.0', '7a6f0858d75f360922f3ca272f7067e8cdf00489')
    version('3.0.0', '07acaae49f7dd3dab790da4fe72d0c7ef0d116d1')
    version('2.2.0', '7869aa08241ce16f93ba3732c1cde155b1f2b6a0')
    version('2.1.0', '70ef3221bdc190fd8fc50cdd4a6ef440f44b74dc')
    version('2.0.2', 'c78a4de58540e2a35f4775fd3e577299ebd15117')
    variant("debug", default=False, description="Installs with debug options")

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")
