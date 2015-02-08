# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install systemd
#
# You can always get back here to change things with:
#
#     spack edit systemd
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class Systemd(Package):
    """Systemd is a suite of basic building blocks for a Linux system."""

    homepage = "http://www.freedesktop.org/wiki/Software/systemd/"
    url      = "http://www.freedesktop.org/software/systemd/systemd-218.tar.xz"

    version('218', '4e2c511b0a7932d7fc9d79822273aac6')

    depends_on("gperf")
    depends_on("coreutils@8.16:") # ln --relative
    depends_on("util-linux") # libmount
    depends_on("python@2.7:")
    depends_on("gcc@4.5:") # pragma gcc diagnostic not allowed inside functions

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, 
                "CC=%s/gcc -std=gnu99" % spec['gcc'].prefix.bin)

        make()
        make("install")
