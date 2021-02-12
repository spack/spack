# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSvg(PerlPackage):
    """Perl extension for generating Scalable Vector Graphics (SVG) documents.
    """

    homepage = "http://search.cpan.org/~manwar/SVG-2.78/lib/SVG.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MA/MANWAR/SVG-2.78.tar.gz"

    version('2.85', sha256='159ec81f3236175957c9a4e911cb0e3715dc5b658144c8a5418b772768a1477c')
    version('2.84', sha256='ec3d6ddde7a46fa507eaa616b94d217296fdc0d8fbf88741367a9821206f28af')
    version('2.83', sha256='7bb91e145563fa125c795e30b3cb79129df203536283f9beaba6928a796b0a22')
    version('2.82', sha256='72d9fc7526aa0321267a99e9ba1980a3a4afb83eb4a766cd445017b77d26159a')
    version('2.81', sha256='13b2f99015e44726e8eb8831d26c57e539ccb36082f1ed7dfb1075feed51e47a')
    version('2.80', sha256='7ec19e9c3b9b54d04cf72805c98ab82cd3b2f880aa0d75a29e3af3452bb5e4e1')
    version('2.79', sha256='daf9853154a66654984e7616a0d225f5868d9d15da28d86e4227872aaa64291b')
    version('2.78', sha256='a665c1f18c0529f3da0f4b631976eb47e0f71f6d6784ef3f44d32fd76643d6bb')
