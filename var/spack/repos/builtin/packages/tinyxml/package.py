from spack import *

class Tinyxml(Package):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml/"
    url      = "https://sourceforge.net/projects/tinyxml/files/tinyxml/2.6.2/tinyxml_2_6_2.tar.gz"

    version('2.6.2', 'cba3f50dd657cb1434674a03b21394df9913d764', url=url)
    variant("debug", default=False, description="Installs with debug options")

    def install(self, spec, prefix):
        from os.path import dirname
        from shutil import copyfile
        copyfile(join_path(dirname(__file__), "CMakeLists.txt"), "CMakeLists.txt")

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
