# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Otf(Package):
    """To improve scalability for very large and massively parallel
       traces the Open Trace Format (OTF) is developed at ZIH as a
       successor format to the Vampir Trace Format (VTF3)."""

    homepage = "http://tu-dresden.de/die_tu_dresden/zentrale_einrichtungen/zih/forschung/projekte/otf/index_html/document_view?set_language=en"
    url      = "http://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz"

    version('1.12.5salmon', 'bf260198633277031330e3356dcb4eec')

    depends_on('zlib')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--without-vtf3',
                  '--with-zlib',
                  '--with-zlibsymbols')
        make()
        make("install")
