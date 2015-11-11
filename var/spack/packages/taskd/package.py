from spack import *

class Taskd(Package):
    """TaskWarrior task synchronization daemon"""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.taskwarrior.org"
    url      = "http://taskwarrior.org/download/taskd-1.1.0.tar.gz"

    version('1.1.0', 'ac855828c16f199bdbc45fbc227388d0')

    depends_on("libuuid")
    depends_on("gnutls")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('-DCMAKE_BUILD_TYPE=release',
                  '..',
                  *std_cmake_args)
            make()
            make("install")
