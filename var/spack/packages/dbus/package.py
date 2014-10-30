# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install dbus
#
# You can always get back here to change things with:
#
#     spack edit dbus
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Dbus(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://dbus.freedesktop.org/releases/dbus/dbus-1.8.8.tar.gz"

    version('1.9.0', 'ec6895a4d5c0637b01f0d0e7689e2b36')
    version('1.8.8', 'b9f4a18ee3faa1e07c04aa1d83239c43')
    version('1.8.6', '6a08ba555d340e9dfe2d623b83c0eea8')
    version('1.8.4', '4717cb8ab5b80978fcadf2b4f2f72e1b')
    version('1.8.2', 'd6f709bbec0a022a1847c7caec9d6068')

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
