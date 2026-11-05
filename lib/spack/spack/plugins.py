# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Discovery and activation of subsystem plugins installed in Spack's Python environment."""

import inspect
from typing import Optional, Type, TypeVar, Union, cast

import spack.config
import spack.util.lang
import spack.util.tty

PluginType = TypeVar("PluginType")


def get_plugin(
    group_name: str,
    selected_name: Optional[str],
    default_class: Type[PluginType],
    *,
    base_class: Optional[Type[PluginType]] = None,
) -> Union[Type[PluginType], PluginType]:
    """Load a selected ``spack.plugins.<group_name>`` class or instance.

    Entry points may provide a class, an instance, or a no-argument setup hook returning either.
    The result must implement ``base_class``, which defaults to ``default_class``. Missing or
    ``default`` selections use the built-in without discovering or loading any entry points.
    """
    if selected_name is None or selected_name == "default":
        return default_class
    group = f"spack.plugins.{group_name}"
    interface = base_class or default_class
    try:
        entries = [
            entry
            for entry in spack.util.lang.get_entry_points(group=group)
            if entry.name == selected_name
        ]
        if not entries:
            raise ValueError(f"no matching {group} entry point is installed")
        if len(entries) != 1:
            raise ValueError(f"multiple {group} entry points have this name")
        target = entries[0].load()
        plugin = target if isinstance(target, (type, interface)) else target()
        if isinstance(plugin, type):
            if not issubclass(plugin, interface) or inspect.isabstract(plugin):
                raise TypeError(
                    f"entry point must provide a concrete {interface.__name__} subclass"
                )
        elif not isinstance(plugin, interface):
            raise TypeError(f"entry point must provide a {interface.__name__} class or instance")
        return cast(Union[Type[PluginType], PluginType], plugin)
    except Exception as error:
        spack.util.tty.warn(
            f"Could not load {group_name} plugin '{selected_name}': {error}; "
            f"using default {default_class.__name__}"
        )
        return default_class


def create_plugin(
    group_name: str,
    default_class: Type[PluginType],
    *args,
    base_class: Optional[Type[PluginType]] = None,
    **kwargs,
) -> PluginType:
    """Construct the configured subsystem plugin, falling back on initialization errors.

    Setup hooks returning instances own their initialization; constructor arguments are passed
    only to classes. Failures in subsequent engine methods are not handled here.
    """
    selected_name = spack.config.CONFIG.get(f"config:plugins:{group_name}")
    plugin = get_plugin(group_name, selected_name, default_class, base_class=base_class)
    try:
        return plugin(*args, **kwargs) if isinstance(plugin, type) else plugin
    except Exception as error:
        if plugin is default_class:
            raise
        spack.util.tty.warn(
            f"Could not initialize {group_name} plugin '{selected_name}': {error}; "
            f"using default {default_class.__name__}"
        )
        return default_class(*args, **kwargs)
