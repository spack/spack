# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Implementation details of the ``spack module`` command."""

import collections
import os
import shutil
import sys
from typing import Dict, List

import spack.cmd
import spack.config
import spack.error
import spack.modules
import spack.modules.common
import spack.modules.error
import spack.repo
import spack.spec
import spack.store
from spack.cmd import MultipleSpecsMatch, NoSpecMatches
from spack.cmd.common import arguments
from spack.util import filesystem, tty
from spack.util.lang import dedupe, stable_partition
from spack.util.tty import color

description = "manipulate module files"
section = "environment"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "-n",
        "--name",
        action="store",
        dest="module_set_name",
        default="default",
        help="named module set to use from modules configuration",
    )
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="subparser_name")

    refresh_parser = sp.add_parser("refresh", help="regenerate module files")
    refresh_parser.add_argument(
        "--delete-tree", help="delete the module file tree before refresh", action="store_true"
    )
    refresh_parser.add_argument(
        "--upstream-modules",
        help="generate modules for packages installed upstream",
        action="store_true",
    )
    arguments.add_common_arguments(refresh_parser, ["constraint", "yes_to_all"])

    find_parser = sp.add_parser("find", help="find module files for packages")
    find_parser.add_argument(
        "--full-path", help="display full path to module file", action="store_true"
    )
    arguments.add_common_arguments(find_parser, ["constraint", "recurse_dependencies"])

    rm_parser = sp.add_parser("rm", help="remove module files")
    arguments.add_common_arguments(rm_parser, ["constraint", "yes_to_all"])

    loads_parser = sp.add_parser(
        "loads", help="prompt the list of modules associated with a constraint"
    )
    add_loads_arguments(loads_parser)
    arguments.add_common_arguments(loads_parser, ["constraint"])

    return sp


def add_loads_arguments(subparser):
    subparser.add_argument(
        "--input-only",
        action="store_false",
        dest="shell",
        help="generate input for module command (instead of a shell script)",
    )
    subparser.add_argument(
        "-p",
        "--prefix",
        dest="prefix",
        default="",
        help="prepend to module names when issuing module load commands",
    )
    subparser.add_argument(
        "-x",
        "--exclude",
        dest="exclude",
        action="append",
        default=[],
        help="exclude package from output; may be specified multiple times",
    )
    arguments.add_common_arguments(subparser, ["recurse_dependencies"])


def one_spec_or_raise(specs):
    """Ensures exactly one spec has been selected, or raises the appropriate
    exception.
    """
    # Ensure a single spec matches the constraint
    if len(specs) == 0:
        raise NoSpecMatches()
    if len(specs) > 1:
        raise MultipleSpecsMatch()

    # Get the spec and module type
    return specs[0]


def check_module_set_name(name):
    modules = spack.config.CONFIG.get("modules")
    if name != "prefix_inspections" and name in modules:
        return

    names = [k for k in modules if k != "prefix_inspections"]

    if not names:
        raise spack.error.ConfigError(
            f"Module set configuration is missing. Cannot use module set '{name}'"
        )

    pretty_names = "', '".join(names)

    raise spack.error.ConfigError(
        f"Cannot use invalid module set '{name}'.",
        f"Valid module set names are: '{pretty_names}'.",
    )


_missing_modules_warning = (
    "Modules have been omitted for one or more specs, either"
    " because they were excluded or because the spec is"
    " associated with a package that is installed upstream and"
    " that installation has not generated a module file. Rerun"
    " this command with debug output enabled for more details."
)


def loads(module_type, specs, args, out=None):
    """Prompt the list of modules associated with a list of specs"""
    check_module_set_name(args.module_set_name)
    out = sys.stdout if out is None else out

    # Get a comprehensive list of specs
    if args.recurse_dependencies:
        specs_from_user_constraint = specs[:]
        specs = []
        # FIXME : during module file creation nodes seem to be visited
        # FIXME : multiple times even if cover='nodes' is given. This
        # FIXME : work around permits to get a unique list of spec anyhow.
        # FIXME : (same problem as in spack/modules.py)
        seen = set()
        seen_add = seen.add
        for spec in specs_from_user_constraint:
            specs.extend(
                [
                    item
                    for item in spec.traverse(order="post", cover="nodes")
                    if not (item in seen or seen_add(item))
                ]
            )

    cache: spack.modules.common.ModuleConfigurationCache = {}
    modules = [
        (
            spec,
            spack.modules.get_module(
                module_type,
                spec,
                get_full_path=False,
                module_set_name=args.module_set_name,
                required=False,
                cache=cache,
            ),
        )
        for spec in specs
    ]

    # Installations folded into one module file cannot be loaded together: only the one the
    # module file lists first gets a live load line
    module_cls = spack.modules.module_types[module_type]
    file_of: Dict[spack.spec.Spec, str] = {}
    first_in_file: Dict[str, spack.spec.Spec] = {}
    for spec, mod in modules:
        if not mod:
            continue
        writer = module_cls.from_spec(spec, args.module_set_name, cache=cache)
        if not writer.has_other_installations:
            continue
        filename = writer.layout.filename
        file_of[spec] = filename
        listed = writer.conf.specs_in_file
        first = first_in_file.setdefault(filename, spec)
        if listed.index(spec) < listed.index(first):
            first_in_file[filename] = spec
    shares_file_with = {
        spec: first_in_file[filename]
        for spec, filename in file_of.items()
        if spec != first_in_file[filename]
    }

    module_commands = {"tcl": "module load ", "lmod": "module load "}

    d = {"command": "" if not args.shell else module_commands[module_type], "prefix": args.prefix}

    exclude_set = set(args.exclude)
    load_template = "{comment}{exclude}{command}{prefix}{name}"
    for spec, mod in modules:
        if not mod:
            module_output_for_spec = "## excluded or missing from upstream: {0}".format(
                spec.format()
            )
        else:
            d["exclude"] = "## " if spec.name in exclude_set else ""
            d["comment"] = "" if not args.shell else "# {0}\n".format(spec.format())
            if spec in shares_file_with:
                d["exclude"] = "## "
                if args.shell:
                    d["comment"] += "# shares its module file with {0}\n".format(
                        shares_file_with[spec].format()
                    )
            d["name"] = mod
            module_output_for_spec = load_template.format(**d)
        out.write(module_output_for_spec)
        out.write("\n")

    if not all(mod for _, mod in modules):
        tty.warn(_missing_modules_warning)
    if shares_file_with:
        tty.warn(
            "Installations sharing a module file cannot be loaded together: only the first load"
            " line of each module file is left active"
        )


def fold_into_one_file(writers) -> bool:
    """Whether the module file of the first writer folds the installations of all of them."""
    specs_in_file = writers[0].conf.specs_in_file
    return all(x.spec in specs_in_file for x in writers)


def shared_module_name(module_type, specs, args, cache):
    """Returns the name, or path with ``--full-path``, of the module file folding every
    installation of ``specs``, or None when they do not all share one."""
    module_cls = spack.modules.module_types[module_type]
    writers = [module_cls.from_spec(spec, args.module_set_name, cache=cache) for spec in specs]
    first = writers[0]
    if not fold_into_one_file(writers) or not first.has_installation:
        return None
    return first.layout.filename if args.full_path else first.layout.name


def find(module_type, specs, args):
    """Retrieve paths or use names of module files"""
    check_module_set_name(args.module_set_name)

    cache: spack.modules.common.ModuleConfigurationCache = {}
    if len(specs) > 1:
        # An installation excluded from module files has no module to find, so it does not
        # make the constraint ambiguous
        module_cls = spack.modules.module_types[module_type]
        included = [
            spec
            for spec in specs
            if not module_cls.from_spec(spec, args.module_set_name, cache=cache).conf.excluded
        ]
        specs = included or specs

    if len(specs) > 1 and not args.recurse_dependencies:
        # Installations folded into one module file are found by the name of the file, which
        # selects none of them in particular
        module_name = shared_module_name(module_type, specs, args, cache)
        if module_name:
            print(module_name)
            return

    single_spec = one_spec_or_raise(specs)

    if args.recurse_dependencies:
        dependency_specs_to_retrieve = list(
            single_spec.traverse(root=False, order="post", cover="nodes", deptype=("link", "run"))
        )
    else:
        dependency_specs_to_retrieve = []

    try:
        modules = [
            spack.modules.get_module(
                module_type,
                spec,
                args.full_path,
                module_set_name=args.module_set_name,
                required=False,
                cache=cache,
            )
            for spec in dependency_specs_to_retrieve
        ]

        modules.append(
            spack.modules.get_module(
                module_type,
                single_spec,
                args.full_path,
                module_set_name=args.module_set_name,
                required=True,
                cache=cache,
            )
        )
    except spack.modules.error.ModuleNotFoundError as e:
        tty.die(e.message)

    if not all(modules):
        tty.warn(_missing_modules_warning)
    modules = [x for x in modules if x]
    print(" ".join(modules))


def rm(module_type, specs, args):
    """Deletes the module files associated with every spec in specs, for every
    module type in module types.
    """
    check_module_set_name(args.module_set_name)

    module_cls = spack.modules.module_types[module_type]
    cache: spack.modules.common.ModuleConfigurationCache = {}

    # Installations sharing a module file are removed from it together: the file is deleted
    # when none remains, written again for the others otherwise
    file2specs: Dict[str, List[spack.spec.Spec]] = collections.defaultdict(list)
    for spec in specs:
        writer = module_cls.from_spec(spec, args.module_set_name, cache=cache)
        if writer.has_installation:
            file2specs[writer.layout.filename].append(spec)

    if not file2specs:
        tty.die("No module file matches your query")

    writers = [
        module_cls.from_spec(
            group[0], args.module_set_name, removed_specs=tuple(group), cache=cache
        )
        for group in file2specs.values()
    ]
    rewritten, deleted = stable_partition(writers, lambda x: x.has_other_installations)

    # Ask for confirmation
    if not args.yes_to_all:
        if deleted:
            msg = "You are about to remove {0} module files for:\n"
            tty.msg(msg.format(module_type))
            spack.cmd.display_specs([s for x in deleted for s in x.conf.removed_specs], long=True)
            print("")
        if rewritten:
            msg = "You are about to remove the following installations from {0} module files"
            msg += " shared with other installations:\n"
            tty.msg(msg.format(module_type))
            spack.cmd.display_specs(
                [s for x in rewritten for s in x.conf.removed_specs], long=True
            )
            print("")
            tty.msg("These module files are written again for the installations they keep:\n")
            spack.cmd.display_specs(
                [s for x in rewritten for s in x.conf.specs_in_file], long=True
            )
            print("")
        answer = tty.get_yes_or_no("Do you want to proceed?")
        if not answer:
            tty.die("Will not remove any module files")

    for x in writers:
        x.remove_installation()


def refresh(module_type, specs, args):
    """Regenerates the module files for every spec in specs and every module
    type in module types.
    """
    check_module_set_name(args.module_set_name)

    # Prompt a message to the user about what is going to change
    if not specs:
        tty.msg("No package matches your query")
        return

    if not args.upstream_modules:
        specs = [s for s in specs if not spack.store.STORE.db.installed_upstream(s)]

    cls = spack.modules.module_types[module_type]
    cache: spack.modules.common.ModuleConfigurationCache = {}

    # Skip unknown packages.
    writers = [
        cls.from_spec(spec, args.module_set_name, cache=cache)
        for spec in specs
        if spack.repo.PATH.exists(spec.name)
    ]

    # Filter excluded packages early
    writers = [x for x in writers if not x.conf.excluded]

    if not args.yes_to_all:
        msg = "You are about to regenerate {types} module files for:\n"
        tty.msg(msg.format(types=module_type))
        spack.cmd.display_specs(specs, long=True)
        print("")
        # A module file folding several installations is written for all of them
        selected = {s.dag_hash() for s in specs}
        folded = [
            s for x in writers for s in x.conf.other_specs_in_file if s.dag_hash() not in selected
        ]
        folded = list(dedupe(folded))
        if folded:
            msg = "The following installations share a module file with them and are written"
            msg += " again too:\n"
            tty.msg(msg)
            spack.cmd.display_specs(folded, long=True)
            print("")
        answer = tty.get_yes_or_no("Do you want to proceed?")
        if not answer:
            tty.die("Module file regeneration aborted.")

    # Detect name clashes in module files: several writers may share a module file only
    # when it folds all their installations
    file2writer = collections.defaultdict(list)
    for item in writers:
        file2writer[item.layout.filename].append(item)

    clashes = {f: w for f, w in file2writer.items() if len(w) > 1 and not fold_into_one_file(w)}
    if clashes:
        spec_fmt_str = "{name}@={version}%{compiler}/{hash:7} {variants} arch={arch}"
        message = "Name clashes detected in module files:\n"
        for filename, writer_list in clashes.items():
            message += "\nfile: {0}\n".format(filename)
            for x in writer_list:
                message += "spec: {0}\n".format(x.spec.format(spec_fmt_str))
            if len({x.spec.version for x in writer_list}) > 1:
                message += (
                    "installations of different versions cannot share a module file, "
                    "add {version} to the projection\n"
                )
        tty.error(message)
        tty.error("Operation aborted")
        raise SystemExit(1)

    if len(writers) == 0:
        msg = "Nothing to be done for {0} module files."
        tty.msg(msg.format(module_type))
        return
    # If we arrived here we have at least one writer
    module_type_root = writers[0].layout.dirname()

    # Proceed regenerating module files
    tty.msg("Regenerating {name} module files".format(name=module_type))
    if os.path.isdir(module_type_root) and args.delete_tree:
        shutil.rmtree(module_type_root, ignore_errors=False)
    filesystem.mkdirp(module_type_root)

    # Dump module index after potentially removing module tree
    spack.modules.common.generate_module_index(
        module_type_root, writers, overwrite=args.delete_tree
    )
    errors = []
    # A module file folding several installations is written once, from the first of them
    for x in (writer_list[0] for writer_list in file2writer.values()):
        try:
            x.write(overwrite=True)
        except spack.error.SpackError as e:
            msg = f"{x.layout.filename}: {e.message}"
            errors.append(msg)
        except Exception as e:
            msg = f"{x.layout.filename}: {str(e)}"
            errors.append(msg)

    if errors:
        errors.insert(0, color.colorize("@*{some module files could not be written}"))
        tty.warn("\n".join(errors))


#: Dictionary populated with the list of sub-commands.
#: Each sub-command must be callable and accept 3 arguments:
#:
#: - module_type: the type of module it refers to
#: - specs : the list of specs to be processed
#: - args : namespace containing the parsed command line arguments
callbacks = {"refresh": refresh, "rm": rm, "find": find, "loads": loads}


def modules_cmd(parser, args, module_type, callbacks=callbacks):
    # Qualifiers to be used when querying the db for specs
    constraint_qualifiers = {
        "refresh": {
            "installed": True,
            "predicate_fn": lambda x: spack.repo.PATH.exists(x.spec.name),
        }
    }
    query_args = constraint_qualifiers.get(args.subparser_name, {})

    # Get the specs that match the query from the DB
    specs = args.specs(**query_args)

    try:
        callbacks[args.subparser_name](module_type, specs, args)

    except MultipleSpecsMatch:
        query = " ".join(str(s) for s in args.constraint_specs)
        msg = f"the constraint '{query}' matches multiple packages:\n"
        for s in specs:
            spec_fmt = (
                "{hash:7} {name}{@version}{compiler_flags}{variants}"
                "{ platform=architecture.platform}{ os=architecture.os}"
                "{ target=architecture.target}"
                "{%compiler}"
            )
            msg += "\t" + s.cformat(spec_fmt) + "\n"
        tty.die(msg, "In this context exactly *one* match is needed.")

    except NoSpecMatches:
        query = " ".join(str(s) for s in args.constraint_specs)
        msg = f"the constraint '{query}' matches no package."
        tty.die(msg, "In this context exactly *one* match is needed.")
