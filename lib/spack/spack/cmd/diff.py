# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import argparse
import os
import sys

import llnl.util.tty as tty
from llnl.util.tty.color import cprint, get_color_when

import spack.cmd
import spack.environment as ev
import spack.solver.asp as asp
import spack.spec
import spack.util.environment
import spack.util.spack_json as sjson

description = "compare two specs or lock files"
section = "basic"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        'args',
        nargs=argparse.REMAINDER, help='two specs or environment lock files')

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
        '-a', '--attribute',
        action='append',
        help="select the attributes to show (defaults to all)"
    )


def compare_specs(a, b, to_string=False, color=None):
    """
    Generate a comparison, including diffs (for each side) and an intersection.

    We can either print the result to the console, or parse
    into a json object for the user to save. We return an object that shows
    the differences, intersection, and names for a pair of specs a and b.

    Arguments:
        a (spack.spec.Spec or list): the first spec to compare
        b (spack.spec.Spec or list): the second spec to compare
        to_string (bool): return an object that can be json dumped
    """

    # Prepare a solver setup to parse differences
    setup = asp.SpackSolverSetup()

    a = [a] if isinstance(a, spack.spec.Spec) else a
    b = [b] if isinstance(b, spack.spec.Spec) else b

    a_facts, b_facts = [], []
    for s in a:
        a_facts.extend(
            setup.spec_clauses(s, body=True, transitive=True, expand_hashes=True))
    for s in b:
        b_facts.extend(
            setup.spec_clauses(s, body=True, transitive=True, expand_hashes=True))

    a_facts = set(a_facts)
    b_facts = set(b_facts)

    # We want to present them to the user as simple key: values
    intersect = sorted(a_facts.intersection(b_facts))
    spec1_not_spec2 = sorted(a_facts.difference(b_facts))
    spec2_not_spec1 = sorted(b_facts.difference(a_facts))

    # We want to show what is the same, and then difference for each
    return {
        "intersect": flatten(intersect) if to_string else intersect,
        "a_not_b": flatten(spec1_not_spec2) if to_string else spec1_not_spec2,
        "b_not_a": flatten(spec2_not_spec1) if to_string else spec2_not_spec1,
    }


def flatten(functions):
    """
    Given a list of ASP functions, convert into a list of key: value tuples.

    We are squashing whatever is after the first index into one string for
    easier parsing in the interface
    """
    updated = []
    for fun in functions:
        updated.append([fun.name, " ".join(str(a) for a in fun.args)])
    return updated


def print_difference(c, attributes="all", out=None):
    """
    Print the difference.

    Given a diffset for A and a diffset for B, print red/green diffs to show
    the differences.
    """
    # Default to standard out unless another stream is provided
    out = out or sys.stdout

    A = c['b_not_a']
    B = c['a_not_b']

    # Cut out early if we don't have any differences!
    if not A and not B:
        print("No differences\n")
        return

    def group_by_type(diffset):
        grouped = {}
        for entry in diffset:
            if entry[0] not in grouped:
                grouped[entry[0]] = []
            grouped[entry[0]].append(entry[1])

        # Sort by second value to make comparison slightly closer
        for key, values in grouped.items():
            values.sort()
        return grouped

    A = group_by_type(A)
    B = group_by_type(B)

    # print a directionally relevant diff
    keys = list(A) + list(B)

    category = None
    for key in keys:
        if "all" not in attributes and key not in attributes:
            continue

        # Write the attribute, B is subtraction A is addition
        subtraction = [] if key not in B else B[key]
        addition = [] if key not in A else A[key]

        # Bail out early if we don't have any entries
        if not subtraction and not addition:
            continue

        # If we have a new category, create a new section
        if category != key:
            category = key

            # print category in bold, colorized
            cprint("@*b{@@ %s @@}" % category)  # bold blue

        # Print subtractions first
        while subtraction:
            cprint("@R{-  %s}" % subtraction.pop(0))  # bright red
            if addition:
                cprint("@G{+  %s}" % addition.pop(0))  # bright green

        # Any additions left?
        while addition:
            cprint("@G{+  %s}" % addition.pop(0))


def print_header(a, b):
    cprint("@R{--- %s}" % a)
    cprint("@G{+++ %s}" % b)


def _is_environment_comparison(args):
    is_lock = lambda p: os.path.isfile(p) and '.lock' in os.path.basename(p)
    return len(args) == 2 and is_lock(args[0]) and is_lock(args[1])


def diff(parser, args):
    color = False if args.dump_json else get_color_when()

    # Try to read environment lock files
    if _is_environment_comparison(args.args):
        mode = 'env'
        env_a = ev.Environment('.', init_file=args.args[0], with_view=False)
        env_b = ev.Environment('.', init_file=args.args[1], with_view=False)
        specs = [
            [s for _, s in env_a.concretized_specs()],
            [s for _, s in env_b.concretized_specs()]
        ]
    else:
        mode = 'specs'
        env = ev.active_environment()
        specs = [spack.cmd.disambiguate_spec(spec, env, first=args.load_first)
                 for spec in spack.cmd.parse_specs(args.args)]
        # note that len(args.args) != len(specs) necessarily.
        if len(specs) != 2:
            tty.die("You must provide two specs or two environment lock files to diff.")

    # Calculate the comparison (c)
    c = compare_specs(specs[0], specs[1], to_string=True, color=color)

    # Default to all attributes
    attributes = args.attribute or ["all"]

    # JSON output
    if args.dump_json:
        print(sjson.dump(c))
        return

    # Text output
    if mode == 'env':
        print_header(
            os.path.abspath(os.path.realpath(args.args[0])),
            os.path.abspath(os.path.realpath(args.args[1])))

    elif mode == 'specs':
        fmt = "{name}{@version}{/hash}"
        print_header(
            specs[0].format(fmt, color=color),
            specs[1].format(fmt, color=color))

    print_difference(c, attributes)
