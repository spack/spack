##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os
import os.path

from spack.main import SpackCommand
from spack.util.executable import which

debug = SpackCommand('debug')


def test_create_db_tarball(tmpdir, database):
    with tmpdir.as_cwd():
        debug('create-db-tarball')

        files = os.listdir(os.getcwd())
        tarball_name = files[0]

        # debug command made an archive
        assert os.path.exists(tarball_name)

        # print contents of archive
        tar = which('tar')
        contents = tar('tzf', tarball_name, output=str)

        # DB file is included
        assert 'index.json' in contents

        # spec.yamls from all installs are included
        for spec in database.query():
            # externals won't have a spec.yaml
            if spec.external:
                continue

            spec_suffix = '%s/.spack/spec.yaml' % spec.dag_hash()
            assert spec_suffix in contents
