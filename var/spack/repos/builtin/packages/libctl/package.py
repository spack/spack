# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libctl(AutotoolsPackage):
    """libctl is a free Guile-based library implementing flexible
    control files for scientific simulations."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/Libctl"
    url      = "http://ab-initio.mit.edu/libctl/libctl-3.2.2.tar.gz"
    list_url = "http://ab-initio.mit.edu/libctl/old"

    version('3.2.2', '5fd7634dc9ae8e7fa70a68473b9cbb68')

    depends_on('guile')

    def configure_args(self):
        spec = self.spec

        return [
            '--enable-shared',
            'GUILE={0}'.format(join_path(
                spec['guile'].prefix.bin, 'guile')),
            'GUILE_CONFIG={0}'.format(join_path(
                spec['guile'].prefix.bin, 'guile-config')),
        ]
