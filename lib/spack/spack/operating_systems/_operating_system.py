# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.lang

import spack.util.spack_yaml as syaml


@llnl.util.lang.lazy_lexicographic_ordering
class OperatingSystem(object):
    """Base class for all the Operating Systems.

     Each Operating System contain its own compiler finding logic, that is used
     to detect compilers.
    """

    def __init__(self, name, version):
        self.name = name.replace('-', '_')
        self.version = str(version).replace('-', '_')

    def __str__(self):
        return "%s%s" % (self.name, self.version)

    def __repr__(self):
        return self.__str__()

    def _cmp_iter(self):
        yield self.name
        yield self.version

    def to_dict(self):
        return syaml.syaml_dict([
            ('name', self.name),
            ('version', self.version)
        ])
