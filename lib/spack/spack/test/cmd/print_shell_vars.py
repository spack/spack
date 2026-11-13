# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import print_setup_info


@pytest.fixture
def module_roots(mutable_config):
    """Configure explicit roots for the shell setup output."""
    mutable_config.set(
        "modules:default:roots", {"tcl": "$data_home/modules", "lmod": "$data_home/lmod"}
    )


def test_print_shell_vars_sh(capfd, module_roots):
    print_setup_info("sh")
    out, _ = capfd.readouterr()

    assert "_sp_sys_type=" in out
    assert "_sp_tcl_roots=" in out
    assert "_sp_lmod_roots=" in out
    assert "_sp_module_prefix" not in out


def test_print_shell_vars_csh(capfd, module_roots):
    print_setup_info("csh")
    out, _ = capfd.readouterr()

    assert "set _sp_sys_type = " in out
    assert "set _sp_tcl_roots = " in out
    assert "set _sp_lmod_roots = " in out
    assert "set _sp_module_prefix = " not in out
