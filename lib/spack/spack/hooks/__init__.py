# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
    * post_install(spec)
    * pre_uninstall(spec)
    * post_uninstall(spec)
    * on_install_start(spec)
    * on_install_success(spec)
    * on_install_failure(spec)
    * on_phase_success(pkg, phase_name, log_file)
    * on_phase_error(pkg, phase_name, log_file)
    * on_phase_error(pkg, phase_name, log_file)
    * on_analyzer_save(pkg, result)
    * post_env_write(env)

This can be used to implement support for things like module
systems (e.g. modules, lmod, etc.) or to add other custom
features.
"""
import contextlib


class HookRunner(object):
    #: Stores all hooks on first call, shared among
    #: all HookRunner objects
    _hooks = None

    def __init__(self, hooks=None):
        self.hooks_names = hooks or []

    def _init_hooks(cls):
        # Lazily populate the list of hooks
        cls._hooks = []

        for name in cls.hooks_names:
            module_name = __name__ + '.' + name
            # When importing a module from a package, __import__('A.B', ...)
            # returns package A when 'fromlist' is empty. If fromlist is not
            # empty it returns the submodule B instead
            # See: https://stackoverflow.com/a/2725668/771663
            cls._hooks.append(__import__(module_name, fromlist=[None]))

    @property
    def hooks(self):
        if not self._hooks:
            self._init_hooks()
        return self._hooks

    def __call__(self, hook_name, *args, **kwargs):
        for module in self.hooks:
            if hasattr(module, hook_name):
                hook = getattr(module, hook_name)
                if hasattr(hook, '__call__'):
                    hook(*args, **kwargs)


_default_runner = HookRunner([
    'extensions',
    'licensing',
    'module_file_generation',
    'permissions_setters',
    'monitor',
    'sbang',
    'write_install_manifest'
])


runner = _default_runner


@contextlib.contextmanager
def use_hook_runner(new_runner):
    global runner
    old_runner, runner = runner, new_runner
    try:
        yield
    finally:
        runner = old_runner
