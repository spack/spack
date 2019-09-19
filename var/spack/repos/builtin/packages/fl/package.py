# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fl(Package):
    """Fawlty Language is an IDL8 (Interactive Data Language) compatible compiler."""

    homepage = "https://www.flxpert.hu/fl/"
    url      = "https://www.flxpert.hu/fl/fl_0.79.47-amd64-linux.tar.gz"

    version('0.79.47', sha256='b8a4a74118c1a024313bf912261fbc016a53f2d15adb1226217f2a10a9f7ca9a')

    # TODO: Add runtime dependency since Fawlty is binary distributed.

    def install(self, spec, prefix):
        with working_dir('fl_{0}'.format(spec.version)):
            if 'x86_64' in spack.architecture.sys_type():
                install_tree('.', prefix)
            else:
                raise InstallError('Cannot install Fawlty on {0} architecture.'
                                   .format(spack.architecture.sys_type()))
