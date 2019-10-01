# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wxpropgrid(Package):
    """wxPropertyGrid is a property sheet control for wxWidgets. In
       other words, it is a specialized two-column grid for editing
       properties such as strings, numbers, flagsets, string arrays,
       and colours."""
    homepage = "http://wxpropgrid.sourceforge.net/"
    url      = "http://prdownloads.sourceforge.net/wxpropgrid/wxpropgrid-1.4.15-src.tar.gz"

    version('1.4.15', 'f44b5cd6fd60718bacfabbf7994f1e93')

    depends_on("wxwidgets")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--with-wxdir=%s" %
                  spec['wx'].prefix.bin, "--enable-unicode")

        make()
        make("install")
