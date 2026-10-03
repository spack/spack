# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.modules.common
import spack.modules.error

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_missing_module_root_raises_clear_error(mutable_empty_config):
    """Module generation requires an explicitly configured installation root."""
    with pytest.raises(spack.modules.error.ModulesError, match="No root configured"):
        spack.modules.common.root_path("tcl", "default")


def test_configured_module_root_is_used(mutable_config, tmp_path):
    """An explicitly configured module root is canonicalized and returned."""
    root = tmp_path / "modules"
    mutable_config.set("modules:default:roots", {"tcl": str(root)})
    assert spack.modules.common.root_path("tcl", "default") == str(root)
