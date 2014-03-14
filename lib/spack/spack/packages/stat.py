# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install v
#
# You can always get back here to change things with:
#
#     spack edit v
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Stat(Package):
    """Library to create, manipulate, and export graphs Graphlib."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/lee218llnl/stat/archive/v2.0.0.tar.gz"

    versions = { '2.0.0' : 'c7494210b0ba26b577171b92838e1a9b', }

    depends_on('libdwarf')
    depends_on('dyninst')
    depends_on('graphlib')
    depends_on('mrnet')

    def install(self, spec, prefix):
        my_mrnet = spec['mrnet']

        # FIXME: Modify the configure line to suit your build system here.
        configure("--enable-gui", "--prefix=%s" %prefix, "--with-launchmon=/collab/usr/global/tools/launchmon/chaos_5_x86_64_ib/launchmon-1.0.0-20140312", "--with-mrnet=%s" %my_mrnet.prefix)

        # FIXME: Add logic to build and install here
        make(parallel=False)
        make("install")
