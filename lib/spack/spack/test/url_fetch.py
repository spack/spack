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
import pytest

from llnl.util.filesystem import working_dir, is_exe

import spack.repo
import spack.config
from spack.fetch_strategy import from_list_url, URLFetchStrategy
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
        mutable_mock_packages
):
    """Fetch an archive and make sure we can checksum it."""
    mock_archive.url
    mock_archive.path

    algo = crypto.hash_fun_for_algo(checksum_type)()
    with open(mock_archive.archive_file, 'rb') as f:
        algo.update(f.read())
    checksum = algo.hexdigest()

    # Get a spec and tweak the test package with new chcecksum params
    spec = Spec('url-test')
    spec.concretize()

    pkg = spack.repo.get('url-test')
    pkg.url = mock_archive.url
    pkg.versions[ver('test')] = {checksum_type: checksum, 'url': pkg.url}
    pkg.spec = spec

    # Enter the stage directory and check some properties
    with pkg.stage:
        with spack.config.override('config:verify_ssl', secure):
            pkg.do_stage()

        with working_dir(pkg.stage.source_path):
            assert os.path.exists('configure')
            assert is_exe('configure')

            with open('configure') as f:
                contents = f.read()
            assert contents.startswith('#!/bin/sh')
            assert 'echo Building...' in contents


def test_from_list_url(mock_packages, config):
    pkg = spack.repo.get('url-list-test')

    # These URLs are all in the url-list-test package and should have
    # checksums taken from the package.
    spec = Spec('url-list-test @0.0.0').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-0.0.0.tar.gz'
    assert fetch_strategy.digest == 'abc000'

    spec = Spec('url-list-test @1.0.0').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-1.0.0.tar.gz'
    assert fetch_strategy.digest == 'abc100'

    spec = Spec('url-list-test @3.0').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-3.0.tar.gz'
    assert fetch_strategy.digest == 'abc30'

    spec = Spec('url-list-test @4.5').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-4.5.tar.gz'
    assert fetch_strategy.digest == 'abc45'

    spec = Spec('url-list-test @2.0.0b2').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-2.0.0b2.tar.gz'
    assert fetch_strategy.digest == 'abc200b2'

    spec = Spec('url-list-test @3.0a1').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-3.0a1.tar.gz'
    assert fetch_strategy.digest == 'abc30a1'

    spec = Spec('url-list-test @4.5-rc5').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-4.5-rc5.tar.gz'
    assert fetch_strategy.digest == 'abc45rc5'

    # this one is not in the url-list-test package.
    spec = Spec('url-list-test @2.0.0').concretized()
    pkg = spack.repo.get(spec)
    fetch_strategy = from_list_url(pkg)
    assert isinstance(fetch_strategy, URLFetchStrategy)
    assert os.path.basename(fetch_strategy.url) == 'foo-2.0.0.tar.gz'
    assert fetch_strategy.digest is None


def test_hash_detection(checksum_type):
    algo = crypto.hash_fun_for_algo(checksum_type)()
    h = 'f' * (algo.digest_size * 2)  # hex -> bytes
    checker = crypto.Checker(h)
    assert checker.hash_name == checksum_type


def test_unknown_hash(checksum_type):
    with pytest.raises(ValueError):
        crypto.Checker('a')
