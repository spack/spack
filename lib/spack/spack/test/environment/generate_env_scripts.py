# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for environment script generation."""

import os
import sys

import pytest

import spack.environment as ev
import spack.environment.generate_env_scripts as env_script
from spack.main import SpackCommand

pytestmark = [pytest.mark.usefixtures("mutable_mock_env_path")]

env = SpackCommand("env")


def test_paths_to_env_scripts(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that activate & deactivate shell scripts are written to the right location."""
    env("create", "test_path_scripts")
    test_env = ev.read("test_path_scripts")

    shells_avail = ["sh"]  # csh and fish have the same scripts as sh

    if sys.platform == "win32":
        shells_avail = ["bat", "pwsh"]

    for shell in shells_avail:
        activate_extension = ""
        if shell == "bat":
            activate_extension = ".bat"
        elif shell == "pwsh":
            activate_extension = ".ps1"

        deactivate_extension = ".ps1" if shell == "pwsh" else f".{shell}"

        expected_activate_path = os.path.join(
            test_env.path, ".spack-env", f"default_activate{activate_extension}"
        )
        actual_activate_path = env_script.path_to_env_script(
            test_env, shell, script_type="activate", view="default"
        )
        assert actual_activate_path == expected_activate_path

        expected_deactivate_path = os.path.join(
            test_env.path, ".spack-env", f"default_deactivate{deactivate_extension}"
        )
        actual_deactivate_path = env_script.path_to_env_script(
            test_env, shell, script_type="deactivate", view="default"
        )
        assert actual_deactivate_path == expected_deactivate_path


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_write_env_activate_script(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that write_env_activate_script creates a script."""
    env_name = f"test_write_activate_{shell}"
    env("create", env_name)
    test_env = ev.read(env_name)

    env_script.write_env_activate_script(test_env)

    script_path = env_script.path_to_env_script(
        test_env, shell, script_type="activate", view="default"
    )

    test_env_path = test_env.path
    cmd_name = "_spack_env_set"
    if shell == "bat":
        test_env_path = f'"{test_env_path}"'
        cmd_name = f"%{cmd_name}%"
    assert os.path.exists(script_path)

    # Verify content
    with open(script_path, "r", encoding="utf-8") as f:
        activation_content = f.read()
    print(activation_content)
    assert len(activation_content) > 0
    assert f"{cmd_name} SPACK_ENV {test_env_path}" in activation_content


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_write_env_deactivate_script(
    shell, mutable_mock_env_path, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Test that write_env_deactivate_script creates a script."""
    env_name = f"test_write_deactivate_{shell}"
    env("create", env_name)
    test_env = ev.read(env_name)

    env_script.write_env_deactivate_script(test_env, view="default")

    script_path = env_script.path_to_env_script(
        test_env, shell, script_type="deactivate", view="default"
    )

    # batch "commands" are actually variables
    cmd_name = "_spack_env_unset"
    if shell == "bat":
        cmd_name = f"%{cmd_name}%"

    assert os.path.exists(script_path)

    # Verify content
    with open(script_path, "r", encoding="utf-8") as f:
        deactivation_content = f.read()

    assert len(deactivation_content) > 0
    assert f"{cmd_name} SPACK_ENV" in deactivation_content


@pytest.mark.parametrize(
    "shell", (["bat", "pwsh"] if sys.platform == "win32" else ["sh", "csh", "fish"])
)
def test_create_individual_env_scripts(
    shell, install_mockery, mock_fetch, mock_archive, mock_packages
):
    """Ensure that each environment's activation/deactivation scripts contain only
    their own environment modifications and aren't mixed when multiple environments
    are created individually."""
    env_name_1 = f"test_env_1_{shell}"
    env_name_2 = f"test_env_2_{shell}"

    # Create environments individually
    env("create", env_name_1)
    env("create", env_name_2)

    env_1 = ev.read(env_name_1)
    env_2 = ev.read(env_name_2)

    # Generate scripts by writing them directly (can't activate both at once)
    env_script.write_env_activate_script(env_1)
    env_script.write_env_deactivate_script(env_1, view="default")
    env_script.write_env_activate_script(env_2)
    env_script.write_env_deactivate_script(env_2, view="default")

    # Check that each activation script only references its own environment
    activate_path_1 = env_script.path_to_env_script(
        env_1, shell, script_type="activate", view="default"
    )
    activate_path_2 = env_script.path_to_env_script(
        env_2, shell, script_type="activate", view="default"
    )

    # batch "commands" are actually variables wrapping a
    # 'call' operation, which in turn invokes another batch script
    # containing the goto which implements the "command" functionality
    # as such they need to be dereferenced
    env1_path = env_1.path
    env2_path = env_2.path
    set_cmd_name = "_spack_env_set"
    unset_cmd_name = "_spack_env_unset"
    if shell == "bat":
        env1_path = f'"{env1_path}"'
        env2_path = f'"{env2_path}"'
        set_cmd_name = f"%{set_cmd_name}%"
        unset_cmd_name = f"%{unset_cmd_name}%"

    with open(activate_path_1, "r", encoding="utf-8") as f:
        activate_content_1 = f.read()
    with open(activate_path_2, "r", encoding="utf-8") as f:
        activate_content_2 = f.read()

    # Each script should reference its own environment path
    assert f"{set_cmd_name} SPACK_ENV {env1_path}" in activate_content_1
    assert f"{set_cmd_name} SPACK_ENV {env2_path}" in activate_content_2

    # But not the other environment's path
    assert env_2.path not in activate_content_1
    assert env_1.path not in activate_content_2

    # Check that each deactivation script only references its own environment
    deactivate_path_1 = env_script.path_to_env_script(
        env_1, shell, script_type="deactivate", view="default"
    )
    deactivate_path_2 = env_script.path_to_env_script(
        env_2, shell, script_type="deactivate", view="default"
    )

    with open(deactivate_path_1, "r", encoding="utf-8") as f:
        deactivate_content_1 = f.read()
    with open(deactivate_path_2, "r", encoding="utf-8") as f:
        deactivate_content_2 = f.read()

    # Both should have the deactivation command
    assert f"{unset_cmd_name} SPACK_ENV" in deactivate_content_1
    assert f"{unset_cmd_name} SPACK_ENV" in deactivate_content_2

    # Environment names shouldn't appear in the other's scripts
    assert env_name_2 not in activate_content_1
    assert env_name_1 not in activate_content_2
    assert env_name_2 not in deactivate_content_1
    assert env_name_1 not in deactivate_content_2
