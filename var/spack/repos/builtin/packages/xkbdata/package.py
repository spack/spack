# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xkbdata(AutotoolsPackage):
    """The XKB data files for the various keyboard models, layouts,
    and locales."""

    homepage = "https://www.x.org/wiki/XKB/"
    url      = "https://www.x.org/archive/individual/data/xkbdata-1.0.1.tar.gz"

    version('1.0.1', 'a7e0fbc9cc84c621243c777694388064')

    depends_on('xkbcomp', type='build')
