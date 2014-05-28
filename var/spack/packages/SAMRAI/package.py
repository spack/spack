# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install SAMRAI
#
# You can always get back here to change things with:
#
#     spack edit SAMRAI
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Samrai(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "https://computation-rnd.llnl.gov/SAMRAI/confirm.php"
    url      = "https://computation-rnd.llnl.gov/SAMRAI/download/SAMRAI-v3.7.3.tar.gz"
	list_url = homepage

    versions = {
      '3.7.3'      : '12d574eacadf8c9a70f1bb4cd1a69df6',
      '3.7.2'      : 'f6a716f171c9fdbf3cb12f71fa6e2737',
      '3.6.3-beta' : 'ef0510bf2893042daedaca434e5ec6ce',
      '3.5.2-beta' : 'd072d9d681eeb9ada15ce91bea784274',
      '3.5.0-beta' : '1ad18a319fc573e12e2b1fbb6f6b0a19',
      '3.4.1-beta' : '00814cbee2cb76bf8302aff56bbb385b',
      '3.3.3-beta' : '1db3241d3e1cab913dc310d736c34388',
      '3.3.2-beta' : 'e598a085dab979498fcb6c110c4dd26c',
      '2.4.4'      : '04fb048ed0efe7c531ac10c81cc5f6ac',
    }

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
