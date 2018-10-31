# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Npth(AutotoolsPackage):
    """nPth is a library to provide the GNU Pth API and thus a
       non-preemptive threads implementation."""

    homepage = "https://gnupg.org/software/npth/index.html"
    url = "https://gnupg.org/ftp/gcrypt/npth/npth-1.5.tar.bz2"

    version('1.5', '9ba2dc4302d2f32c66737c43ed191b1b')
    version('1.4', '76cef5542e0db6a339cf960641ed86f8')
