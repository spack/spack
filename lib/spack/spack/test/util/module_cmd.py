# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.util.module_cmd


@pytest.mark.not_on_windows("Module files are not supported on Windows")
def test_load_module_success(monkeypatch, working_env):
    """Test that load_module properly handles successful module loads.

    This is a very lightweight test that only confirms that successful
    loads are not flagged as failed."""

    # Mock the module function to simulate a successful module load
    def mock_module(*args, **kwargs):
        if args[0] == "show":
            return ""
        elif args[0] == "load":
            # Simulate successful module load by adding to LOADEDMODULES
            current_modules = os.environ.get("LOADEDMODULES", "")
            if current_modules:
                os.environ["LOADEDMODULES"] = f"{current_modules}:{args[1]}"
            else:
                os.environ["LOADEDMODULES"] = args[1]

    monkeypatch.setattr(spack.util.module_cmd, "module", mock_module)

    # This should succeed
    spack.util.module_cmd.load_module("test_module")
    spack.util.module_cmd.load_module("test_module_2")

    # Confirm LOADEDMODULES was modified
    assert "test_module:test_module_2" in os.environ["LOADEDMODULES"]


@pytest.mark.not_on_windows("Module files are not supported on Windows")
def test_load_module_failure(monkeypatch, working_env):
    """Test that load_module raises an exception when a module load fails."""

    # Mock the module function to simulate a failed module load
    def mock_module(*args, **kwargs):
        if args[0] == "show":
            return ""
        elif args[0] == "load":
            # Simulate module load failure by not changing LOADEDMODULES
            pass

    monkeypatch.setattr(spack.util.module_cmd, "module", mock_module)

    # This should fail with ModuleLoadError
    with pytest.raises(spack.util.module_cmd.ModuleLoadError):
        spack.util.module_cmd.load_module("non_existent_module")
