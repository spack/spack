# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fl(Package):
    """Fawlty Language is an IDL8
    (Interactive Data Language) compatible compiler."""

    homepage = "https://www.flxpert.hu/fl/"
    url      = "https://www.flxpert.hu/fl/fl_0.79.47-amd64-linux.tar.gz"

    version('0.79.47', sha256='b8a4a74118c1a024313bf912261fbc016a53f2d15adb1226217f2a10a9f7ca9a')

    def install(self, spec, prefix):
        if (self.spec.satisfies('platform=linux') and
           self.spec.target.family == 'x86_64'):
            with working_dir('fl_{0}'.format(spec.version)):
                install_tree('.', prefix)
        else:
            raise InstallError('fl is built for Linux x86_64 platform only.')
