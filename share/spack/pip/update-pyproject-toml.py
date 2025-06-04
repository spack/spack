# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import re
import sys

import toml

""" When creating a pip package from a Spack distribution, the
structure changes from:

 - spack/pyproject.toml
 - spack/var/...
 - spack/lib/...

to

 - build-dir/pyproject.toml
 - build-dir/spack/var/...
 - build-dir/spack/lib/...

i.e., the pyproject.toml is moved up a level so it is peer to the
spack source distribution. This makes it so any paths that are
referenced in pyproject.toml are no longer correct. This script
updates pyproject.toml such that any path references (lib/spack/...)
or class references (spack.lib....) used for the pip package build are
correct.

For most paths, this is done automatically. For other values, this is
done on a case-by-case basis.  """


module_name = "update-pyproject-toml"


def eprint(*args, **kwargs):
    print(module_name + ":", *args, file=sys.stderr, **kwargs)


def update_value(fqn, value):
    """
    fqns (fully qualified names) are the name of the keys all the way
    to the TOML document root. This function returns a mutated value.
    """

    if fqn == ".project.scripts.spack":
        # Update the installable main module path
        new_val = "spack." + value
    elif re.match(r"^(lib|bin|var)/spack", value):
        # Update known valid paths that don't have a leading "./"
        new_val = "spack/" + value
    elif re.match(r"^\./(lib|bin|var)/spack", value):
        # Update all known valid paths that start with "./"
        new_val = "./spack/" + value[2:]
    elif fqn == ".tool.hatch.build.targets.wheel.include":
        # This fqn has a list of paths in the value, update each appropriately
        if value[0] == "/":
            new_val = "/spack" + value
        else:
            new_val = "/spack/" + value
    else:
        if verbosity >= 2:
            eprint("Did not change", fqn, "=", value)
        return value

    if verbosity >= 1:
        eprint("Old:", fqn, "=", value)
        eprint("New:", fqn, "=", new_val)
    return new_val


def should_delete(fqn):
    """
    Selectively clean certain fqns from pyproject.toml in cases where
    they are unneeded. This is currently not used, but problematic
    keys that make no sense to update should be placed here.

    Candidate fqns: .tools.[isort, black, mypy, coverage, ruff]
    """
    if fqn in []:
        return True
    return False


def descend(coll, fqn=""):
    """Given a collection, get down to fqns and string elements to
    determine modifications (including deletions).

    """
    to_delete = []

    try:
        # Try this as a dict-like type
        for k, v in coll.items():
            new_fqn = fqn + "." + k
            if type(v) in [int, bool]:
                pass
            elif type(v) is str:
                coll[k] = update_value(new_fqn, v)
            else:
                if should_delete(new_fqn):
                    if verbosity >= 1:
                        eprint("Marking for deletion:")
                        eprint("   ", coll[k])
                    to_delete.append(k)
                else:
                    descend(coll[k], new_fqn)
    except AttributeError:
        try:
            # Try this as a list-like type
            for idx in range(len(coll)):
                new_fqn = fqn  # Explicitly omit index from fqn
                if type(coll[idx]) is str:
                    coll[idx] = update_value(new_fqn, coll[idx])
                elif type(coll[idx]) in [int, bool]:
                    pass
                else:
                    descend(coll[idx], new_fqn)
        except TypeError:
            eprint("Collection is of unexpected type", type(coll))
            raise

    for section in to_delete:
        del coll[section]


def process_toml(tomlstr):
    tomlobj = toml.loads(tomlstr)
    descend(tomlobj)
    return toml.dumps(tomlobj)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, help="Input pyproject.toml", action="store", default=sys.stdin
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output pyproject.toml",
        action="store",
        default=sys.stdout,
    )
    parser.add_argument(
        "-v", "--verbose", help="Increase verbosity of this tool", action="count", default=0
    )
    args = parser.parse_args()
    verbosity = args.verbose

    if args.input != sys.stdin:
        with open(args.input, "r") as f:
            in_str = f.read()
    else:
        in_str = sys.stdout.read()

    out_str = process_toml(in_str)
    if args.output != sys.stdout:
        with open(args.output, "w") as f:
            f.write(out_str)
    else:
        sys.stdout.write(out_str)
