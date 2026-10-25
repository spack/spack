# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional, Set

import spack.config
import spack.modules
import spack.spec
from spack.util import tty


def _for_each_enabled(
    spec: spack.spec.Spec, method_name: str, explicit: Optional[bool] = None, add_op: bool = True
) -> None:
    """Calls a method for each enabled module"""
    set_names: Set[str] = set(spack.config.CONFIG.get("modules", {}).keys())
    for name in set_names:
        enabled = spack.config.CONFIG.get(f"modules:{name}:enable")
        if not enabled:
            tty.debug("NO MODULE WRITTEN: list of enabled module files is empty")
            continue

        for module_type in enabled:
            generator = spack.modules.module_types[module_type].from_spec(
                spec, name, explicit, add_op=add_op
            )
            try:
                getattr(generator, method_name)()
            except RuntimeError as e:
                msg = "cannot perform the requested {0} operation on module files"
                msg += " [{1}]"
                tty.warn(msg.format(method_name, str(e)))


def post_install(spec, explicit: bool):
    _for_each_enabled(spec, "write", explicit)


def post_uninstall(spec):
    _for_each_enabled(spec, "remove_installation", add_op=False)
