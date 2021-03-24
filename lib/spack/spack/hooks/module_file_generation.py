# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.config
import spack.environment as ev
import spack.modules
import spack.modules.common
import llnl.util.tty as tty


def _for_each_enabled(spec, method_name):
    """Calls a method for each enabled module"""
    enabled = spack.config.get('modules:enable')
    if not enabled:
        tty.debug('NO MODULE WRITTEN: list of enabled module files is empty')
        return

    # We do this once automatically, and an extra time for the environment
    # If no environment, the set has a single element
    # If the element is not None, it is an Environment
    for env in set([None, ev.get_env({}, '')]):
        if env:
            # If the environment defines module roots, use those
            # Otherwise, add the default module roots
            module_roots = env.module_path_defaults
            full_roots = spack.config.get('config:module_roots')
            no_env_roots = spack.config.no_env_config().get(
                'config:module_roots')
            for mtype, path in module_roots.items():
                if full_roots[mtype] != no_env_roots[mtype]:
                    module_roots[mtype] = full_roots[mtype]
        else:
            module_roots = spack.config.get('config:module_roots')

        with spack.config.override('config:module_roots', module_roots):
            for name in enabled:
                generator = spack.modules.module_types[name](spec, env)
                try:
                    getattr(generator, method_name)()
                except RuntimeError as e:
                    msg = 'cannot perform the requested {0} operation on '
                    msg += 'module files [{1}]'
                    tty.warn(msg.format(method_name, str(e)))


def post_install(spec):
    _for_each_enabled(spec, 'write')


def post_uninstall(spec):
    _for_each_enabled(spec, 'remove')
