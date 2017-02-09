##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import re

from spack.architecture import OperatingSystem
from spack.util.executable import *
import spack.spec
import spack.version
from spack.util.multiproc import parmap
import spack.compilers


class Cnl(OperatingSystem):
    """ Compute Node Linux (CNL) is the operating system used for the Cray XC
    series super computers. It is a very stripped down version of GNU/Linux.
    Any compilers found through this operating system will be used with
    modules. If updated, user must make sure that version and name are
    updated to indicate that OS has been upgraded (or downgraded)
    """

    def detect_crayos_version(self):
        modulecmd = which("modulecmd")
        modulecmd.add_default_arg("python")
        output = modulecmd("avail", "PrgEnv-intel", output=str, error=str)
        matches = re.findall(r'PrgEnv-intel/(\d+).\d+.\d+', output)
        version_set = set(matches) # 
        recent_version = max(version_set)
        return spack.version.Version(recent_version)

    def __init__(self):
        name = 'cnl'
        version = self.detect_crayos_version()
        super(Cnl, self).__init__(name, version)

    def __str__(self):
        return self.name + str(self.version)

    def find_compilers(self, *paths):
        types = spack.compilers.all_compiler_types()
        compiler_lists = parmap(
            lambda cmp_cls: self.find_compiler(cmp_cls, *paths), types)

        # ensure all the version calls we made are cached in the parent
        # process, as well.  This speeds up Spack a lot.
        clist = reduce(lambda x, y: x + y, compiler_lists)
        return clist

    def find_compiler(self, cmp_cls, *paths):
        compilers = []
        if cmp_cls.PrgEnv:
            if not cmp_cls.PrgEnv_compiler:
                tty.die('Must supply PrgEnv_compiler with PrgEnv')

            modulecmd = which('modulecmd')
            modulecmd.add_default_arg('python')

            output = modulecmd(
                'avail', cmp_cls.PrgEnv_compiler, output=str, error=str)
            version_regex = r'(%s)/([\d\.]+[\d])' % cmp_cls.PrgEnv_compiler
            matches = re.findall(version_regex, output)
            for name, version in matches:
                v = version
                comp = cmp_cls(
                    spack.spec.CompilerSpec(name + '@' + v),
                    self, "any",
                    ['cc', 'CC', 'ftn'], [cmp_cls.PrgEnv, name + '/' + v])

                compilers.append(comp)

        return compilers
