##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import pytest

from llnl.util.filesystem import *

import spack
from spack.spec import Spec
from spack.version import ver
import spack.util.crypto as crypto


@pytest.fixture(params=list(crypto.hashes.keys()))
def checksum_type(request):
    return request.param


@pytest.mark.parametrize('secure', [True, False])
def test_fetch(
        mock_archive,
        secure,
        checksum_type,
        config,
        refresh_builtin_mock
):
    """Fetch an archive and make sure we can checksum it."""
    mock_archive.url
    mock_archive.path

    algo = crypto.hashes[checksum_type]()
    with open(mock_archive.archive_file, 'rb') as f:
        algo.update(f.read())
    checksum = algo.hexdigest()

    # Get a spec and tweak the test package with new chcecksum params
    spec = Spec('url-test')
    spec.concretize()

    pkg = spack.repo.get('url-test', new=True)
    pkg.url = mock_archive.url
    pkg.versions[ver('test')] = {checksum_type: checksum, 'url': pkg.url}
    pkg.spec = spec

    # Enter the stage directory and check some properties
    with pkg.stage:
        try:
            spack.insecure = secure
            pkg.do_stage()
        finally:
            spack.insecure = False

        assert os.path.exists('configure')
        assert is_exe('configure')

        with open('configure') as f:
            contents = f.read()
        assert contents.startswith('#!/bin/sh')
        assert 'echo Building...' in contents


class MockFilesystem(object):
    def __init__(self, exists=None, files=None):
        self.removed = set()
        self.symlinked = set()
        self.copied = set()
        self.files = set(files or set())
        self.exists = set(exists or set()) | self.files

    def remove(self, path):
        self.removed.add(path)
        self.exists.remove(path)

    def symlink(self, src, dst):
        self.symlinked.add((src, dst))
        self.exists.add(dst)

    def copy(self, src, dst):
        self.copied.add((src, dst))
        self.exists.add(dst)

    def file_exists(self, path):
        return path in self.exists

    def is_file(self, path):
        return path in self.files


class MockStage(object):
    def __init__(self, save_filename):
        self._save_filename = save_filename

    def chdir(self):
        pass

    @property
    def save_filename(self):
        return self._save_filename


def test_no_symlink_noexpand_cached(tmpdir):
    test_path = 'made-up-path'
    dst_path = 'dst-path'
    mock_fs = MockFilesystem(files=[test_path])
    cache_fetcher = spack.fetch_strategy.CacheURLFetchStrategy(
        url=test_path, filesystem=mock_fs, expand=False)
    cache_fetcher.set_stage(MockStage(dst_path))
    cache_fetcher.fetch()
    assert not mock_fs.symlinked
    assert (test_path, dst_path) in mock_fs.copied


def test_hash_detection(checksum_type):
    algo = crypto.hashes[checksum_type]()
    h = 'f' * (algo.digest_size * 2)  # hex -> bytes
    checker = crypto.Checker(h)
    assert checker.hash_name == checksum_type


def test_unknown_hash(checksum_type):
    with pytest.raises(ValueError):
        crypto.Checker('a')
