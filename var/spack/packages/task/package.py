from spack import *

class Task(Package):
    """Feature-rich console based todo list manager"""
    homepage = "http://www.taskwarrior.org"
    url      = "http://taskwarrior.org/download/task-2.4.4.tar.gz"

    version('2.4.4', '517450c4a23a5842df3e9905b38801b3')

    depends_on("gnutls")
    depends_on("libuuid")
    # depends_on("gcc@4.8:")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('-DCMAKE_BUILD_TYPE=release',
                  '..',
                  *std_cmake_args)
            make()
            make("install")
