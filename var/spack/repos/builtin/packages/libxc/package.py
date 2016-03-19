from spack import *

class Libxc(Package):
    """
    Libxc is a library of exchange-correlation functionals for density-functional theory. 
    The aim is to provide a portable, well tested and reliable set of exchange and 
    correlation functionals that can be used by all the ETSF codes and also other codes.
    In Libxc you can find different types of functionals: LDA, GGA, hybrids, and mGGA (experimental). 
    These functionals depend on local information, in the sense that the value of the
    potential at a given point depends only on the values of the density -- and the gradient 
    of the density and the kinetic energy density, for the GGA and mGGA cases -- at a given point:

    It can calculate the functional itself and its derivative; for some functionals, 
    higher-order derivatives are available.
    Libxc is written in C and has Fortran bindings. It is released under the LGPL license (v. 3.0). 
    Contributions are welcome."""

    homepage = "http://www.tddft.org/programs/octopus/wiki/index.php/Libxc"
    url      = "http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-2.2.2.tar.gz"

    version('2.2.2', 'd9f90a0d6e36df6c1312b6422280f2ec')

    # FIXME: This version does not compile due an include file in F90 code!
    #version('2.0.0', 'b15303a3c1f82d157e474ec97edafd83')

    def install(self, spec, prefix):
        configure("--enable-fortran", "--enable-static", "--enable-shared", "--prefix=%s" % prefix)

        make(parallel=False)
        make("install")
