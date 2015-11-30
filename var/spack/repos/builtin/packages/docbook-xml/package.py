import os
import glob
from spack import *


class DocbookXml(Package):
    """Docbook DTD XML files."""
    homepage = "http://www.oasis-open.org/docbook"
    url = "http://www.oasis-open.org/docbook/xml/4.5/docbook-xml-4.5.zip"

    version('4.5', '03083e288e87a7e829e437358da7ef9e')

    def install(self, spec, prefix):
        cp = which('cp')

        install_args = ['-a', '-t', prefix]
        install_args.extend(glob.glob('*'))

        cp(*install_args)
