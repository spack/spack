from spack import *

class Memaxes(Package):
    """MemAxes is a visualizer for sampled memory trace data."""

    homepage = "https://github.com/scalability-llnl/MemAxes"

    version('0.5', 'b0f561d48aa7301e028d074bc4b5751b',
            url='https://github.com/scalability-llnl/MemAxes/archive/v0.5.tar.gz')

    depends_on("cmake@2.8.9:")
    depends_on("qt@5:")
    depends_on("vtk")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")

