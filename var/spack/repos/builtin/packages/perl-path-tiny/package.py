# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPathTiny(PerlPackage):
    """This module provides a small, fast utility for working with file paths.
    It is friendlier to use than File::Spec and provides easy access to
    functions from several other core file handling modules. It aims to be
    smaller and faster than many alternatives on CPAN, while helping people do
    many common things in consistent and less error-prone ways."""

    homepage = "https://metacpan.org/pod/Path::Tiny"
    url      = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Path-Tiny-0.108.tar.gz"

    version('0.118', sha256='32138d8d0f4c9c1a84d2a8f91bc5e913d37d8a7edefbb15a10961bfed560b0fd')
    version('0.116', sha256='0379108b2aee556f877760711e03ce8775a98859cdd03cb94aaf4738a37a62d3')
    version('0.114', sha256='cd0f88f37a58fc3667ec065767fe01e73ee6efa18a112bfd3508cf6579ca00e1')
    version('0.112', sha256='813df2d140c65f795daefd8eca18e61194ecac7050c5406a069db86dea31cc3a')
    version('0.110', sha256='a849dc0777315899689d0b351e815d90eaa636a01ed1d5e6de99a368529b5cfa')
    version('0.108', sha256='3c49482be2b3eb7ddd7e73a5b90cff648393f5d5de334ff126ce7a3632723ff5')
