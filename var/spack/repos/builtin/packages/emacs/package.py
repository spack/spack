# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install emacs
#
# You can always get back here to change things with:
#
#     spack edit emacs
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Emacs(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://ftp.gnu.org/gnu/emacs/emacs-24.5.tar.gz"

    version('24.5', 'd74b597503a68105e61b5b9f6d065b44')

    # FIXME: Add dependencies if this package requires them.
    depends_on('ncurses')

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
