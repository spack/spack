# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xmlto(AutotoolsPackage):
    """Utility xmlto is a simple shell script for converting XML files to various
    formats. It serves as easy to use command line frontend to make fine output
    without remembering many long options and searching for the syntax of the
    backends."""

    homepage = "https://pagure.io/xmlto"
    url      = "https://releases.pagure.org/xmlto/xmlto-0.0.28.tar.gz"

    version('0.0.28', 'a1fefad9d83499a15576768f60f847c6')

    # FIXME: missing a lot of dependencies
    depends_on('libxslt')
