# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import glob
import json
import os
import shutil
import sys
import tempfile
from typing import List

import llnl.util.tty as tty
import llnl.util.tty.color as clr
from llnl.string import plural
from llnl.util.lang import elide_list

import spack.binary_distribution as bindist
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.environment as ev
import spack.error
import spack.mirror
import spack.relocate
import spack.repo
import spack.spec
import spack.store
import spack.util.crypto
import spack.util.url as url_util
import spack.util.web as web_util
from spack.cmd import display_specs
from spack.spec import Spec, save_dependency_specfiles
from spack.stage import Stage

description = "create, download and install binary packages"
section = "packaging"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser):
    setattr(setup_parser, "parser", subparser)
    subparsers = subparser.add_subparsers(help="buildcache sub-commands")

    push = subparsers.add_parser("push", aliases=["create"], help=push_fn.__doc__)
    push.add_argument("-f", "--force", action="store_true", help="overwrite tarball if it exists")
    push.add_argument(
        "--allow-root",
        "-a",
        action="store_true",
        help="allow install root string in binary files after RPATH substitution",
    )
    push_sign = push.add_mutually_exclusive_group(required=False)
    push_sign.add_argument(
        "--unsigned", "-u", action="store_true", help="push unsigned buildcache tarballs"
    )
    push_sign.add_argument(
        "--key", "-k", metavar="key", type=str, default=None, help="key for signing"
    )
    push.add_argument("mirror", type=str, help="mirror name, path, or URL")
    push.add_argument(
        "--update-index",
        "--rebuild-index",
        action="store_true",
        default=False,
        help="regenerate buildcache index after building package(s)",
    )
    push.add_argument(
        "--spec-file", default=None, help="create buildcache entry for spec from json or yaml file"
    )
    push.add_argument(
        "--only",
        default="package,dependencies",
        dest="things_to_install",
        choices=["package", "dependencies"],
        help="select the buildcache mode. "
        "The default is to build a cache for the package along with all its dependencies. "
        "Alternatively, one can decide to build a cache for only the package or only the "
        "dependencies",
    )
    push.add_argument(
        "--fail-fast",
        action="store_true",
        help="stop pushing on first failure (default is best effort)",
    )
    arguments.add_common_arguments(push, ["specs"])
    push.set_defaults(func=push_fn)

    install = subparsers.add_parser("install", help=install_fn.__doc__)
    install.add_argument(
        "-f", "--force", action="store_true", help="overwrite install directory if it exists"
    )
    install.add_argument(
        "-m", "--multiple", action="store_true", help="allow all matching packages"
    )
    install.add_argument(
        "-u",
        "--unsigned",
        action="store_true",
        help="install unsigned buildcache tarballs for testing",
    )
    install.add_argument(
        "-o",
        "--otherarch",
        action="store_true",
        help="install specs from other architectures instead of default platform and OS",
    )

    arguments.add_common_arguments(install, ["specs"])
    install.set_defaults(func=install_fn)

    listcache = subparsers.add_parser("list", help=list_fn.__doc__)
    arguments.add_common_arguments(listcache, ["long", "very_long", "namespaces"])
    listcache.add_argument(
        "-v",
        "--variants",
        action="store_true",
        dest="variants",
        help="show variants in output (can be long)",
    )
    listcache.add_argument(
        "-a",
        "--allarch",
        action="store_true",
        help="list specs for all available architectures instead of default platform and OS",
    )
    arguments.add_common_arguments(listcache, ["specs"])
    listcache.set_defaults(func=list_fn)

    keys = subparsers.add_parser("keys", help=keys_fn.__doc__)
    keys.add_argument(
        "-i", "--install", action="store_true", help="install Keys pulled from mirror"
    )
    keys.add_argument("-t", "--trust", action="store_true", help="trust all downloaded keys")
    keys.add_argument("-f", "--force", action="store_true", help="force new download of keys")
    keys.set_defaults(func=keys_fn)

    preview = subparsers.add_parser("preview", help=preview_fn.__doc__)
    arguments.add_common_arguments(preview, ["installed_specs"])
    preview.set_defaults(func=preview_fn)

    # Check if binaries need to be rebuilt on remote mirror
    check = subparsers.add_parser("check", help=check_fn.__doc__)
    check.add_argument(
        "-m",
        "--mirror-url",
        default=None,
        help="override any configured mirrors with this mirror URL",
    )

    check.add_argument(
        "-o", "--output-file", default=None, help="file where rebuild info should be written"
    )

    # used to construct scope arguments below
    scopes = spack.config.scopes()

    check.add_argument(
        "--scope",
        choices=scopes,
        metavar=spack.config.SCOPES_METAVAR,
        default=spack.config.default_modify_scope(),
        help="configuration scope containing mirrors to check",
    )
    check_spec_or_specfile = check.add_mutually_exclusive_group(required=True)
    check_spec_or_specfile.add_argument(
        "-s", "--spec", help="check single spec instead of release specs file"
    )
    check_spec_or_specfile.add_argument(
        "--spec-file",
        help="check single spec from json or yaml file instead of release specs file",
    )

    check.set_defaults(func=check_fn)

    # Download tarball and specfile
    download = subparsers.add_parser("download", help=download_fn.__doc__)
    download_spec_or_specfile = download.add_mutually_exclusive_group(required=True)
    download_spec_or_specfile.add_argument(
        "-s", "--spec", help="download built tarball for spec from mirror"
    )
    download_spec_or_specfile.add_argument(
        "--spec-file", help="download built tarball for spec (from json or yaml file) from mirror"
    )
    download.add_argument(
        "-p",
        "--path",
        required=True,
        default=None,
        help="path to directory where tarball should be downloaded",
    )
    download.set_defaults(func=download_fn)

    # Get buildcache name
    getbuildcachename = subparsers.add_parser(
        "get-buildcache-name", help=get_buildcache_name_fn.__doc__
    )
    getbuildcachename_spec_or_specfile = getbuildcachename.add_mutually_exclusive_group(
        required=True
    )
    getbuildcachename_spec_or_specfile.add_argument(
        "-s", "--spec", help="spec string for which buildcache name is desired"
    )
    getbuildcachename_spec_or_specfile.add_argument(
        "--spec-file", help="path to spec json or yaml file for which buildcache name is desired"
    )
    getbuildcachename.set_defaults(func=get_buildcache_name_fn)

    # Given the root spec, save the yaml of the dependent spec to a file
    savespecfile = subparsers.add_parser("save-specfile", help=save_specfile_fn.__doc__)
    savespecfile_spec_or_specfile = savespecfile.add_mutually_exclusive_group(required=True)
    savespecfile_spec_or_specfile.add_argument("--root-spec", help="root spec of dependent spec")
    savespecfile_spec_or_specfile.add_argument(
        "--root-specfile", help="path to json or yaml file containing root spec of dependent spec"
    )
    savespecfile.add_argument(
        "-s",
        "--specs",
        required=True,
        help="list of dependent specs for which saved yaml is desired",
    )
    savespecfile.add_argument(
        "--specfile-dir", required=True, help="path to directory where spec yamls should be saved"
    )
    savespecfile.set_defaults(func=save_specfile_fn)

    # Sync buildcache entries from one mirror to another
    sync = subparsers.add_parser("sync", help=sync_fn.__doc__)
    sync.add_argument(
        "--manifest-glob", help="a quoted glob pattern identifying copy manifest files"
    )
    sync.add_argument(
        "src_mirror",
        metavar="source mirror",
        type=arguments.mirror_name_or_url,
        nargs="?",
        help="source mirror name, path, or URL",
    )
    sync.add_argument(
        "dest_mirror",
        metavar="destination mirror",
        type=arguments.mirror_name_or_url,
        nargs="?",
        help="destination mirror name, path, or URL",
    )
    sync.set_defaults(func=sync_fn)

    # Update buildcache index without copying any additional packages
    update_index = subparsers.add_parser(
        "update-index", aliases=["rebuild-index"], help=update_index_fn.__doc__
    )
    update_index.add_argument(
        "mirror", type=arguments.mirror_name_or_url, help="destination mirror name, path, or URL"
    )
    update_index.add_argument(
        "-k",
        "--keys",
        default=False,
        action="store_true",
        help="if provided, key index will be updated as well as package index",
    )
    update_index.set_defaults(func=update_index_fn)


def _matching_specs(specs: List[Spec]) -> List[Spec]:
    """Disambiguate specs and return a list of matching specs"""
    return [spack.cmd.disambiguate_spec(s, ev.active_environment(), installed=any) for s in specs]


def push_fn(args: argparse.Namespace):
    """create a binary package and push it to a mirror"""
    if args.spec_file:
        tty.warn(
            "The flag `--spec-file` is deprecated and will be removed in Spack 0.22. "
            "Use positional arguments instead."
        )

    if args.specs or args.spec_file:
        specs = _matching_specs(spack.cmd.parse_specs(args.specs or args.spec_file))
    else:
        specs = spack.cmd.require_active_env("buildcache push").all_specs()

    mirror = arguments.mirror_name_or_url(args.mirror)

    if args.allow_root:
        tty.warn(
            "The flag `--allow-root` is the default in Spack 0.21, will be removed in Spack 0.22"
        )

    url = mirror.push_url

    specs = bindist.specs_to_be_packaged(
        specs,
        root="package" in args.things_to_install,
        dependencies="dependencies" in args.things_to_install,
    )

    # When pushing multiple specs, print the url once ahead of time, as well as how
    # many specs are being pushed.
    if len(specs) > 1:
        tty.info(f"Selected {len(specs)} specs to push to {url}")

    skipped = []
    failed = []

    # tty printing
    color = clr.get_color_when()
    format_spec = lambda s: s.format("{name}{@version}{/hash:7}", color=color)
    total_specs = len(specs)
    digits = len(str(total_specs))

    for i, spec in enumerate(specs):
        try:
            bindist.push_or_raise(
                spec,
                url,
                bindist.PushOptions(
                    force=args.force,
                    unsigned=args.unsigned,
                    key=args.key,
                    regenerate_index=args.update_index,
                ),
            )

            if total_specs > 1:
                msg = f"[{i+1:{digits}}/{total_specs}] Pushed {format_spec(spec)}"
            else:
                msg = f"Pushed {format_spec(spec)} to {url}"

            tty.info(msg)

        except bindist.NoOverwriteException:
            skipped.append(format_spec(spec))

        # Catch any other exception unless the fail fast option is set
        except Exception as e:
            if args.fail_fast or isinstance(e, (bindist.PickKeyException, bindist.NoKeyException)):
                raise
            failed.append((format_spec(spec), e))

    if skipped:
        if len(specs) == 1:
            tty.info("The spec is already in the buildcache. Use --force to overwrite it.")
        elif len(skipped) == len(specs):
            tty.info("All specs are already in the buildcache. Use --force to overwrite them.")
        else:
            tty.info(
                "The following {} specs were skipped as they already exist in the buildcache:\n"
                "    {}\n"
                "    Use --force to overwrite them.".format(
                    len(skipped), ", ".join(elide_list(skipped, 5))
                )
            )

    if failed:
        if len(failed) == 1:
            raise failed[0][1]

        raise spack.error.SpackError(
            f"The following {len(failed)} errors occurred while pushing specs to the buildcache",
            "\n".join(
                elide_list([f"    {spec}: {e.__class__.__name__}: {e}" for spec, e in failed], 5)
            ),
        )


def install_fn(args):
    """install from a binary package"""
    if not args.specs:
        tty.die("a spec argument is required to install from a buildcache")

    query = bindist.BinaryCacheQuery(all_architectures=args.otherarch)
    matches = spack.store.find(args.specs, multiple=args.multiple, query_fn=query)
    for match in matches:
        bindist.install_single_spec(match, unsigned=args.unsigned, force=args.force)


def list_fn(args):
    """list binary packages available from mirrors"""
    try:
        specs = bindist.update_cache_and_get_specs()
    except bindist.FetchCacheError as e:
        tty.die(e)

    if not args.allarch:
        arch = spack.spec.Spec.default_arch()
        specs = [s for s in specs if s.intersects(arch)]

    if args.specs:
        constraints = set(args.specs)
        specs = [s for s in specs if any(s.intersects(c) for c in constraints)]
    if sys.stdout.isatty():
        builds = len(specs)
        tty.msg("%s." % plural(builds, "cached build"))
        if not builds and not args.allarch:
            tty.msg(
                "You can query all available architectures with:",
                "spack buildcache list --allarch",
            )
    display_specs(specs, args, all_headers=True)


def keys_fn(args):
    """get public keys available on mirrors"""
    bindist.get_keys(args.install, args.trust, args.force)


def preview_fn(args):
    """analyze an installed spec and reports whether executables and libraries are relocatable"""
    tty.warn(
        "`spack buildcache preview` is deprecated since `spack buildcache push --allow-root` is "
        "now the default. This command will be removed in Spack 0.22"
    )


def check_fn(args: argparse.Namespace):
    """check specs against remote binary mirror(s) to see if any need to be rebuilt

    this command uses the process exit code to indicate its result, specifically, if the
    exit code is non-zero, then at least one of the indicated specs needs to be rebuilt
    """
    if args.spec_file:
        tty.warn(
            "The flag `--spec-file` is deprecated and will be removed in Spack 0.22. "
            "Use --spec instead."
        )

    specs = spack.cmd.parse_specs(args.spec or args.spec_file)

    if specs:
        specs = _matching_specs(specs)
    else:
        specs = spack.cmd.require_active_env("buildcache check").all_specs()

    if not specs:
        tty.msg("No specs provided, exiting.")
        return

    for spec in specs:
        spec.concretize()

    # Next see if there are any configured binary mirrors
    configured_mirrors = spack.config.get("mirrors", scope=args.scope)

    if args.mirror_url:
        configured_mirrors = {"additionalMirrorUrl": args.mirror_url}

    if not configured_mirrors:
        tty.msg("No mirrors provided, exiting.")
        return

    if bindist.check_specs_against_mirrors(configured_mirrors, specs, args.output_file) == 1:
        sys.exit(1)


def download_fn(args):
    """download buildcache entry from a remote mirror to local folder

    this command uses the process exit code to indicate its result, specifically, a non-zero exit
    code indicates that the command failed to download at least one of the required buildcache
    components
    """
    if args.spec_file:
        tty.warn(
            "The flag `--spec-file` is deprecated and will be removed in Spack 0.22. "
            "Use --spec instead."
        )

    specs = _matching_specs(spack.cmd.parse_specs(args.spec or args.spec_file))

    if len(specs) != 1:
        tty.die("a single spec argument is required to download from a buildcache")

    if not bindist.download_single_spec(specs[0], args.path):
        sys.exit(1)


def get_buildcache_name_fn(args):
    """get name (prefix) of buildcache entries for this spec"""
    tty.warn("This command is deprecated and will be removed in Spack 0.22.")
    specs = _matching_specs(spack.cmd.parse_specs(args.spec or args.spec_file))
    if len(specs) != 1:
        tty.die("a single spec argument is required to get buildcache name")
    print(bindist.tarball_name(specs[0], ""))


def save_specfile_fn(args):
    """get full spec for dependencies and write them to files in the specified output directory

    uses exit code to signal success or failure. an exit code of zero means the command was likely
    successful. if any errors or exceptions are encountered, or if expected command-line arguments
    are not provided, then the exit code will be non-zero
    """
    if args.root_specfile:
        tty.warn(
            "The flag `--root-specfile` is deprecated and will be removed in Spack 0.22. "
            "Use --root-spec instead."
        )

    specs = spack.cmd.parse_specs(args.root_spec or args.root_specfile)

    if len(specs) != 1:
        tty.die("a single spec argument is required to save specfile")

    root = specs[0]

    if not root.concrete:
        root.concretize()

    save_dependency_specfiles(
        root, args.specfile_dir, dependencies=spack.cmd.parse_specs(args.specs)
    )


def copy_buildcache_file(src_url, dest_url, local_path=None):
    """Copy from source url to destination url"""
    tmpdir = None

    if not local_path:
        tmpdir = tempfile.mkdtemp()
        local_path = os.path.join(tmpdir, os.path.basename(src_url))

    try:
        temp_stage = Stage(src_url, path=os.path.dirname(local_path))
        try:
            temp_stage.create()
            temp_stage.fetch()
            web_util.push_to_url(local_path, dest_url, keep_original=True)
        except spack.error.FetchError as e:
            # Expected, since we have to try all the possible extensions
            tty.debug("no such file: {0}".format(src_url))
            tty.debug(e)
        finally:
            temp_stage.destroy()
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


def sync_fn(args):
    """sync binaries (and associated metadata) from one mirror to another

    requires an active environment in order to know which specs to sync
    """
    if args.manifest_glob:
        manifest_copy(glob.glob(args.manifest_glob))
        return 0

    if args.src_mirror is None or args.dest_mirror is None:
        tty.die("Provide mirrors to sync from and to.")

    src_mirror = args.src_mirror
    dest_mirror = args.dest_mirror

    src_mirror_url = src_mirror.fetch_url
    dest_mirror_url = dest_mirror.push_url

    # Get the active environment
    env = spack.cmd.require_active_env(cmd_name="buildcache sync")

    tty.msg(
        "Syncing environment buildcache files from {0} to {1}".format(
            src_mirror_url, dest_mirror_url
        )
    )

    build_cache_dir = bindist.build_cache_relative_path()
    buildcache_rel_paths = []

    tty.debug("Syncing the following specs:")
    for s in env.all_specs():
        tty.debug("  {0}{1}: {2}".format("* " if s in env.roots() else "  ", s.name, s.dag_hash()))

        buildcache_rel_paths.extend(
            [
                os.path.join(build_cache_dir, bindist.tarball_path_name(s, ".spack")),
                os.path.join(build_cache_dir, bindist.tarball_name(s, ".spec.json.sig")),
                os.path.join(build_cache_dir, bindist.tarball_name(s, ".spec.json")),
                os.path.join(build_cache_dir, bindist.tarball_name(s, ".spec.yaml")),
            ]
        )

    tmpdir = tempfile.mkdtemp()

    try:
        for rel_path in buildcache_rel_paths:
            src_url = url_util.join(src_mirror_url, rel_path)
            local_path = os.path.join(tmpdir, rel_path)
            dest_url = url_util.join(dest_mirror_url, rel_path)

            tty.debug("Copying {0} to {1} via {2}".format(src_url, dest_url, local_path))
            copy_buildcache_file(src_url, dest_url, local_path=local_path)
    finally:
        shutil.rmtree(tmpdir)


def manifest_copy(manifest_file_list):
    """Read manifest files containing information about specific specs to copy
    from source to destination, remove duplicates since any binary packge for
    a given hash should be the same as any other, and copy all files specified
    in the manifest files."""
    deduped_manifest = {}

    for manifest_path in manifest_file_list:
        with open(manifest_path) as fd:
            manifest = json.loads(fd.read())
            for spec_hash, copy_list in manifest.items():
                # Last duplicate hash wins
                deduped_manifest[spec_hash] = copy_list

    for spec_hash, copy_list in deduped_manifest.items():
        for copy_file in copy_list:
            tty.debug("copying {0} to {1}".format(copy_file["src"], copy_file["dest"]))
            copy_buildcache_file(copy_file["src"], copy_file["dest"])


def update_index(mirror: spack.mirror.Mirror, update_keys=False):
    url = mirror.push_url

    bindist.generate_package_index(url_util.join(url, bindist.build_cache_relative_path()))

    if update_keys:
        keys_url = url_util.join(
            url, bindist.build_cache_relative_path(), bindist.build_cache_keys_relative_path()
        )

        bindist.generate_key_index(keys_url)


def update_index_fn(args):
    """update a buildcache index"""
    update_index(args.mirror, update_keys=args.keys)


def buildcache(parser, args):
    if args.func:
        args.func(args)
