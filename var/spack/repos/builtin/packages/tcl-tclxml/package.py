##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
