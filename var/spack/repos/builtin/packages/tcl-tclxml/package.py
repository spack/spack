# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TclTclxml(AutotoolsPackage):
    """TclXML is an API for parsing XML documents using the Tcl scripting
    language. It is also a package including a DOM implementation (TclDOM) and
    XSL Transformations (TclXSLT). These allow Tcl scripts to read, manipulate
    and write XML documents."""

    homepage   = "http://tclxml.sourceforge.net/tclxml.html"
    url        = "https://sourceforge.net/projects/tclxml/files/TclXML/3.2/tclxml-3.2.tar.gz"
    list_url   = "https://sourceforge.net/projects/tclxml/files/TclXML/"
    list_depth = 1

    version('3.2', '9d1605246c899eff7db591bca3c23200')
    version('3.1', '35de63a4ceba7a6fdb85dd1a62f2e881')

    extends('tcl')

    depends_on('tcl-tcllib')
    depends_on('libxml2')
    depends_on('libxslt')

    def configure_args(self):
        return [
            '--exec-prefix={0}'.format(
                self.prefix),
            '--with-tcl={0}/lib'.format(
                self.spec['tcl'].prefix),
            '--with-xml2-config={0}/bin/xml2-config'.format(
                self.spec['libxml2'].prefix),
            '--with-xslt-config={0}/bin/xslt-config'.format(
                self.spec['libxslt'].prefix),
        ]
