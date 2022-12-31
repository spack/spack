# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Spack-specific environment metadata Utilities."""
import os
import pickle
import platform
import re
import shlex
import socket

from llnl.util.path import system_path_filter

import spack.platforms
import spack.spec

bash_function_finder = re.compile(r"BASH_FUNC_(.*?)\(\)")


def env_var_to_source_line(var, val):
    if var.startswith("BASH_FUNC"):
        source_line = "function {fname}{decl}; export -f {fname}".format(
            fname=bash_function_finder.sub(r"\1", var), decl=val
        )
    else:
        source_line = "{var}={val}; export {var}".format(var=var, val=shlex.quote(val))
    return source_line


@system_path_filter(arg_slice=slice(1))
def dump_environment(path, environment=None):
    """Dump an environment dictionary to a source-able file."""
    use_env = environment or os.environ
    hidden_vars = set(["PS1", "PWD", "OLDPWD", "TERM_SESSION_ID"])

    fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o600)
    with os.fdopen(fd, "w") as env_file:
        for var, val in sorted(use_env.items()):
            env_file.write(
                "".join(
                    ["#" if var in hidden_vars else "", env_var_to_source_line(var, val), "\n"]
                )
            )


@system_path_filter(arg_slice=slice(1))
def pickle_environment(path, environment=None):
    """Pickle an environment dictionary to a file."""
    pickle.dump(dict(environment if environment else os.environ), open(path, "wb"), protocol=2)


def get_host_environment_metadata():
    """Get the host environment, reduce to a subset that we can store in
    the install directory, and add the spack version.
    """
    import spack.main

    environ = get_host_environment()
    return {
        "host_os": environ["os"],
        "platform": environ["platform"],
        "host_target": environ["target"],
        "hostname": environ["hostname"],
        "spack_version": spack.main.get_version(),
        "kernel_version": platform.version(),
    }


def get_host_environment():
    """Return a dictionary (lookup) with host information (not including the
    os.environ).
    """
    host_platform = spack.platforms.host()
    host_target = host_platform.target("default_target")
    host_os = host_platform.operating_system("default_os")
    arch_fmt = "platform={0} os={1} target={2}"
    arch_spec = spack.spec.Spec(arch_fmt.format(host_platform, host_os, host_target))
    return {
        "target": str(host_target),
        "os": str(host_os),
        "platform": str(host_platform),
        "arch": arch_spec,
        "architecture": arch_spec,
        "arch_str": str(arch_spec),
        "hostname": socket.gethostname(),
    }
