# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from six import StringIO

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments
import spack.spec

description = 'concretize an environment and write a lockfile'
section = "environments"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true',
        help="Re-concretize even if already concretized.")
    subparser.add_argument(
        '--test', default=None,
        choices=['root', 'all'],
        help="""Concretize with test dependencies. When 'root' is chosen, test
dependencies are only added for the environment's root specs. When 'all' is
chosen, test dependencies are enabled for all packages in the environment.""")

    spack.cmd.common.arguments.add_concretizer_args(subparser)


def subtract_spec_constraints(lhs, rhs):
    # Subtraction in the set of constraints (not in the solution space)
    # returns an abstract spec:
    # Spec(zlib+pic%gcc) - Spec(zlib~pic%gcc) = Spec(zlib+pic).
    # Spec(zlib+pic)     - Spec(zlib+pic)     = Spec()

    # For now require concrete specs
    assert lhs.concrete and rhs.concrete and lhs.name == rhs.name
    out = spack.spec.Spec()
    out.name = lhs.name
    out.versions = None if lhs.versions == rhs.versions else lhs.versions.copy()
    out.architecture = (None if lhs.architecture == rhs.architecture
                        else lhs.architecture.copy())
    out.compiler = None if lhs.compiler == rhs.compiler else lhs.compiler.copy()
    out.compiler_flags = (None if lhs.compiler_flags == rhs.compiler_flags
                          else lhs.compiler_flags.copy())
    out.variants = lhs.variants.copy()
    for key in rhs.variants:
        if key in out.variants and out.variants[key] == rhs.variants[key]:
            del out.variants[key]
    return out


def get_sorted_specs_of_environment(env):
    roots = [env.specs_by_hash[key].copy(deps=True) for key in env.specs_by_hash]
    roots.sort()
    return roots


def empty_spec(s):
    return (not s.versions and not s.architecture and not s.compiler and
            not s.compiler_flags and not s.variants)


def print_deletion(spec, depth, io):
    if depth:
        io.write("    " * depth)
        io.write('^')
    io.write(spec.cformat(r'{name}{@version}{%compiler}{variants}{arch=architecture}'))
    io.write(" => dropped")
    io.write('\n')


def print_insertion(spec, depth, io):
    if depth:
        io.write("    " * depth)
        io.write('^')
    io.write(spec.cformat(r'{name}{@version}{%compiler}{variants}{arch=architecture}'))
    io.write(" => new")
    io.write('\n')


def print_equal(name, depth, io):
    if depth:
        io.write("    " * depth)
        io.write('^')
    io.write(name)
    io.write('\n')


def print_mutation(lhs_min_rhs, rhs_min_lhs, depth, io):
    if depth:
        io.write("    " * depth)
        io.write('^')
    io.write(lhs_min_rhs.name)
    io.write('{')
    fmt = r'{@version}{%compiler}{variants}{arch=architecture}'
    io.write(lhs_min_rhs.cformat(fmt))
    io.write(" => ")
    io.write(rhs_min_lhs.cformat(fmt))
    io.write("}\n")


def handle_stack(stack, depth, io):
    n = len(stack)
    for i in range(n):
        print_equal(stack[i], depth - n + i, io)
    stack[:] = []


def recursive_diff(before, after, visited, stack, depth=0, io=sys.stdout):
    lhs_specs_iterator, rhs_specs_iterator = iter(before), iter(after)
    lhs_spec, rhs_spec = next(lhs_specs_iterator, None), next(rhs_specs_iterator, None)

    changed = False

    while lhs_spec or rhs_spec:
        # Skip over what we've seen before
        if id(lhs_spec) in visited:
            lhs_spec = next(lhs_specs_iterator, None)
            continue

        if id(rhs_spec) in visited:
            rhs_spec = next(rhs_specs_iterator, None)
            continue

        # Handle hitting the end of the lists
        if rhs_spec is None:
            handle_stack(stack, depth, io)
            print_deletion(lhs_spec, depth=depth, io=io)
            visited.add(id(lhs_spec))
            changed = True
            lhs_spec = next(lhs_specs_iterator, None)
            continue

        if lhs_spec is None:
            handle_stack(stack, depth, io)
            print_insertion(rhs_spec, depth=depth, io=io)
            visited.add(id(rhs_spec))
            changed = True
            rhs_spec = next(rhs_specs_iterator, None)
            continue

        # Handle end of package groups
        if lhs_spec.name < rhs_spec.name:
            handle_stack(stack, depth, io)
            print_deletion(lhs_spec, depth=depth, io=io)
            visited.add(id(lhs_spec))
            changed = True
            lhs_spec = next(lhs_specs_iterator, None)
            continue

        if lhs_spec.name > rhs_spec.name:
            handle_stack(stack, depth, io)
            print_insertion(rhs_spec, depth=depth, io=io)
            visited.add(id(rhs_spec))
            changed = True
            rhs_spec = next(rhs_specs_iterator, None)
            continue

        lhs_min_rhs = subtract_spec_constraints(lhs_spec, rhs_spec)
        rhs_min_lhs = subtract_spec_constraints(rhs_spec, lhs_spec)

        # If this spec is not mutated, remember it, maybe its children are.
        if empty_spec(lhs_min_rhs) and empty_spec(rhs_min_lhs):
            stack.append(lhs_spec.name)
        else:
            handle_stack(stack, depth, io)
            print_mutation(lhs_min_rhs, rhs_min_lhs, depth, io)
            changed = True

        visited.add(id(lhs_spec))
        visited.add(id(rhs_spec))

        deps_changed = recursive_diff(
            lhs_spec.dependencies(), rhs_spec.dependencies(), visited,
            stack, depth + 1, io)

        # Pop if list is not flushed already
        if stack:
            stack.pop()

        changed |= deps_changed

        lhs_spec = next(lhs_specs_iterator, None)
        rhs_spec = next(rhs_specs_iterator, None)

    return changed


def concretize(parser, args):
    env = spack.cmd.require_active_env(cmd_name='concretize')

    if args.test == 'all':
        tests = True
    elif args.test == 'root':
        tests = [spec.name for spec in env.user_specs]
    else:
        tests = False

    with env.write_transaction():
        before = get_sorted_specs_of_environment(env)
        env.concretize(force=args.force, tests=tests)
        after = get_sorted_specs_of_environment(env)

        out = StringIO()
        if recursive_diff(before, after, set(), [], io=out):
            sys.stdout.write(out.getvalue())

            # if we're about to overwrite changes, prompt first
            if sys.stdin.isatty() and before:
                if not tty.get_yes_or_no('Persist changes?', default=True):
                    return

        env.write()
