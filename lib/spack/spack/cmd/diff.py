# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.environment

import llnl.util.tty as tty
from llnl.util.tty.colify import colify
import spack.util.spack_json as sjson
import operator
import sys

description = "compare two specs"
section = "extensions"
level = "short"


def setup_parser(subparser):
    """Parser is only constructed so that this prints a nice help
       message with -h. """
    arguments.add_common_arguments(
        subparser, ['specs'])

    subparser.add_argument(
        '--json',
        action='store_true',
        default=False,
        dest='dump_json',
        help="Dump json output instead of pretty printing."
    )
    subparser.add_argument(
        '--first',
        action='store_true',
        default=False,
        dest='load_first',
        help="load the first match if multiple packages match the spec"
    )
    subparser.add_argument(
        '--diff-type',
        default='all',
        dest='diff_type',
        choices=[
            'all', 'version', 'concrete', 'node', 'node_compiler_set',
            'node_compiler_version_set', 'node_os_set', 'node_platform_set',
            'node_target_set', 'variant_set'
        ],
        help="select the diff type (defaults to all)"
    )


def bold(string):
    """Make a header string bold so we can easily see it
    """
    return "\033[1m" + string + "\033[0m"


def compare_specs(a, b, a_name, b_name, to_string=False):
    """Generate a comparison, including diffs (for each side) along with
    an intersection. We can either print the result to the console, or parse
    into a json object for the user to save. We return an object that shows
    the differences, intersection, and names for a pair of specs a and b.

    Arguments:
        a (spec): the first spec to compare
        b (spec): the second spec to compare
        a_name (str): the name of spec a
        b_name (str): the name of spec b
        to_string (bool): return an object that can be json dumped
    """
    from spack.solver.asp import SpackSolverSetup

    # Prepare a solver setup to parse differences
    setup = SpackSolverSetup()

    a_facts = set(to_tuple(t) for t in setup.spec_clauses(a))
    b_facts = set(to_tuple(t) for t in setup.spec_clauses(b))

    # We want to present them to the user as simple key: values
    intersect = list(a_facts.intersection(b_facts))
    spec1_not_spec2 = list(a_facts.difference(b_facts))
    spec2_not_spec1 = list(b_facts.difference(a_facts))

    # We want to show what is the same, and then difference for each
    return {
        "intersect": flatten(intersect) if to_string else intersect,
        "a_not_b": flatten(spec1_not_spec2) if to_string else spec1_not_spec2,
        "b_not_a": flatten(spec2_not_spec1) if to_string else spec2_not_spec1,
        "a_name": a_name,
        "b_name": b_name,
    }


def to_tuple(asp_function):
    """Prepare tuples of objects. If we need to save to json, convert to strings
    See https://gist.github.com/tgamblin/83eba3c6d27f90d9fa3afebfc049ceaf
    """
    args = []
    for arg in asp_function.args:
        if isinstance(arg, str):
            args.append(arg)
            continue
        args.append("%s(%s)" % (type(arg).__name__, str(arg)))
    return tuple([asp_function.name] + args)


def flatten(tuple_list):
    """Given a list of tuples, convert into a list of key: value tuples (so
    we are squashing whatever is after the first index into one string for
    easier parsing in the interface
    """
    updated = []
    for item in tuple_list:
        updated.append([item[0], " ".join(item[1:])])
    return updated


def print_difference(diffset, diff_type="all"):
    """Given a diffset and a user preference (e.g., print versions or print all)
    print a tabular, organized version of the diffset
    """
    # Cut out early if we don't have any differences!
    if not diffset:
        print("No differences\n")
        return

    # Sort by name so they are grouped together
    sorted_diffset = sorted(diffset, key=operator.itemgetter(0))

    # Keep rows to print
    rows = []

    # Always print a new category
    category = None
    for entry in sorted_diffset:
        if diff_type == "all" or diff_type == entry[0]:

            # If we have a new category, create a new section
            if category != entry[0]:
                category = entry[0]
                rows.append(bold(category.upper()))
            rows.append(entry[1])

    colify(rows, indent=0, output=sys.stdout)


def diff(parser, args):
    env = ev.get_env(args, 'diff')

    if len(args.specs) != 2:
        tty.die("You must provide two specs to diff.")

    specs = [spack.cmd.disambiguate_spec(spec, env, first=args.load_first)
             for spec in spack.cmd.parse_specs(args.specs)]

    # Calculate the comparison (c)
    c = compare_specs(specs[0], specs[1], args.specs[0], args.specs[1], to_string=True)

    if args.dump_json:
        print(sjson.dump(c))
    else:
        # For each spec, print the differences wanted by the user
        tty.info("diff(%s, %s)" % (c['a_name'], c['b_name']))
        print_difference(c['a_not_b'], args.diff_type)
        tty.info("diff(%s, %s)" % (c['b_name'], c['a_name']))
        print_difference(c['b_not_a'], args.diff_type)
