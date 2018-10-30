# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LxdeLibfm(AutotoolsPackage):
    """LXDE PCManFM libfm component"""

    homepage = "https://wiki.lxde.org/en/PCManFM"
    url      = "http://downloads.sourceforge.net/project/pcmanfm/PCManFM%20%2B%20Libfm%20%28tarball%20release%29/LibFM/libfm-1.2.4.tar.xz"

    version('1.2.4', '74997d75e7e87dc73398746fd373bf52')

    variant('extraonly', default=False,
            description="Needed to avoid circulare dep with menucache")
    depends_on('libtool', type='build')
    depends_on('intltool', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('perl', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('cairo')
    depends_on('gtkplus')
    depends_on('glib')
    depends_on('lxde-menu-cache', when='~extraonly')

    def configure_args(self):
        args = []
        if '+extraonly' in self.spec:
            args.append('--with-extra-only')
        return args
