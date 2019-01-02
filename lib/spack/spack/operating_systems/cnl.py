# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import llnl.util.tty as tty
import llnl.util.multiproc as mp

from spack.architecture import OperatingSystem
from spack.util.module_cmd import get_module_cmd


class Cnl(OperatingSystem):
    """ Compute Node Linux (CNL) is the operating system used for the Cray XC
    series super computers. It is a very stripped down version of GNU/Linux.
    Any compilers found through this operating system will be used with
    modules. If updated, user must make sure that version and name are
    updated to indicate that OS has been upgraded (or downgraded)
    """

    def __init__(self):
        name = 'cnl'
        version = self._detect_crayos_version()
        super(Cnl, self).__init__(name, version)

    def __str__(self):
        return self.name + str(self.version)

    def _detect_crayos_version(self):
        modulecmd = get_module_cmd()
        output = modulecmd("avail", "PrgEnv-", output=str, error=str)
        matches = re.findall(r'PrgEnv-\w+/(\d+).\d+.\d+', output)
        major_versions = set(matches)
        latest_version = max(major_versions)
        return latest_version

    def find_compilers(self, *paths):
        # function-local so that cnl doesn't depend on spack.config
        import spack.compilers

        types = spack.compilers.all_compiler_types()
        compiler_lists = mp.parmap(
            lambda cmp_cls: self.find_compiler(cmp_cls, *paths), types)

        # ensure all the version calls we made are cached in the parent
        # process, as well.  This speeds up Spack a lot.
        clist = [comp for cl in compiler_lists for comp in cl]
        return clist

    def find_compiler(self, cmp_cls, *paths):
        # function-local so that cnl doesn't depend on spack.config
        import spack.spec

        compilers = []
        if cmp_cls.PrgEnv:
            if not cmp_cls.PrgEnv_compiler:
                tty.die('Must supply PrgEnv_compiler with PrgEnv')

            modulecmd = get_module_cmd()

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
