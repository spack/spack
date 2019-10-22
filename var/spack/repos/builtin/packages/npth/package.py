# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Npth(AutotoolsPackage):
    """nPth is a library to provide the GNU Pth API and thus a
       non-preemptive threads implementation."""

    homepage = "https://gnupg.org/software/npth/index.html"
    url = "https://gnupg.org/ftp/gcrypt/npth/npth-1.5.tar.bz2"

    version('1.5', sha256='294a690c1f537b92ed829d867bee537e46be93fbd60b16c04630fbbfcd9db3c2')
    version('1.4', sha256='8915141836a3169a502d65c1ebd785fcc6d406cae5ee84474272ebf2fa96f1f2')
