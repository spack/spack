# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.spec
import spack.util.path
import spack.version
from spack.error import SpackError

description = "add a spec to an environment's dev-build information"
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument("-p", "--path", help="source location of package")

    clone_group = subparser.add_mutually_exclusive_group()
    clone_group.add_argument(
        "--no-clone",
        action="store_false",
        dest="clone",
        default=None,
        help="do not clone, the package already exists at the source path",
    )
    clone_group.add_argument(
        "--clone",
        action="store_true",
        dest="clone",
        default=None,
        help="clone the package even if the path already exists",
    )

    scopes = spack.config.scopes()
    scopes_metavar = spack.config.SCOPES_METAVAR
    subparser.add_argument(
        "--scope", choices=scopes, metavar=scopes_metavar, help="configuration scope to modify"
    )

    subparser.add_argument(
        "-f", "--force", help="remove any files or directories that block cloning source code"
    )

    arguments.add_common_arguments(subparser, ["spec"])


def _update_config(spec, path):
    dev_configs = spack.config.matched_config("develop")

    entry = {"spec": str(spec)}
    if path != spec.name:
        entry["path"] = path

    found = False
    for scope, dev_config in dev_configs:
        if spec.name in dev_config:
            tty.msg(
                "Updating develop spec {0}:\n\told: {1}\n\tnew: {2}".format(
                    str(spec), dev_config[spec.name], path
                )
            )
            dev_config[spec.name] = entry
            found = True
            break

    # If the dev spec exists in a particular scope already, modify
    # that scope specifically
    if found:
        spack.config.set("develop", dev_config, scope=scope)
        return

    tty.msg("New development spec: {0}".format(str(spec)))

    for scope, dev_config in dev_configs:
        if dev_config:
            dev_config[spec.name] = entry
            found = True
            break

    # If the dev spec exists nowhere, then write this new dev spec
    # into the highest priority scope where dev specs are defined
    if found:
        spack.config.set("develop", dev_config, scope=scope)
        return

    # If no dev specs are defined anywhere, then write this into the
    # highest-priority scope
    scope = dev_configs[0][0]
    dev_config = {spec.name: entry}
    spack.config.set("develop", dev_config, scope=scope)


def _retrieve_develop_source(spec, abspath):
    # "steal" the source code via staging API. We ask for a stage
    # to be created, then copy it afterwards somewhere else. It would be
    # better if we can create the `source_path` directly into its final
    # destination.
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    # We construct a package class ourselves, rather than asking for
    # Spec.package, since Spec only allows this when it is concrete
    package = pkg_cls(spec)
    if isinstance(package.stage[0].fetcher, spack.fetch_strategy.GitFetchStrategy):
        package.stage[0].fetcher.get_full_repo = True
        # If we retrieved this version before and cached it, we may have
        # done so without cloning the full git repo; likewise, any
        # mirror might store an instance with truncated history.
        package.stage[0].disable_mirrors()

    package.stage.steal_source(abspath)


def develop(parser, args):
    if not args.spec:
        env = spack.cmd.require_active_env(cmd_name="develop")
        if args.clone is False:
            raise SpackError("No spec provided to spack develop command")

        # download all dev specs
        for name, entry in env.dev_specs.items():
            path = entry.get("path", name)
            abspath = spack.util.path.canonicalize_path(path, default_wd=env.path)

            if os.path.exists(abspath):
                msg = "Skipping developer download of %s" % entry["spec"]
                msg += " because its path already exists."
                tty.msg(msg)
                continue

            # Both old syntax `spack develop pkg@x` and new syntax `spack develop pkg@=x`
            # are currently supported.
            spec = spack.spec.parse_with_version_concrete(entry["spec"])
            _retrieve_develop_source(spec, abspath)

        if not env.dev_specs:
            tty.warn("No develop specs to download")

        return

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        raise SpackError("spack develop requires at most one named spec")

    spec = specs[0]
    version = spec.versions.concrete_range_as_version
    if not version:
        raise SpackError("Packages to develop must have a concrete version")
    spec.versions = spack.version.VersionList([version])

    # If user does not specify --path, we choose to create a directory in the
    # active environment's directory, named after the spec
    path = args.path or spec.name
    if not os.path.isabs(path):
        env = spack.cmd.require_active_env(cmd_name="develop")
        abspath = spack.util.path.canonicalize_path(path, default_wd=env.path)
    else:
        abspath = path

    # clone default: only if the path doesn't exist
    clone = args.clone
    if clone is None:
        clone = not os.path.exists(abspath)

    if not clone and not os.path.exists(abspath):
        raise SpackError("Provided path %s does not exist" % abspath)

    if clone:
        if os.path.exists(abspath):
            if args.force:
                shutil.rmtree(abspath)
            else:
                msg = "Path %s already exists and cannot be cloned to." % abspath
                msg += " Use `spack develop -f` to overwrite."
                raise SpackError(msg)

        _retrieve_develop_source(spec, abspath)

    # Note: we could put develop specs in any scope, but I assume
    # users would only ever want to do this for either (a) an active
    # env or (b) a specified config file (e.g. that is included by
    # an environment)
    # TODO: when https://github.com/spack/spack/pull/35307 is merged,
    # an active env is not required if a scope is specified
    env = spack.cmd.require_active_env(cmd_name="develop")
    tty.debug("Updating develop config for {0} transactionally".format(env.name))
    with env.write_transaction():
        _update_config(spec, path)
