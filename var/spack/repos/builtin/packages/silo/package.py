from spack import *

class Silo(Package):
    """Silo is a library for reading and writing a wide variety of scientific
       data to binary, disk files."""

    homepage = "http://wci.llnl.gov/simulation/computer-codes/silo"
    url      = "https://wci.llnl.gov/content/assets/docs/simulation/computer-codes/silo/silo-4.8/silo-4.8.tar.gz"

    version('4.8', 'b1cbc0e7ec435eb656dc4b53a23663c9')

    variant('fortran', default=True, description='Enable Fortran support')

    depends_on("hdf5")

    def install(self, spec, prefix):
        config_args = [
            '--enable-fortran' if '+fortran' in spec else '--disable-fortran',
        ]

        configure(
            "--prefix=%s" % prefix,
            "--with-hdf5=%s,%s" % (spec['hdf5'].prefix.include, spec['hdf5'].prefix.lib),
            "--with-zlib=%s,%s" % (spec['zlib'].prefix.include, spec['zlib'].prefix.lib),
            *config_args)

        make()
        make("install")
