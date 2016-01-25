from spack import *

class Silo(Package):
    """Silo is a library for reading and writing a wide variety of scientific data to binary, disk files."""

    homepage = "http://wci.llnl.gov/simulation/computer-codes/silo"
    url      = "https://wci.llnl.gov/content/assets/docs/simulation/computer-codes/silo/silo-4.8/silo-4.8.tar.gz"

    #version('4.9', 'a83eda4f06761a86726e918fc55e782a')
    version('4.8', 'b1cbc0e7ec435eb656dc4b53a23663c9')

    depends_on("hdf5@:1.8.12")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-hdf5=%s" %spec['hdf5'].prefix)

        make()
        make("install")
