from spack import *

class Gbenchmark(Package):
    """A microbenchmark support library"""

    homepage = "https://github.com/google/benchmark"
    url      = "https://github.com/google/benchmark/archive/v1.0.0.tar.gz"

    version('1.1.0', '8c539bbe2a212618fa87b6c38fba087100b6e4ae',
            url='https://github.com/google/benchmark/archive/v1.1.0.tar.gz')
    version('1.0.0', '4f778985dce02d2e63262e6f388a24b595254a93')
    variant("debug", default=False, description="Installs with debug options")

    def patch(self):
        filter_file(
            r'add_cxx_compiler_flag..fstrict.aliasing.',
            r'##### add_cxx_compiler_flag(-fstrict-aliasing)',
            'CMakeLists.txt'
        )
        filter_file(
            r'add_cxx_compiler_flag..Werror',
            r'##### add_cxx_compiler_flag(-Werror',
            'CMakeLists.txt'
        )

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        if self.compiler.name == 'intel':
            options.append("-DCMAKE_CXX_FLAGS='-no-ansi-alias -fno-strict-aliasing'")
            options.append("-DCMAKE_C_FLAGS='-no-ansi-alias -fno-strict-aliasing'")
            options.append("-DBENCHMARK_ENABLE_TESTING=OFF")
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
