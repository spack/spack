# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Texinfo(AutotoolsPackage):
    """Texinfo is the official documentation format of the GNU project.

    It was invented by Richard Stallman and Bob Chassell many years ago,
    loosely based on Brian Reid's Scribe and other formatting languages
    of the time. It is used by many non-GNU projects as well."""

    homepage = "https://www.gnu.org/software/texinfo/"
    url      = "https://ftpmirror.gnu.org/texinfo/texinfo-6.0.tar.gz"

    version('6.5', '94e8f7149876793030e5518dd8d6e956')
    version('6.3', '9b08daca9bf8eccae9b0f884aba41f9e')
    version('6.0', 'e1a2ef5dce5018b53f0f6eed45b247a7')
    version('5.2', '1b8f98b80a8e6c50422125e07522e8db')
    version('5.1', '54e250014fe698fb4832016158747c03')
    version('5.0', '918432285abe6fe96c98355594c5656a')

    depends_on('perl')
