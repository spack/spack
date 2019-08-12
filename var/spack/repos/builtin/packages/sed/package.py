# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sed(AutotoolsPackage):
    """GNU implementation of the famous stream editor."""
    homepage = "http://www.gnu.org/software/sed/"
    url      = "https://ftpmirror.gnu.org/sed/sed-4.2.2.tar.bz2"

    version('4.2.2', '7ffe1c7cdc3233e1e0c4b502df253974')
