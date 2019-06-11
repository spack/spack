# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import pytest

from llnl.util.filesystem import mkdirp
import spack.environment as ev
from spack.cmd.location import BadEnvironmentError, MissingBuildDirectoryError
from spack.cmd.location import SpecificationError
from spack.main import SpackCommand
import spack.paths


# everything here uses the mock_env_path
pytestmark = pytest.mark.usefixtures('config')

# location prints out "locations of packages and spack directories"
location = SpackCommand('location')

_repo_dir = os.path.join(spack.paths.repos_path, 'builtin.mock')
_pkg_dir = os.path.join(_repo_dir, 'packages')

_mock_spec_name = 'externaltest'
_test_env_name = 'test'


@pytest.fixture
def mock_test_env(mutable_mock_env_path):
    env_dir = ev.root(_test_env_name)
    mkdirp(env_dir)
    yield

    shutil.rmtree(env_dir)


@pytest.fixture
def mock_spec():
    s = spack.spec.Spec(_mock_spec_name).concretized()
    pkg = spack.repo.get(s)

    # Make it look like the source was actually expanded.
    source_path = pkg.stage.source_path
    mkdirp(source_path)
    yield

    # The test is done so be sure to remove the spec from the mock stage area.
    shutil.rmtree(pkg.stage.path)


def test_location_bad_env():
    """Tests spack location with an unknown environment."""
    with pytest.raises(BadEnvironmentError, match="No such environment"):
        location('--env', 'test-unknown-env')


@pytest.mark.parametrize('spec1,spec2,msg', [
    (None, None, "You must supply a spec"),
    ('spec1', 'spec2', "Only one spec, not 2")])
def test_location_bad_spec_options(spec1, spec2, msg):
    """Tests spack location with bad spec options."""
    args = [spec1, spec2]
    if not all(args):
        args = []

    with pytest.raises(SpecificationError, match=msg):
        location(*args)


@pytest.mark.db
@pytest.mark.usefixtures('database', 'mock_spec')
def test_location_build_dir():
    """Tests spack location --build-dir"""
    out = location('--build-dir', _mock_spec_name)
    assert _mock_spec_name in out


@pytest.mark.usefixtures('mock_test_env')
def test_location_env():
    out = location('--env', _test_env_name)
    assert 'mock-env-path' in out and out[:-1].endswith(_test_env_name)


@pytest.mark.db
@pytest.mark.parametrize('cmd,option,result,endswith', [
    ('--install-dir', 'libelf', 'libelf-', False),
    ('--module-dir', None, spack.paths.module_path, True),
    ('--package-dir', 'mpileaks', os.path.join(_pkg_dir, 'mpileaks'), True),
    ('--packages', None, _repo_dir, True),
    ('--spack-root', None, spack.paths.prefix, True),
    ('--stage-dir', 'libelf', 'libelf-', False),
    ('--stages', None, 'mock_stage', False)])
@pytest.mark.usefixtures('database')
def test_location_options(cmd, option, result, endswith):
    """Tests location command outputs that yield expected results."""
    args = [cmd]
    if option is not None:
        args.append(option)
    out = location(*args)

    if endswith:
        assert out[:-1].endswith(result)
    else:
        assert result in out


@pytest.mark.db
@pytest.mark.usefixtures('database')
def test_location_missing_build_dir():
    """Tests spack location with a missing build directory."""
    with pytest.raises(MissingBuildDirectoryError,
                       match="Build directory does not exist yet"):
        location('--build-dir', 'mpileaks')
