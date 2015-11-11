from spack import *

class PyTrianglePlot(Package):
    """Make some beautiful corner plots of samples."""
    homepage = "https://github.com/dfm/triangle.py"
    version("0.0.6", "970a35a9bde6002d673e3188fe39f0ed",
            url="https://pypi.python.org/packages/source/t/triangle_plot/triangle_plot-0.0.6.tar.gz")

    extends("python")

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=%s" % prefix)
