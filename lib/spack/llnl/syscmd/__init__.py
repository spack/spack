# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Provides classes and functions to manipulate environment modifications, and to
call arbitrary commands in a subprocess, within a controlled environment.
"""
from .environment import (
    SYSTEM_DIRS,
    TRACING_ENABLED,
    AppendPath,
    EnvironmentModifications,
    PrependPath,
    RemovePath,
    SetEnv,
    UnsetEnv,
    dump_environment,
    env_flag,
    filter_system_paths,
    get_path,
    inspect_path,
    is_system_path,
    path_put_first,
    pickle_environment,
    preserve_environment,
    sanitize,
    set_env,
    validate,
)
from .executable import CommandNotFoundError, Executable, ProcessError, which, which_string
from .sourcing import environment_after_sourcing_files, from_sourcing_file

__all__ = [
    "EnvironmentModifications",
    "SetEnv",
    "dump_environment",
    "preserve_environment",
    "sanitize",
    "UnsetEnv",
    "AppendPath",
    "PrependPath",
    "RemovePath",
    "pickle_environment",
    "inspect_path",
    "filter_system_paths",
    "is_system_path",
    "env_flag",
    "get_path",
    "validate",
    "path_put_first",
    "set_env",
    "SYSTEM_DIRS",
    "TRACING_ENABLED",
    "which",
    "ProcessError",
    "Executable",
    "which_string",
    "CommandNotFoundError",
    "from_sourcing_file",
    "environment_after_sourcing_files",
]
