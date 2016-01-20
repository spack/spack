from spack import *

class Vtk(Package):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization. """
    homepage = "http://www.vtk.org"
    url      = "http://www.vtk.org/files/release/6.1/VTK-6.1.0.tar.gz"

    version('6.1.0', '25e4dfb3bad778722dcaec80cd5dab7d')

    depends_on("qt")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = [
                "..",
                "-DBUILD_SHARED_LIBS=ON",
                # Disable wrappers for other languages.
                "-DVTK_WRAP_PYTHON=OFF",
                "-DVTK_WRAP_JAVA=OFF",
                "-DVTK_WRAP_TCL=OFF"]
            cmake_args.extend(std_cmake_args)

            # Enable Qt support here.
            cmake_args.extend([
                "-DQT_QMAKE_EXECUTABLE:PATH=%s/qmake" % spec['qt'].prefix.bin,
                "-DVTK_Group_Qt:BOOL=ON",
                # Ignore webkit because it's hard to build w/Qt
                "-DVTK_Group_Qt=OFF",
                "-DModule_vtkGUISupportQt:BOOL=ON",
                "-DModule_vtkGUISupportQtOpenGL:BOOL=ON"
                ])

            if spec['qt'].satisfies('@5'):
                cmake_args.append("-DVTK_QT_VERSION:STRING=5")

            cmake(*cmake_args)
            make()
            make("install")
