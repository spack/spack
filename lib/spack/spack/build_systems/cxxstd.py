# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PackageBase
from spack.directives import depends_on, variant, conflicts

import spack.variant


class CxxstdPackage(PackageBase):
    """Auxiliary class which contains cxxstd variant, dependencies and conflicts
    and is meant to unify and facilitate its usage.
    """
    variant('cxxstd',
            default='default',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
 
    def cxxstd_to_flag(self):
        flag = ''
        if self.spec.variants['cxxstd'].value == '98':
            flag = self.compiler.cxx98_flag
        elif self.spec.variants['cxxstd'].value == '11':
            flag = self.compiler.cxx11_flag
        elif self.spec.variants['cxxstd'].value == '14':
            flag = self.compiler.cxx14_flag
        elif self.spec.variants['cxxstd'].value == '17':
            flag = self.compiler.cxx17_flag
        elif self.spec.variants['cxxstd'].value == 'default':
            # Let the compiler do what it usually does.
            pass
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die("INTERNAL ERROR: cannot accommodate unexpected variant ",
                    "cxxstd={0}".format(self.spec.variants['cxxstd'].value))
        return flag
