# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty

import spack.config
import spack.modules


def _for_each_enabled(spec, method_name, explicit=None):
    """Calls a method for each enabled module"""
    set_names = set(spack.config.get("modules", {}).keys())
    for name in set_names:
        enabled = spack.config.get("modules:%s:enable" % name)
        if not enabled:
            tty.debug("NO MODULE WRITTEN: list of enabled module files is empty")
            continue

        for module_type in enabled:
            generator = spack.modules.module_types[module_type](spec, name, explicit)
            try:
                getattr(generator, method_name)()
            except RuntimeError as e:
                msg = "cannot perform the requested {0} operation on module files"
                msg += " [{1}]"
                tty.warn(msg.format(method_name, str(e)))


def post_install(spec, explicit):
    import spack.environment as ev  # break import cycle

    if ev.active_environment():
        # If the installed through an environment, we skip post_install
        # module generation and generate the modules on env_write so Spack
        # can manage interactions between env views and modules
        return

    _for_each_enabled(spec, "write", explicit)


def post_uninstall(spec):
    _for_each_enabled(spec, "remove")


def post_env_write(env):
    for spec in env.new_installs:
        _for_each_enabled(spec, "write")
