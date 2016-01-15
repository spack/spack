# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install espresso
#
# You can always get back here to change things with:
#
#     spack edit espresso
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Espresso(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://quantum-espresso.org"
    url      = "http://www.qe-forge.org/gf/download/frsrelease/199/855/espresso-5.2.1.tar.gz"

    version('5.2.1', 'da3ec5302e4343804e65de60f6004c2d')
    variant('mpi', default=True, description='Build Quantum-ESPRESSO with mpi support')
    variant('openmp', default=False, description='Build Quantum-ESPRESSO with mpi openmp')
    variant('scalapack', default=False, description='Build Quantum-ESPRESSO with mpi openmp')


    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")
    depends_on('mpi', when='+mpi')


#    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
#        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
#        make()
#        make("install")

    def install(self, spec, prefix):
        # TAU isn't happy with directories that have '@' in the path.  Sigh.

        # TAU configure, despite the name , seems to be a manually written script (nothing related to autotools).
        # As such it has a few #peculiarities# that make this build quite hackish.
        options = ["-prefix=%s" % prefix,
                   "--enable-parallel"]

        if '+openmp' in spec:
            options.append('--enable-openmp')

        if '+scalapack' in spec:
            options.append('--with-scalapack=yes')

        configure(*options)
        make("all")
        make("install")

