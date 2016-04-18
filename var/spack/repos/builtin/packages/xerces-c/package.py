# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install xerces-c
#
# You can always get back here to change things with:
#
#     spack edit xerces-c
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class XercesC(Package):
    """ Xerces-C++ is a validating XML parser written in a portable subset of C++.
    Xerces-C++ makes it easy to give your application the ability to read and
    write XML data. A shared library is provided for parsing, generating,
    manipulating, and validating XML documents using the DOM, SAX, and SAX2 APIs.
    """

    homepage = "https://xerces.apache.org/xerces-c"
    url      = "https://www.apache.org/dist/xerces/c/3/sources/xerces-c-3.1.3.tar.gz"
    version('3.1.3', '70320ab0e3269e47d978a6ca0c0e1e2d')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--disable-network")
        make("clean")
        make()
        make("install")

