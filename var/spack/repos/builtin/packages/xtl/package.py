# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xtl(CMakePackage):
    """QuantStack tools library"""

    homepage = "https://github.com/QuantStack/xtl"
    url      = "https://github.com/QuantStack/xtl/archive/0.3.4.tar.gz"
    git      = "https://github.com/QuantStack/xtl.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('0.6.9', sha256='c348fcf53dd2b355d143ad28e77f1ede7e1d5e6a196d2d5b9c478b1c005dedd0')
    version('0.4.0', '48c76b63ab12e497a53fb147c41ae747')
    version('0.3.4', 'b76548a55f1e171a9c849e5ed543e8b3')
    version('0.3.3', '09b6d9611e460d9280bf1156bcca20f5')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')
