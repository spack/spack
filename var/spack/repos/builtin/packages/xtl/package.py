# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version('0.6.4', sha256='5db5087c37daab3e1d35337782f79972aaaf19218a0de786a0515f247244e390')
    version('0.4.0', '48c76b63ab12e497a53fb147c41ae747')
    version('0.3.4', 'b76548a55f1e171a9c849e5ed543e8b3')
    version('0.3.3', '09b6d9611e460d9280bf1156bcca20f5')

    # C++14 support
    conflicts('%gcc@:4.8')
    conflicts('%clang@:3.6')
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')
