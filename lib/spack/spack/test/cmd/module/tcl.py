# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.main
import spack.modules.tcl

module = spack.main.SpackCommand("module")

pytestmark = pytest.mark.not_on_windows("does not run on windows")

writer_cls = spack.modules.tcl.TclModulefileWriter


@pytest.mark.db
def test_find_variants(mutable_database, module_configuration):
    """Test found module is returned with its variant specification if enabled."""
    module_configuration("variants_all")

    module("tcl", "refresh", "-y", "--delete-tree")
    out = module("tcl", "find", "mpileaks ^zmpi")
    assert " build_system=generic ~debug ~fortran ~opt +shared +static" in out


@pytest.mark.db
def test_loads_variants(mutable_database, module_configuration):
    """Test module to load is returned with its variant specification if enabled."""
    module_configuration("variants_all")

    module("tcl", "refresh", "-y", "--delete-tree")
    out = module("tcl", "loads", "mpileaks ^zmpi")
    assert " build_system=generic ~debug ~fortran ~opt +shared +static" in out
