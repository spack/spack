# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.cmd

import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.environment
import spack.solver.asp as asp

import llnl.util.tty as tty
import llnl.util.tty.color as color
import spack.util.spack_json as sjson
import spack.cmd
import sys

description = "compare two specs"
section = "basic"
level = "long"


def setup_parser(subparser):
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


def compare_specs(a, b, to_string=False, colorful=True):
    """
    Generate a comparison, including diffs (for each side) and an intersection.

    We can either print the result to the console, or parse
    into a json object for the user to save. We return an object that shows
    the differences, intersection, and names for a pair of specs a and b.

    Arguments:
        a (spec): the first spec to compare
        b (spec): the second spec to compare
        a_name (str): the name of spec a
        b_name (str): the name of spec b
        to_string (bool): return an object that can be json dumped
        colorful (bool): do not format the names for the console
    """
    # Prepare a solver setup to parse differences
    setup = asp.SpackSolverSetup()

    a_facts = set(to_tuple(t) for t in setup.spec_clauses(a))
    b_facts = set(to_tuple(t) for t in setup.spec_clauses(b))

    # We want to present them to the user as simple key: values
    intersect = list(a_facts.intersection(b_facts))
    spec1_not_spec2 = list(a_facts.difference(b_facts))
    spec2_not_spec1 = list(b_facts.difference(a_facts))

    # Format the spec names to be colored
    fmt = "{name}{@version}{/hash:7}"
    a_name = a.format(fmt, color=color.get_color_when())
    b_name = a.format(fmt, color=color.get_color_when())

    # We want to show what is the same, and then difference for each
    return {
        "intersect": flatten(intersect) if to_string else intersect,
        "a_not_b": flatten(spec1_not_spec2) if to_string else spec1_not_spec2,
        "b_not_a": flatten(spec2_not_spec1) if to_string else spec2_not_spec1,
        "a_name": a_name if colorful else a.format("{name}{@version}{/hash:7}"),
        "b_name": b_name if colorful else b.format("{name}{@version}{/hash:7}")
    }


def to_tuple(asp_function):
    """
    Prepare tuples of objects.

    If we need to save to json, convert to strings
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
    """
    Given a list of tuples, convert into a list of key: value tuples.

    We are squashing whatever is after the first index into one string for
    easier parsing in the interface
    """
    updated = []
    for item in tuple_list:
        updated.append([item[0], " ".join(item[1:])])
    return updated


def print_difference(spec1, spec2):
    """Print a diff of the attributes.
    """
    atts1 = spec1.format(return_lookup=True)
    atts2 = spec2.format(return_lookup=True)

    # Assume we look for all attributes of the default format string
    # This is also in the correct order. See spack.spec default_format
    attrs = ['name', 'version', 'compiler.name', 'compiler.version',
             'compiler_flags', 'variants', 'architecture']

    # Our final string to print
    final = ""

    # Prefixes depend on variable name
    prefixes = {'version': "@", "compiler.name": '%', 'compiler.version': '@',
                'architecture': 'arch='}

    # Loop through attributes (changes from one to the next) and prepare
    # string that shows second as newer, first as older
    for attr in attrs:
        att1 = atts1.get(attr)
        att2 = atts2.get(attr)

        # Printing prefix
        prefix = "" if attr not in prefixes else prefixes[attr]

        # Case 1: it's in neither
        if not att1 and not att2:
            continue

        # Case 2: it's missing entirely in our first, this is new (GREEN)
        elif not att1 and att2:
            final += color.colorize("@G{%s%s}" % (prefix, att2))

        # Case 3: it's missing entirely in our second, not present first (RED)
        elif not att2 and att1:
            final += color.colorize("@-R{%s%s}" % (prefix, att1))

        # Case 4: both are defined and equal (keep as regular color)
        elif att1 == att2:
            final += "%s%s" % (prefix, att1)

        # Case 5: both are defined and different
        elif att1 != att2:
            # TODO: we could do another level of comparison here
            final += color.colorize("@-R{%s%s}@G{%s}" % (prefix, att1, att2))

    print(final)


def diff(parser, args):
    env = ev.get_env(args, 'diff')

    if len(args.specs) != 2:
        tty.die("You must provide two specs to diff.")

    specs = [spack.cmd.disambiguate_spec(spec, env, first=args.load_first)
             for spec in spack.cmd.parse_specs(args.specs)]

    # Calculate the comparison to dump as json
    if args.dump_json:
        c = compare_specs(specs[0], specs[1], to_string=True,
                          colorful=not args.dump_json)
        print(sjson.dump(c))

    # or print a colored diff
    else:

        # Cut out early if the specs are the same
        if specs[0] == specs[1]:
            tty.info("No differences.")
            sys.exit(0)

        print_difference(specs[0], specs[1])
