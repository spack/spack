# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import os
import os.path

from spack.main import SpackCommand
from spack.util.executable import which

debug = SpackCommand('debug')


@pytest.mark.db
def test_create_db_tarball(tmpdir, database):
    with tmpdir.as_cwd():
        debug('create-db-tarball')

        # get the first non-dotfile to avoid coverage files in the directory
        files = os.listdir(os.getcwd())
        tarball_name = next(f for f in files if not f.startswith('.'))

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
