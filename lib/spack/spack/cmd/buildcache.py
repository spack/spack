# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import json
import os
import shutil
import sys
import tempfile

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.environment as ev
import spack.hash_types as ht
import spack.mirror
import spack.relocate
import spack.repo
import spack.spec
import spack.store
import spack.util.crypto
import spack.util.url as url_util
import spack.util.web as web_util
from spack.cmd import display_specs
from spack.error import SpecError
from spack.spec import Spec, save_dependency_specfiles
from spack.stage import Stage
from spack.util.string import plural

description = "create, download and install binary packages"
section = "packaging"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help="buildcache sub-commands")

    create = subparsers.add_parser("create", help=create_fn.__doc__)
    create.add_argument(
        "-r",
        "--rel",
        action="store_true",
        help="make all rpaths relative before creating tarballs.",
    )
    create.add_argument(
        "-f", "--force", action="store_true", help="overwrite tarball if it exists."
    )
    create.add_argument(
        "-u",
        "--unsigned",
        action="store_true",
        help="create unsigned buildcache tarballs for testing",
    )
    create.add_argument(
        "-a",
        "--allow-root",
        action="store_true",
        help="allow install root string in binary files after RPATH substitution",
    )
    create.add_argument(
        "-k", "--key", metavar="key", type=str, default=None, help="Key for signing."
    )
    output = create.add_mutually_exclusive_group(required=False)
    # TODO: remove from Spack 0.21
    output.add_argument(
        "-d",
        "--directory",
        metavar="directory",
        dest="mirror_flag",
        type=arguments.mirror_directory,
        help="local directory where buildcaches will be written. (deprecated)",
    )
    # TODO: remove from Spack 0.21
    output.add_argument(
        "-m",
        "--mirror-name",
        metavar="mirror-name",
        dest="mirror_flag",
        type=arguments.mirror_name,
        help="name of the mirror where buildcaches will be written. (deprecated)",
    )
    # TODO: remove from Spack 0.21
    output.add_argument(
        "--mirror-url",
        metavar="mirror-url",
        dest="mirror_flag",
        type=arguments.mirror_url,
        help="URL of the mirror where buildcaches will be written. (deprecated)",
    )
    # Unfortunately we cannot add this to the mutually exclusive group above,
    # because we have further positional arguments.
    # TODO: require from Spack 0.21
    create.add_argument("mirror", type=str, help="Mirror name, path, or URL.", nargs="?")
    create.add_argument(
        "--rebuild-index",
        action="store_true",
        default=False,
        help="Regenerate buildcache index after building package(s)",
    )
    create.add_argument(
        "--spec-file", default=None, help="Create buildcache entry for spec from json or yaml file"
    )
    create.add_argument(
        "--only",
        default="package,dependencies",
        dest="things_to_install",
        choices=["package", "dependencies"],
        help=(
            "Select the buildcache mode. the default is to"
            " build a cache for the package along with all"
            " its dependencies. Alternatively, one can"
            " decide to build a cache for only the package"
            " or only the dependencies"
        ),
    )
    arguments.add_common_arguments(create, ["specs"])
    create.set_defaults(func=create_fn)

    install = subparsers.add_parser("install", help=install_fn.__doc__)
    install.add_argument(
        "-f", "--force", action="store_true", help="overwrite install directory if it exists."
    )
    install.add_argument(
        "-m", "--multiple", action="store_true", help="allow all matching packages "
    )
    install.add_argument(
        "-a",
        "--allow-root",
        action="store_true",
        help="allow install root string in binary files after RPATH substitution",
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
    arguments.add_common_arguments(listcache, ["long", "very_long"])
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
        help="Override any configured mirrors with this mirror URL",
    )

    check.add_argument(
        "-o", "--output-file", default=None, help="File where rebuild info should be written"
    )

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    check.add_argument(
        "--scope",
        choices=scopes,
        metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope containing mirrors to check",
    )

    check.add_argument(
        "-s", "--spec", default=None, help="Check single spec instead of release specs file"
    )

    check.add_argument(
        "--spec-file",
        default=None,
        help=("Check single spec from json or yaml file instead of release specs file"),
    )

    check.set_defaults(func=check_fn)

    # Download tarball and specfile
    download = subparsers.add_parser("download", help=download_fn.__doc__)
    download.add_argument(
        "-s", "--spec", default=None, help="Download built tarball for spec from mirror"
    )
    download.add_argument(
        "--spec-file",
        default=None,
        help=("Download built tarball for spec (from json or yaml file) from mirror"),
    )
    download.add_argument(
        "-p", "--path", default=None, help="Path to directory where tarball should be downloaded"
    )
    download.set_defaults(func=download_fn)

    # Get buildcache name
    getbuildcachename = subparsers.add_parser(
        "get-buildcache-name", help=get_buildcache_name_fn.__doc__
    )
    getbuildcachename.add_argument(
        "-s", "--spec", default=None, help="Spec string for which buildcache name is desired"
    )
    getbuildcachename.add_argument(
        "--spec-file",
        default=None,
        help=("Path to spec json or yaml file for which buildcache name is desired"),
    )
    getbuildcachename.set_defaults(func=get_buildcache_name_fn)

    # Given the root spec, save the yaml of the dependent spec to a file
    savespecfile = subparsers.add_parser("save-specfile", help=save_specfile_fn.__doc__)
    savespecfile.add_argument("--root-spec", default=None, help="Root spec of dependent spec")
    savespecfile.add_argument(
        "--root-specfile",
        default=None,
        help="Path to json or yaml file containing root spec of dependent spec",
    )
    savespecfile.add_argument(
        "-s",
        "--specs",
        default=None,
        help="List of dependent specs for which saved yaml is desired",
    )
    savespecfile.add_argument(
        "--specfile-dir", default=None, help="Path to directory where spec yamls should be saved"
    )
    savespecfile.set_defaults(func=save_specfile_fn)

    # Sync buildcache entries from one mirror to another
    sync = subparsers.add_parser("sync", help=sync_fn.__doc__)
    sync.add_argument(
        "--manifest-glob",
        default=None,
        help="A quoted glob pattern identifying copy manifest files",
    )
    source = sync.add_mutually_exclusive_group(required=False)
    # TODO: remove in Spack 0.21
    source.add_argument(
        "--src-directory",
        metavar="DIRECTORY",
        dest="src_mirror_flag",
        type=arguments.mirror_directory,
        help="Source mirror as a local file path (deprecated)",
    )
    # TODO: remove in Spack 0.21
    source.add_argument(
        "--src-mirror-name",
        metavar="MIRROR_NAME",
        dest="src_mirror_flag",
        type=arguments.mirror_name,
        help="Name of the source mirror (deprecated)",
    )
    # TODO: remove in Spack 0.21
    source.add_argument(
        "--src-mirror-url",
        metavar="MIRROR_URL",
        dest="src_mirror_flag",
        type=arguments.mirror_url,
        help="URL of the source mirror (deprecated)",
    )
    # TODO: only support this in 0.21
    source.add_argument(
        "src_mirror",
        metavar="source mirror",
        type=arguments.mirror_name_or_url,
        help="Source mirror name, path, or URL",
        nargs="?",
    )
    dest = sync.add_mutually_exclusive_group(required=False)
    # TODO: remove in Spack 0.21
    dest.add_argument(
        "--dest-directory",
        metavar="DIRECTORY",
        dest="dest_mirror_flag",
        type=arguments.mirror_directory,
        help="Destination mirror as a local file path (deprecated)",
    )
    # TODO: remove in Spack 0.21
    dest.add_argument(
        "--dest-mirror-name",
        metavar="MIRROR_NAME",
        type=arguments.mirror_name,
        dest="dest_mirror_flag",
        help="Name of the destination mirror (deprecated)",
    )
    # TODO: remove in Spack 0.21
    dest.add_argument(
        "--dest-mirror-url",
        metavar="MIRROR_URL",
        dest="dest_mirror_flag",
        type=arguments.mirror_url,
        help="URL of the destination mirror (deprecated)",
    )
    # TODO: only support this in 0.21
    dest.add_argument(
        "dest_mirror",
        metavar="destination mirror",
        type=arguments.mirror_name_or_url,
        help="Destination mirror name, path, or URL",
        nargs="?",
    )
    sync.set_defaults(func=sync_fn)

    # Update buildcache index without copying any additional packages
    update_index = subparsers.add_parser("update-index", help=update_index_fn.__doc__)
    update_index_out = update_index.add_mutually_exclusive_group(required=True)
    # TODO: remove in Spack 0.21
    update_index_out.add_argument(
        "-d",
        "--directory",
        metavar="directory",
        dest="mirror_flag",
        type=arguments.mirror_directory,
        help="local directory where buildcaches will be written (deprecated)",
    )
    # TODO: remove in Spack 0.21
    update_index_out.add_argument(
        "-m",
        "--mirror-name",
        metavar="mirror-name",
        dest="mirror_flag",
        type=arguments.mirror_name,
        help="name of the mirror where buildcaches will be written (deprecated)",
    )
    # TODO: remove in Spack 0.21
    update_index_out.add_argument(
        "--mirror-url",
        metavar="mirror-url",
        dest="mirror_flag",
        type=arguments.mirror_url,
        help="URL of the mirror where buildcaches will be written (deprecated)",
    )
    # TODO: require from Spack 0.21
    update_index_out.add_argument(
        "mirror",
        type=arguments.mirror_name_or_url,
        help="Destination mirror name, path, or URL",
        nargs="?",
    )
    update_index.add_argument(
        "-k",
        "--keys",
        default=False,
        action="store_true",
        help="If provided, key index will be updated as well as package index",
    )
    update_index.set_defaults(func=update_index_fn)


def _matching_specs(specs, spec_file):
    """Return a list of matching specs read from either a spec file (JSON or YAML),
    a query over the store or a query over the active environment.
    """
    env = ev.active_environment()
    hashes = env.all_hashes() if env else None
    if spec_file:
        return spack.store.specfile_matches(spec_file, hashes=hashes)

    if specs:
        constraints = spack.cmd.parse_specs(specs)
        return spack.store.find(constraints, hashes=hashes)

    if env:
        return [concrete for _, concrete in env.concretized_specs()]

    tty.die(
        "build cache file creation requires at least one"
        " installed package spec, an active environment,"
        " or else a path to a json or yaml file containing a spec"
        " to install"
    )


def _concrete_spec_from_args(args):
    spec_str, specfile_path = args.spec, args.spec_file

    if not spec_str and not specfile_path:
        tty.error("must provide either spec string or path to YAML or JSON specfile")
        sys.exit(1)

    if spec_str:
        try:
            constraints = spack.cmd.parse_specs(spec_str)
            spec = spack.store.find(constraints)[0]
            spec.concretize()
        except SpecError as spec_error:
            tty.error("Unable to concretize spec {0}".format(spec_str))
            tty.debug(spec_error)
            sys.exit(1)

        return spec

    return Spec.from_specfile(specfile_path)


def create_fn(args):
    """create a binary package and push it to a mirror"""
    if args.mirror_flag:
        mirror = args.mirror_flag
    elif not args.mirror:
        raise ValueError("No mirror provided")
    else:
        mirror = arguments.mirror_name_or_url(args.mirror)

    if args.mirror_flag:
        tty.warn(
            "Using flags to specify mirrors is deprecated and will be removed in "
            "Spack 0.21, use positional arguments instead."
        )

    # TODO: remove this in 0.21. If we have mirror_flag, the first
    # spec is in the positional mirror arg due to argparse limitations.
    specs = args.specs
    if args.mirror_flag and args.mirror:
        specs.insert(0, args.mirror)

    url = mirror.push_url

    matches = _matching_specs(specs, args.spec_file)

    msg = "Pushing binary packages to {0}/build_cache".format(url)
    tty.msg(msg)
    kwargs = {
        "key": args.key,
        "force": args.force,
        "relative": args.rel,
        "unsigned": args.unsigned,
        "allow_root": args.allow_root,
        "regenerate_index": args.rebuild_index,
    }
    bindist.push(
        matches,
        url,
        include_root="package" in args.things_to_install,
        include_dependencies="dependencies" in args.things_to_install,
        **kwargs,
    )


def install_fn(args):
    """install from a binary package"""
    if not args.specs:
        tty.die("a spec argument is required to install from a buildcache")

    query = bindist.BinaryCacheQuery(all_architectures=args.otherarch)
    matches = spack.store.find(args.specs, multiple=args.multiple, query_fn=query)
    for match in matches:
        bindist.install_single_spec(
            match, allow_root=args.allow_root, unsigned=args.unsigned, force=args.force
        )


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
    """analyze an installed spec and reports whether executables
    and libraries are relocatable
    """
    constraints = spack.cmd.parse_specs(args.specs)
    specs = spack.store.find(constraints, multiple=True)

    # Cycle over the specs that match
    for spec in specs:
        print("Relocatable nodes")
        print("--------------------------------")
        print(spec.tree(status_fn=spack.relocate.is_relocatable))


def check_fn(args):
    """Check specs (either a single spec from --spec, or else the full set
    of release specs) against remote binary mirror(s) to see if any need
    to be rebuilt.  This command uses the process exit code to indicate
    its result, specifically, if the exit code is non-zero, then at least
    one of the indicated specs needs to be rebuilt.
    """
    if args.spec or args.spec_file:
        specs = [_concrete_spec_from_args(args)]
    else:
        env = spack.cmd.require_active_env(cmd_name="buildcache")
        env.concretize()
        specs = env.all_specs()

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
    """Download buildcache entry from a remote mirror to local folder.  This
    command uses the process exit code to indicate its result, specifically,
    a non-zero exit code indicates that the command failed to download at
    least one of the required buildcache components."""
    if not args.spec and not args.spec_file:
        tty.msg("No specs provided, exiting.")
        return

    if not args.path:
        tty.msg("No download path provided, exiting")
        return

    spec = _concrete_spec_from_args(args)
    result = bindist.download_single_spec(spec, args.path)

    if not result:
        sys.exit(1)


def get_buildcache_name_fn(args):
    """Get name (prefix) of buildcache entries for this spec"""
    spec = _concrete_spec_from_args(args)
    buildcache_name = bindist.tarball_name(spec, "")
    print("{0}".format(buildcache_name))


def save_specfile_fn(args):
    """Get full spec for dependencies, relative to root spec, and write them
    to files in the specified output directory.  Uses exit code to signal
    success or failure.  An exit code of zero means the command was likely
    successful.  If any errors or exceptions are encountered, or if expected
    command-line arguments are not provided, then the exit code will be
    non-zero.
    """
    if not args.root_spec and not args.root_specfile:
        tty.msg("No root spec provided, exiting.")
        sys.exit(1)

    if not args.specs:
        tty.msg("No dependent specs provided, exiting.")
        sys.exit(1)

    if not args.specfile_dir:
        tty.msg("No yaml directory provided, exiting.")
        sys.exit(1)

    if args.root_specfile:
        with open(args.root_specfile) as fd:
            root_spec_as_json = fd.read()
        spec_format = "yaml" if args.root_specfile.endswith("yaml") else "json"
    else:
        root_spec = Spec(args.root_spec)
        root_spec.concretize()
        root_spec_as_json = root_spec.to_json(hash=ht.dag_hash)
        spec_format = "json"
    save_dependency_specfiles(
        root_spec_as_json, args.specfile_dir, args.specs.split(), spec_format
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
        except web_util.FetchError as e:
            # Expected, since we have to try all the possible extensions
            tty.debug("no such file: {0}".format(src_url))
            tty.debug(e)
        finally:
            temp_stage.destroy()
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


def sync_fn(args):
    """Syncs binaries (and associated metadata) from one mirror to another.
    Requires an active environment in order to know which specs to sync.

    Args:
        src (str): Source mirror URL
        dest (str): Destination mirror URL
    """
    if args.manifest_glob:
        manifest_copy(glob.glob(args.manifest_glob))
        return 0

    # If no manifest_glob, require a source and dest mirror.
    # TODO: Simplify in Spack 0.21
    if not (args.src_mirror_flag or args.src_mirror) or not (
        args.dest_mirror_flag or args.dest_mirror
    ):
        raise ValueError("Source and destination mirror are required.")

    if args.src_mirror_flag or args.dest_mirror_flag:
        tty.warn(
            "Using flags to specify mirrors is deprecated and will be removed in "
            "Spack 0.21, use positional arguments instead."
        )

    src_mirror = args.src_mirror_flag if args.src_mirror_flag else args.src_mirror
    dest_mirror = args.dest_mirror_flag if args.dest_mirror_flag else args.dest_mirror

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
    """Update a buildcache index."""
    if args.mirror_flag:
        tty.warn(
            "Using flags to specify mirrors is deprecated and will be removed in "
            "Spack 0.21, use positional arguments instead."
        )
    mirror = args.mirror_flag if args.mirror_flag else args.mirror
    update_index(mirror, update_keys=args.keys)


def buildcache(parser, args):
    if args.func:
        args.func(args)
