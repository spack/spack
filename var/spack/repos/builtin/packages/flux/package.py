##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os

class Flux(Package):
    """ A next-generation resource manager (pre-alpha) """

    homepage = "https://github.com/flux-framework/flux-core"
    url      = "https://github.com/flux-framework/flux-core"

    version('master', branch='master', git='https://github.com/flux-framework/flux-core')

    # Also needs autotools, but should use the system version if available
    depends_on("zeromq@4.0.4:")
    depends_on("czmq@2.2:")
    depends_on("hwloc")
    depends_on("lua@5.1:5.1.99")
    depends_on("munge")
    depends_on("libjson-c")
    depends_on("libxslt")
    depends_on("python")
    depends_on("py-cffi")

    # TODO: This provides a catalog, hacked with environment below for now
    depends_on("docbook-xml")
    depends_on("asciidoc")

    def install(self, spec, prefix):
        # Bootstrap with autotools
        bash = which('bash')
        bash('./autogen.sh')
        bash('./autogen.sh') #yes, twice, intentionally

        # Fix asciidoc dependency on xml style sheets and whatnot
        os.environ['XML_CATALOG_FILES'] = os.path.join(spec['docbook-xml'].prefix,
                                                       'catalog.xml')
        # Configure, compile & install
        configure("--prefix=" + prefix)
        make("install", "V=1")

