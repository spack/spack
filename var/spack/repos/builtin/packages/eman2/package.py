# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eman2(Package):
    """EMAN2 is the successor to EMAN1. It is a broadly based greyscale
       scientific image processing suite with a primary focus on processing
       data from transmission electron microscopes."""

    homepage = "https://blake.bcm.edu/emanwiki/EMAN2"
    url      = "https://cryoem.bcm.edu/cryoem/static/software/release-2.3/eman2.3.linux64.sh"

    version('2.3', sha256='f3cdb956fc7b12dbdeee90c0276169d6cc55d8c75208f94e85655e5884d1e8c8',
            expand=False)

    def url_for_version(self, version):
        pfx = 'https://cryoem.bcm.edu/cryoem/static/software/'
        sfx = 'release-{0}/eman{0}.linux64.sh'.format(version.dotted)
        return '{0}{1}'.format(pfx, sfx)

    def install(self, spec, prefix):
        # interactive installer, questions:
        # 1. installation prefix

        # the installer complains if the directory already exists
        # install to a temporary prefix, and then copy the tree
        temp_prefix = join_path(self.stage.source_path, 'eman2')

        config_filename = 'spack-config.in'
        config_answers = [temp_prefix]

        with open(config_filename, 'w') as f:
            f.write('\n'.join(config_answers))

        with open(config_filename, 'r') as f:
            sh = which('sh')
            sh(self.stage.archive_file, input=f)

        # install to actual prefix
        install_tree(temp_prefix, prefix)
