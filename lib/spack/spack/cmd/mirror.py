# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.lang as lang
import llnl.util.tty as tty
import llnl.util.tty.colify as colify

import spack.caches
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.concretize
import spack.config
import spack.environment as ev
import spack.mirror
import spack.repo
import spack.spec
import spack.util.path
import spack.util.web as web_util
from spack.error import SpackError
from spack.util.spack_yaml import syaml_dict

description = "manage mirrors (source and binary)"
section = "config"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["no_checksum", "deprecated"])

    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="mirror_command")

    # Create
    create_parser = sp.add_parser("create", help=mirror_create.__doc__)
    create_parser.add_argument(
        "-d", "--directory", default=None, help="directory in which to create mirror"
    )

    create_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="mirror all versions of all packages in Spack, or all packages"
        " in the current environment if there is an active environment"
        " (this requires significant time and space)",
    )
    create_parser.add_argument("-f", "--file", help="file with specs of packages to put in mirror")
    create_parser.add_argument(
        "--exclude-file",
        help="specs which Spack should not try to add to a mirror"
        " (listed in a file, one per line)",
    )
    create_parser.add_argument(
        "--exclude-specs",
        help="specs which Spack should not try to add to a mirror" " (specified on command line)",
    )

    create_parser.add_argument(
        "--skip-unstable-versions",
        action="store_true",
        help="don't cache versions unless they identify a stable (unchanging)" " source code",
    )
    create_parser.add_argument(
        "-D", "--dependencies", action="store_true", help="also fetch all dependencies"
    )
    create_parser.add_argument(
        "-n",
        "--versions-per-spec",
        help="the number of versions to fetch for each spec, choose 'all' to"
        " retrieve all versions of each package",
    )
    arguments.add_common_arguments(create_parser, ["specs"])

    # Destroy
    destroy_parser = sp.add_parser("destroy", help=mirror_destroy.__doc__)

    destroy_target = destroy_parser.add_mutually_exclusive_group(required=True)
    destroy_target.add_argument(
        "-m",
        "--mirror-name",
        metavar="mirror_name",
        type=str,
        help="find mirror to destroy by name",
    )
    destroy_target.add_argument(
        "--mirror-url", metavar="mirror_url", type=str, help="find mirror to destroy by url"
    )

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    # Add
    add_parser = sp.add_parser("add", help=mirror_add.__doc__)
    add_parser.add_argument("name", help="mnemonic name for mirror", metavar="mirror")
    add_parser.add_argument("url", help="url of mirror directory from 'spack mirror create'")
    add_parser.add_argument(
        "--scope",
        choices=scopes,
        metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )
    arguments.add_s3_connection_args(add_parser, False)
    # Remove
    remove_parser = sp.add_parser("remove", aliases=["rm"], help=mirror_remove.__doc__)
    remove_parser.add_argument("name", help="mnemonic name for mirror", metavar="mirror")
    remove_parser.add_argument(
        "--scope",
        choices=scopes,
        metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )

    # Set-Url
    set_url_parser = sp.add_parser("set-url", help=mirror_set_url.__doc__)
    set_url_parser.add_argument("name", help="mnemonic name for mirror", metavar="mirror")
    set_url_parser.add_argument("url", help="url of mirror directory from 'spack mirror create'")
    set_url_parser.add_argument(
        "--push", action="store_true", help="set only the URL used for uploading new packages"
    )
    set_url_parser.add_argument(
        "--scope",
        choices=scopes,
        metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope to modify",
    )
    arguments.add_s3_connection_args(set_url_parser, False)

    # List
    list_parser = sp.add_parser("list", help=mirror_list.__doc__)
    list_parser.add_argument(
        "--scope",
        choices=scopes,
        metavar=scopes_metavar,
        default=spack.config.default_list_scope(),
        help="configuration scope to read from",
    )


def mirror_add(args):
    """Add a mirror to Spack."""
    if (
        args.s3_access_key_id
        or args.s3_access_key_secret
        or args.s3_access_token
        or args.s3_profile
        or args.s3_endpoint_url
    ):
        connection = {"url": args.url}
        if args.s3_access_key_id and args.s3_access_key_secret:
            connection["access_pair"] = (args.s3_access_key_id, args.s3_access_key_secret)
        if args.s3_access_token:
            connection["access_token"] = args.s3_access_token
        if args.s3_profile:
            connection["profile"] = args.s3_profile
        if args.s3_endpoint_url:
            connection["endpoint_url"] = args.s3_endpoint_url
        mirror = spack.mirror.Mirror(fetch_url=connection, push_url=connection, name=args.name)
    else:
        mirror = spack.mirror.Mirror(args.url, name=args.name)
    spack.mirror.add(mirror, args.scope)


def mirror_remove(args):
    """Remove a mirror by name."""
    spack.mirror.remove(args.name, args.scope)


def mirror_set_url(args):
    """Change the URL of a mirror."""
    url = args.url
    mirrors = spack.config.get("mirrors", scope=args.scope)
    if not mirrors:
        mirrors = syaml_dict()

    if args.name not in mirrors:
        tty.die("No mirror found with name %s." % args.name)

    entry = mirrors[args.name]
    key_values = ["s3_access_key_id", "s3_access_token", "s3_profile"]

    if any(value for value in key_values if value in args):
        incoming_data = {
            "url": url,
            "access_pair": (args.s3_access_key_id, args.s3_access_key_secret),
            "access_token": args.s3_access_token,
            "profile": args.s3_profile,
            "endpoint_url": args.s3_endpoint_url,
        }
    try:
        fetch_url = entry["fetch"]
        push_url = entry["push"]
    except TypeError:
        fetch_url, push_url = entry, entry

    changes_made = False

    if args.push:
        if isinstance(push_url, dict):
            changes_made = changes_made or push_url != incoming_data
            push_url = incoming_data
        else:
            changes_made = changes_made or push_url != url
            push_url = url
    else:
        if isinstance(push_url, dict):
            changes_made = changes_made or push_url != incoming_data or push_url != incoming_data
            fetch_url, push_url = incoming_data, incoming_data
        else:
            changes_made = changes_made or push_url != url
            fetch_url, push_url = url, url

    items = [
        (
            (n, u)
            if n != args.name
            else (
                (n, {"fetch": fetch_url, "push": push_url})
                if fetch_url != push_url
                else (n, {"fetch": fetch_url, "push": fetch_url})
            )
        )
        for n, u in mirrors.items()
    ]

    mirrors = syaml_dict(items)
    spack.config.set("mirrors", mirrors, scope=args.scope)

    if changes_made:
        tty.msg(
            "Changed%s url or connection information for mirror %s."
            % ((" (push)" if args.push else ""), args.name)
        )
    else:
        tty.msg("No changes made to mirror %s." % args.name)


def mirror_list(args):
    """Print out available mirrors to the console."""

    mirrors = spack.mirror.MirrorCollection(scope=args.scope)
    if not mirrors:
        tty.msg("No mirrors configured.")
        return

    mirrors.display()


def specs_from_text_file(filename, concretize=False):
    """Return a list of specs read from a text file.

    The file should contain one spec per line.

    Args:
        filename (str): name of the file containing the abstract specs.
        concretize (bool): if True concretize the specs before returning
            the list.
    """
    with open(filename, "r") as f:
        specs_in_file = f.readlines()
        specs_in_file = [s.strip() for s in specs_in_file]
    return spack.cmd.parse_specs(" ".join(specs_in_file), concretize=concretize)


def concrete_specs_from_user(args):
    """Return the list of concrete specs that the user wants to mirror. The list
    is passed either from command line or from a text file.
    """
    specs = concrete_specs_from_cli_or_file(args)
    specs = extend_with_additional_versions(specs, num_versions=versions_per_spec(args))
    if args.dependencies:
        specs = extend_with_dependencies(specs)
    specs = filter_externals(specs)
    specs = list(set(specs))
    specs.sort(key=lambda s: (s.name, s.version))
    specs, _ = lang.stable_partition(specs, predicate_fn=not_excluded_fn(args))
    return specs


def extend_with_additional_versions(specs, num_versions):
    if num_versions == "all":
        mirror_specs = spack.mirror.get_all_versions(specs)
    else:
        mirror_specs = spack.mirror.get_matching_versions(specs, num_versions=num_versions)
    mirror_specs = [x.concretized() for x in mirror_specs]
    return mirror_specs


def filter_externals(specs):
    specs, external_specs = lang.stable_partition(specs, predicate_fn=lambda x: not x.external)
    for spec in external_specs:
        msg = "Skipping {0} as it is an external spec."
        tty.msg(msg.format(spec.cshort_spec))
    return specs


def extend_with_dependencies(specs):
    """Extend the input list by adding all the dependencies explicitly."""
    result = set()
    for spec in specs:
        for s in spec.traverse():
            result.add(s)
    return list(result)


def concrete_specs_from_cli_or_file(args):
    tty.msg("Concretizing input specs")
    with spack.concretize.disable_compiler_existence_check():
        if args.specs:
            specs = spack.cmd.parse_specs(args.specs, concretize=True)
            if not specs:
                raise SpackError("unable to parse specs from command line")

        if args.file:
            specs = specs_from_text_file(args.file, concretize=True)
            if not specs:
                raise SpackError("unable to parse specs from file '{}'".format(args.file))
    return specs


def not_excluded_fn(args):
    """Return a predicate that evaluate to True if a spec was not explicitly
    excluded by the user.
    """
    exclude_specs = []
    if args.exclude_file:
        exclude_specs.extend(specs_from_text_file(args.exclude_file, concretize=False))
    if args.exclude_specs:
        exclude_specs.extend(spack.cmd.parse_specs(str(args.exclude_specs).split()))

    def not_excluded(x):
        return not any(x.satisfies(y) for y in exclude_specs)

    return not_excluded


def concrete_specs_from_environment(selection_fn):
    env = ev.active_environment()
    assert env, "an active environment is required"
    mirror_specs = env.all_specs()
    mirror_specs = filter_externals(mirror_specs)
    mirror_specs, _ = lang.stable_partition(mirror_specs, predicate_fn=selection_fn)
    return mirror_specs


def all_specs_with_all_versions(selection_fn):
    specs = [spack.spec.Spec(n) for n in spack.repo.all_package_names()]
    mirror_specs = spack.mirror.get_all_versions(specs)
    mirror_specs.sort(key=lambda s: (s.name, s.version))
    mirror_specs, _ = lang.stable_partition(mirror_specs, predicate_fn=selection_fn)
    return mirror_specs


def versions_per_spec(args):
    """Return how many versions should be mirrored per spec."""
    if not args.versions_per_spec:
        num_versions = 1
    elif args.versions_per_spec == "all":
        num_versions = "all"
    else:
        try:
            num_versions = int(args.versions_per_spec)
        except ValueError:
            raise SpackError(
                "'--versions-per-spec' must be a number or 'all',"
                " got '{0}'".format(args.versions_per_spec)
            )
    return num_versions


def create_mirror_for_individual_specs(mirror_specs, path, skip_unstable_versions):
    present, mirrored, error = spack.mirror.create(path, mirror_specs, skip_unstable_versions)
    tty.msg("Summary for mirror in {}".format(path))
    process_mirror_stats(present, mirrored, error)


def process_mirror_stats(present, mirrored, error):
    p, m, e = len(present), len(mirrored), len(error)
    tty.msg(
        "Archive stats:",
        "  %-4d already present" % p,
        "  %-4d added" % m,
        "  %-4d failed to fetch." % e,
    )
    if error:
        tty.error("Failed downloads:")
        colify.colify(s.cformat("{name}{@version}") for s in error)
        sys.exit(1)


def mirror_create(args):
    """Create a directory to be used as a spack mirror, and fill it with
    package archives.
    """
    if args.specs and args.all:
        raise SpackError(
            "cannot specify specs on command line if you chose to mirror all specs with '--all'"
        )

    if args.file and args.all:
        raise SpackError(
            "cannot specify specs with a file if you chose to mirror all specs with '--all'"
        )

    if args.file and args.specs:
        raise SpackError("cannot specify specs with a file AND on command line")

    if not args.specs and not args.file and not args.all:
        raise SpackError(
            "no packages were specified.",
            "To mirror all packages, use the '--all' option "
            "(this will require significant time and space).",
        )

    if args.versions_per_spec and args.all:
        raise SpackError(
            "cannot specify '--versions_per-spec' and '--all' together",
            "The option '--all' already implies mirroring all versions for each package.",
        )

    # When no directory is provided, the source dir is used
    path = args.directory or spack.caches.fetch_cache_location()

    if args.all and not ev.active_environment():
        create_mirror_for_all_specs(
            path=path,
            skip_unstable_versions=args.skip_unstable_versions,
            selection_fn=not_excluded_fn(args),
        )
        return

    if args.all and ev.active_environment():
        create_mirror_for_all_specs_inside_environment(
            path=path,
            skip_unstable_versions=args.skip_unstable_versions,
            selection_fn=not_excluded_fn(args),
        )
        return

    mirror_specs = concrete_specs_from_user(args)
    create_mirror_for_individual_specs(
        mirror_specs, path=path, skip_unstable_versions=args.skip_unstable_versions
    )


def create_mirror_for_all_specs(path, skip_unstable_versions, selection_fn):
    mirror_specs = all_specs_with_all_versions(selection_fn=selection_fn)
    mirror_cache, mirror_stats = spack.mirror.mirror_cache_and_stats(
        path, skip_unstable_versions=skip_unstable_versions
    )
    for candidate in mirror_specs:
        pkg_cls = spack.repo.path.get_pkg_class(candidate.name)
        pkg_obj = pkg_cls(spack.spec.Spec(candidate))
        mirror_stats.next_spec(pkg_obj.spec)
        spack.mirror.create_mirror_from_package_object(pkg_obj, mirror_cache, mirror_stats)
    process_mirror_stats(*mirror_stats.stats())


def create_mirror_for_all_specs_inside_environment(path, skip_unstable_versions, selection_fn):
    mirror_specs = concrete_specs_from_environment(selection_fn=selection_fn)
    create_mirror_for_individual_specs(
        mirror_specs, path=path, skip_unstable_versions=skip_unstable_versions
    )


def mirror_destroy(args):
    """Given a url, recursively delete everything under it."""
    mirror_url = None

    if args.mirror_name:
        result = spack.mirror.MirrorCollection().lookup(args.mirror_name)
        mirror_url = result.push_url
    elif args.mirror_url:
        mirror_url = args.mirror_url

    web_util.remove_url(mirror_url, recursive=True)


def mirror(parser, args):
    action = {
        "create": mirror_create,
        "destroy": mirror_destroy,
        "add": mirror_add,
        "remove": mirror_remove,
        "rm": mirror_remove,
        "set-url": mirror_set_url,
        "list": mirror_list,
    }

    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    if args.deprecated:
        spack.config.set("config:deprecated", True, scope="command_line")

    action[args.mirror_command](args)
