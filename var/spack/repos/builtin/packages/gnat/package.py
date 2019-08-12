# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gnat(MakefilePackage):
    """The GNAT Ada compiler. Ada is a modern programming language designed
    for large, long-lived applications - and embedded systems in particular
    - where reliability and efficiency are essential."""

    homepage = "https://libre.adacore.com/tools/gnat-gpl-edition/"

    # NOTE: This is a binary installer intended to bootstrap GCC's Ada compiler

    # There may actually be a way to install GNAT from source. If you go to
    # the GNAT Download page: https://libre.adacore.com/download/
    # select "Free Software or Academic Development", select your platform,
    # expand GNAT Ada, and expand Sources, you'll see links to download the
    # source code for GNAT and all of its dependencies. Most of these
    # dependencies are already in Spack.

    # This is the GPL release for Linux x86-64
    version('2016', '9741107cca1a6a4ddb0d5e8de824a90c', extension='tar.gz',
            url="http://mirrors.cdn.adacore.com/art/5739cefdc7a447658e0b016b")

    phases = ['install']

    def install(self, spec, prefix):
        make('ins-all', 'prefix={0}'.format(prefix))
