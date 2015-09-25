# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install trilinos
#
# You can always get back here to change things with:
#
#     spack edit trilinos
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Trilinos(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://trilinos.csbsju.edu/download/files/trilinos-12.2.1-Source.tar.gz"

    version('12.2.1' , '6161926ea247863c690e927687f83be9')
    version('12.0.1' , 'bd99741d047471e127b8296b2ec08017')
    version('11.14.3', '2f4f83f8333e4233c57d0f01c4b57426')
    version('11.14.2', 'a43590cf896c677890d75bfe75bc6254')
    version('11.14.1', '40febc57f76668be8b6a77b7607bb67f')

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        cmake('.', *std_cmake_args)

        # FIXME: Add logic to build and install here
        make()
        make("install")
