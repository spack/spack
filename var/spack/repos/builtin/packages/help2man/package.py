# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Help2man(AutotoolsPackage):
    """help2man produces simple manual pages from the '--help' and '--version'
    output of other commands."""

    homepage = "https://www.gnu.org/software/help2man/"
    url      = "https://ftpmirror.gnu.org/help2man/help2man-1.47.4.tar.xz"

    version('1.47.4', '544aca496a7d89de3e5d99e56a2f03d3')

    depends_on('gettext', type='build')
    depends_on('perl', type='build')
