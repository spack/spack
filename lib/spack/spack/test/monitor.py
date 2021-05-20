# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.config
import spack.spec
from spack.main import SpackCommand
import pytest
import os

install = SpackCommand('install')


@pytest.fixture(scope='session')
def test_install_monitor_save_local(install_mockery_mutable_config,
                                    mock_fetch, tmpdir_factory):
    """
    Mock installing and saving monitor results to file.
    """
    reports_dir = tmpdir_factory.mktemp('reports')
    spack.config.set('config:monitor_dir', str(reports_dir))
    out = install('--monitor', '--monitor-save-local', 'dttop')
    assert "Successfully installed dttop" in out

    # The reports directory should not be empty (timestamped folders)
    assert os.listdir(str(reports_dir))

    # Get the spec name
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    full_hash = spec.full_hash()

    # Ensure we have monitor results saved
    for dirname in os.listdir(str(reports_dir)):
        dated_dir = os.path.join(str(reports_dir), dirname)
        build_metadata = "build-metadata-%s.json" % full_hash
        assert build_metadata in os.listdir(dated_dir)
        spec_file = "spec-dttop-%s-config.json" % spec.version
        assert spec_file in os.listdir(dated_dir)

    spack.config.set('config:monitor_dir', "~/.spack/reports/monitor")
