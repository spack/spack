# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.util.module_cmd


@pytest.mark.not_on_windows("Module files are not supported on Windows")
def test_load_module_success(monkeypatch, working_env):
    """Test that load_module properly handles successful module loads."""

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

    # Test loading a module
    test_module = "test_module"

    # Clear LOADEDMODULES before testing
    if "LOADEDMODULES" in os.environ:
        del os.environ["LOADEDMODULES"]

    # This should succeed
    spack.util.module_cmd.load_module(test_module)

    # Check that the module was added to LOADEDMODULES
    assert test_module in os.environ.get("LOADEDMODULES", "").split(":")


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

    # Test loading a module that will fail
    test_module = "non_existent_module"

    # Clear LOADEDMODULES before testing
    if "LOADEDMODULES" in os.environ:
        del os.environ["LOADEDMODULES"]

    # This should fail with ModuleLoadError
    with pytest.raises(spack.util.module_cmd.ModuleLoadError):
        spack.util.module_cmd.load_module(test_module)