# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import functools
import os

import spack.cmd.common.arguments
import spack.cmd.modules
import spack.config
import spack.modules
import spack.modules.cache
import spack.repo
import spack.store
from spack.util import tty
from spack.util.string import plural


def add_command(parser, command_dict):
    tcl_parser = parser.add_parser("tcl", help="manipulate tcl module files")
    sp = spack.cmd.modules.setup_parser(tcl_parser)

    # Set default module file for a package
    setdefault_parser = sp.add_parser(
        "setdefault", help="set the default module file for a package"
    )
    spack.cmd.common.arguments.add_common_arguments(setdefault_parser, ["constraint"])

    # Build or clear module cache in modulepath directories managed by spack
    sp.add_parser("cachebuild", help="build module cache")
    sp.add_parser("cacheclear", help="clear module cache")

    callbacks = dict(spack.cmd.modules.callbacks.items())
    callbacks["setdefault"] = setdefault
    callbacks["cachebuild"] = cachebuild
    callbacks["cacheclear"] = cacheclear

    command_dict["tcl"] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type="tcl", callbacks=callbacks
    )


def setdefault(module_type, specs, args):
    """set the default module file, when multiple are present"""
    # Currently, accepts only a single matching spec
    spack.cmd.modules.one_spec_or_raise(specs)
    spec = specs[0]
    data = {"modules": {args.module_set_name: {"tcl": {"defaults": [str(spec)]}}}}
    scope = spack.config.InternalConfigScope("tcl-setdefault", data)
    with spack.config.CONFIG.override(scope):
        writer = spack.modules.module_types["tcl"].from_spec(spec, args.module_set_name)
        writer.update_module_defaults()
        writer.register_cache_update()


def _spack_modulepaths(module_type, args):
    """Modulepath directories of the module set holding module files for the
    installed specs."""
    spack.cmd.modules.check_module_set_name(args.module_set_name)
    cls = spack.modules.module_types[module_type]
    cache = {}
    dirs = set()
    for spec in spack.store.STORE.db.query():
        if not spack.repo.PATH.exists(spec.name):
            continue
        writer = cls.from_spec(spec, args.module_set_name, cache=cache)
        if not writer.conf.excluded:
            dirs.add(writer.layout.modulepath)
    return sorted(d for d in dirs if os.path.isdir(d))


def cachebuild(module_type, specs, args):
    """build the module cache of every modulepath directory managed by spack"""
    dirs = _spack_modulepaths(module_type, args)
    if not dirs:
        tty.msg("No modulepath directory found to build module cache")
        return
    dirs_str = plural(len(dirs), "modulepath directory", "modulepath directories")
    tty.msg(f"Building module cache in {dirs_str}")
    spack.modules.cache.cachebuild(dirs)


def cacheclear(module_type, specs, args):
    """clear the module cache of every modulepath directory managed by spack"""
    dirs = _spack_modulepaths(module_type, args)
    if not dirs:
        tty.msg("No modulepath directory found to clear module cache")
        return
    dirs_str = plural(len(dirs), "modulepath directory", "modulepath directories")
    tty.msg(f"Clearing module cache in {dirs_str}")
    spack.modules.cache.cacheclear(dirs)
