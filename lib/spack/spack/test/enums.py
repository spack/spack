# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.enums as enums


def test_context_enum():
    """Test the Context enum string representation and parsing."""
    assert str(enums.Context.BUILD) == "build"
    assert str(enums.Context.RUN) == "run"
    assert str(enums.Context.TEST) == "test"

    assert enums.Context.from_string("build") == enums.Context.BUILD
    assert enums.Context.from_string("run") == enums.Context.RUN
    assert enums.Context.from_string("test") == enums.Context.TEST

    with pytest.raises(ValueError, match="context should be one of"):
        enums.Context.from_string("invalid_context")


def test_install_record_status():
    """Test the InstallRecordStatus bitwise flags."""
    assert (enums.InstallRecordStatus.INSTALLED | enums.InstallRecordStatus.DEPRECATED | enums.InstallRecordStatus.MISSING) == enums.InstallRecordStatus.ANY
    
    # Ensure flag operations work as expected
    combined = enums.InstallRecordStatus.INSTALLED | enums.InstallRecordStatus.MISSING
    assert enums.InstallRecordStatus.INSTALLED in combined
    assert enums.InstallRecordStatus.MISSING in combined
    assert enums.InstallRecordStatus.DEPRECATED not in combined


def test_config_scope_priority():
    """Test the ordering of ConfigScopePriority."""
    assert enums.ConfigScopePriority.DEFAULTS < enums.ConfigScopePriority.CONFIG_FILES
    assert enums.ConfigScopePriority.CONFIG_FILES < enums.ConfigScopePriority.ENVIRONMENT
    assert enums.ConfigScopePriority.ENVIRONMENT < enums.ConfigScopePriority.CUSTOM
    assert enums.ConfigScopePriority.CUSTOM < enums.ConfigScopePriority.COMMAND_LINE
    assert enums.ConfigScopePriority.COMMAND_LINE < enums.ConfigScopePriority.ENVIRONMENT_SPEC_GROUPS
