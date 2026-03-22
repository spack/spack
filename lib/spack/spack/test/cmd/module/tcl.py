# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.main
import spack.modules.tcl

install = spack.main.SpackCommand("install")
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


def test_refresh_fold_variants(install_mockery, module_configuration, modulefile_filenames):
    """Test same module version is folded into one module file after refresh."""
    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"
    install("--fake", "--add", spec_a)
    install("--fake", "--add", spec_b)

    module_configuration("variants_all")
    module_file_a = modulefile_filenames("tcl", spec_a)[0]
    module_file_b = modulefile_filenames("tcl", spec_b)[0]
    assert module_file_a != module_file_b

    module_configuration("fold_variants_all")
    module("tcl", "refresh", "-y", "--delete-tree")
    module_file_a = module("tcl", "find", "--full-path", spec_a)
    module_file_b = module("tcl", "find", "--full-path", spec_b)
    assert module_file_a == module_file_b


def test_rm_fold_variants(install_mockery, module_configuration, modulefile_filenames):
    """Test rm command over a module file holding multiple installations."""
    module_configuration("fold_variants_all")

    spec_a = "mpileaks@2.3 ~debug ^zmpi"
    spec_b = "mpileaks@2.3 +debug ^zmpi"

    # remove module file holding one installation
    install("--fake", "--add", spec_a)
    module_file_a = modulefile_filenames("tcl", spec_a)[0]
    module("tcl", "rm", "-y", spec_a)
    assert not os.path.exists(module_file_a)

    # remove module file holding multiple installations
    module("tcl", "refresh", "-y", "--delete-tree")
    install("--fake", "--add", spec_b)
    modulefile_filenames("tcl", spec_b)[0]
    module("tcl", "rm", "-y", spec_b)
    assert not os.path.exists(module_file_a)
