# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Motif(AutotoolsPackage):
    """"
    Motif - Graphical user interface (GUI)
    specification and the widget toolkit
    """
    homepage = "http://motif.ics.com/"
    url = "http://cfhcable.dl.sourceforge.net/project/motif/Motif%202.3.8%20Source%20Code/motif-2.3.8.tar.gz"

    version('2.3.8', sha256='859b723666eeac7df018209d66045c9853b50b4218cecadb794e2359619ebce7')

    depends_on("flex")
    depends_on("libx11")
    depends_on("libxt")
    depends_on("libxext")
    depends_on("libxft")
    depends_on("libxcomposite")
    depends_on("libxfixes")
    depends_on("xbitmaps")
    depends_on("jpeg")
