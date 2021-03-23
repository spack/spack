# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MparkVariant(CMakePackage):
    """C++17 `std::variant` for C++11/14/17"""

    homepage = "https://github.com/mpark/variant"
    git     = "https://github.com/mpark/variant.git"
    maintainers = ['ax3l']

    version('1.4.0', commit='4988879a9f5a95d72308eca2b1779db6ed9b135d')
    version('1.3.0', commit='29319715a1f0eb0980d380db8a2fda5af8d58feb')

    # Ref.: https://github.com/mpark/variant/pull/73
    patch('nvcc.patch', when='@:1.4.0')
    patch('version.patch', when='@:1.4.0')

    cxx11_msg = 'MPark.Variant needs a C++11-capable compiler. ' \
                'See https://github.com/mpark/variant#requirements'
    conflicts('%gcc@:4.7', msg=cxx11_msg)
    conflicts('%clang@:3.5', msg=cxx11_msg)

    conflicts('%gcc@7.3.1',
              msg='GCC 7.3.1 has a bug that prevents using MPark.Variant. '
                  'See https://github.com/mpark/variant/issues/43 and '
                  'https://gcc.gnu.org/bugzilla/show_bug.cgi?id=84785 '
                  'Please use a different compiler version or another '
                  'compiler.')
