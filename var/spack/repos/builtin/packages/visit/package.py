from spack import *


class Visit(Package):
    """VisIt is an Open Source, interactive, scalable, visualization, animation and analysis tool."""
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    url = "http://portal.nersc.gov/project/visit/releases/2.10.1/visit2.10.1.tar.gz"

    version('2.10.1', '3cbca162fdb0249f17c4456605c4211e')

    depends_on("vtk@6.1.0~opengl2")
    depends_on("qt@4.8.6")
    depends_on("python")
    # TODO: Other package dependencies from spack

    def install(self, spec, prefix):

        feature_args = std_cmake_args[:]
        feature_args = ["-DVTK_MAJOR_VERSION=6",
                        "-DVTK_MINOR_VERSION=1",
                        "-DCMAKE_INSTALL_PREFIX:PATH=%s" % spec.prefix,
                        "-DVISIT_LOC_QMAKE_EXE:FILEPATH=%s/qmake-qt4" % spec['qt'].prefix.bin,
                        "-DPYTHON_EXECUTABLE:FILEPATH=%s/python" % spec['python'].prefix.bin]

        cmake('./src', *feature_args)

        make()
        make("install")
