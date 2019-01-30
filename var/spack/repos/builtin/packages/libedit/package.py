# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libedit(AutotoolsPackage):
    """An autotools compatible port of the NetBSD editline library"""
    homepage = "http://thrysoee.dk/editline/"
    url      = "http://thrysoee.dk/editline/libedit-20170329-3.1.tar.gz"

    version('3.1-20170329', 'c57a0690e62ef523c083598730272cfd')
    version('3.1-20160903', '0467d27684c453a351fbcefebbcb16a3')
    version('3.1-20150325', '43cdb5df3061d78b5e9d59109871b4f6')

    depends_on('ncurses')

    def url_for_version(self, version):
        url = "http://thrysoee.dk/editline/libedit-{0}-{1}.tar.gz"
        return url.format(version[-1], version.up_to(-1))
