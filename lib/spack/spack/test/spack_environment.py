# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test the Environment class"""
import sys

import pytest

import spack.environment as ev
import spack.spec
from spack.main import SpackCommand

env = SpackCommand("env")

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Environments are not supported on Windows yet"
)


def test_dev_rebuild_dependent_delayed(
    tmpdir, mock_packages, mutable_database, mutable_mock_env_path
):
    """Install X->Y; change Y; perform "spack install Y" (not rebuilding X);
    and then do "spack install". In this case, The final command should
    reinstall X. This makes sure we don't lose track of when dependents
    should be reinstalled.
    """

    existing_dev_path = tmpdir.ensure("dev-path", dir=True)

    env("create", "test")
    with ev.read("test") as e:
        e.add("dependent-of-dev-build")
        e.develop(spack.spec.Spec("dev-build-test-install@=0.0.0"), path=str(existing_dev_path))
        e.concretize()

        user_to_concretized = list(e.concretized_specs())
        root = user_to_concretized[0][1]
        dependent = root["dependent-of-dev-build"]
        child = root["dev-build-test-install"]

        db = spack.database.Database(tmpdir.join("db"), lock_cfg=spack.database.NO_LOCK)
        db._add(child, installation_time=2)
        db._add(dependent, installation_time=1)

        needs_reinstall = e._get_overwrite_specs(_database=db)
        assert needs_reinstall == [dependent.dag_hash()]
