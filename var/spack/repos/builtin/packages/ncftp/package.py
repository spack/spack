# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ncftp(AutotoolsPackage):
    """NcFTP Client is a set of application programs implementing the
       File Transfer Protocol."""

    homepage = "http://www.ncftp.com/"
    url      = "ftp://ftp.ncftp.com/ncftp/ncftp-3.2.6-src.tar.gz"

    version('3.2.6', 'e7cce57ef6274d4c7433ffe28ffe0a71')

    depends_on('ncurses')
