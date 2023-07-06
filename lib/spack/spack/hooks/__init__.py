# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This package contains modules with hooks for various stages in the
Spack install process.  You can add modules here and they'll be
executed by package at various times during the package lifecycle.

Each hook is just a function that takes a package as a parameter.
Hooks are not executed in any particular order.

Currently the following hooks are supported:

    * pre_install(spec)
    * post_install(spec, explicit)
    * pre_uninstall(spec)
    * post_uninstall(spec)
    * on_install_start(spec)
    * on_install_success(spec)
    * on_install_failure(spec)
    * on_phase_success(pkg, phase_name, log_file)
    * on_phase_error(pkg, phase_name, log_file)
    * on_phase_error(pkg, phase_name, log_file)
    * post_env_write(env)

This can be used to implement support for things like module
systems (e.g. modules, lmod, etc.) or to add other custom
features.
"""

from llnl.util.lang import ensure_last, list_modules

import spack.paths


class _HookRunner:
    #: Stores all hooks on first call, shared among
    #: all HookRunner objects
    _hooks = None

    def __init__(self, hook_name):
        self.hook_name = hook_name

    @classmethod
    def _populate_hooks(cls):
        # Lazily populate the list of hooks
        cls._hooks = []

        relative_names = list(list_modules(spack.paths.hooks_path))

        # Ensure that write_install_manifest comes last
        ensure_last(relative_names, "absolutify_elf_sonames", "write_install_manifest")

        for name in relative_names:
            module_name = __name__ + "." + name
            # When importing a module from a package, __import__('A.B', ...)
            # returns package A when 'fromlist' is empty. If fromlist is not
            # empty it returns the submodule B instead
            # See: https://stackoverflow.com/a/2725668/771663
            module_obj = __import__(module_name, fromlist=[None])
            cls._hooks.append((module_name, module_obj))

    @property
    def hooks(self):
        if not self._hooks:
            self._populate_hooks()
        return self._hooks

    def __call__(self, *args, **kwargs):
        for _, module in self.hooks:
            if hasattr(module, self.hook_name):
                hook = getattr(module, self.hook_name)
                if hasattr(hook, "__call__"):
                    hook(*args, **kwargs)


# pre/post install and run by the install subprocess
pre_install = _HookRunner("pre_install")
post_install = _HookRunner("post_install")

# These hooks are run within an install subprocess
pre_uninstall = _HookRunner("pre_uninstall")
post_uninstall = _HookRunner("post_uninstall")
on_phase_success = _HookRunner("on_phase_success")
on_phase_error = _HookRunner("on_phase_error")

# These are hooks in installer.py, before starting install subprocess
on_install_start = _HookRunner("on_install_start")
on_install_success = _HookRunner("on_install_success")
on_install_failure = _HookRunner("on_install_failure")
on_install_cancel = _HookRunner("on_install_cancel")

# Environment hooks
post_env_write = _HookRunner("post_env_write")
