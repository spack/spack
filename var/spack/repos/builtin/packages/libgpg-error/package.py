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


class LibgpgError(AutotoolsPackage):
    """Libgpg-error is a small library that defines common error
       values for all GnuPG components. Among these are GPG, GPGSM,
       GPGME, GPG-Agent, libgcrypt, Libksba, DirMngr, Pinentry,
       SmartCard Daemon and possibly more in the future. """

    homepage = "https://www.gnupg.org/related_software/libgpg-error"
    url = "https://gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-1.27.tar.bz2"

    version('1.27', '5217ef3e76a7275a2a3b569a12ddc989')
    version('1.21', 'ab0b5aba6d0a185b41d07bda804fd8b2')
    version('1.18', '12312802d2065774b787cbfc22cc04e9')
