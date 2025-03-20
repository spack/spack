import argparse
import re
import sys

import toml

verbosity = 0


def update_value(fqn, value):
    if fqn == ".project.name":
        new_val = "spack-package-manager-mlcurry"
    elif fqn == ".project.scripts.spack":
        new_val = "spack." + value
    elif re.match(r"^(lib|bin|var)/spack", value):
        new_val = "spack/" + value
    elif re.match(r"^\./(lib|bin|var)/spack", value):
        new_val = "./spack/" + value[2:]
    elif fqn == ".tool.hatch.build.targets.wheel.include":
        if value[0] == "/":
            new_val = "/spack" + value
        else:
            new_val = "/spack/" + value
    else:
        if verbosity >= 2:
            print("Not changed:")
            print(fqn)
            print("    ", value)
            print()
        return value

    if verbosity >= 1:
        print("Updated", fqn)
        print("   ", value)
        print("   ", new_val)
    return new_val


def should_delete(fqn):
    # Candidates: .tools.[isort, black, mypy, coverage, ruff]
    if fqn in []:
        return True
    return False


def descend(coll, fqn=""):
    # Get down to strings. Fuzzify fqn if necessary.
    to_delete = []
    if type(coll) is dict:
        for k, v in coll.items():
            new_fqn = fqn + "." + k
            if type(v) in [int, bool]:
                pass
            elif type(v) is str:
                coll[k] = update_value(new_fqn, v)
            else:
                if should_delete(new_fqn):
                    if verbosity >= 1:
                        print("Marking for deletion:")
                        print(coll[k])
                    to_delete.append(k)
                else:
                    descend(coll[k], new_fqn)
    elif type(coll) is list:
        for idx in range(len(coll)):
            new_fqn = fqn # Explicitly omit index from fqn
            if type(coll[idx]) is str:
                coll[idx] = update_value(new_fqn, coll[idx])
            elif type(coll[idx]) in [int, bool]:
                pass
            else:
                descend(coll[idx], new_fqn)
    else:
        print('Collection if of unexpected type:', type(coll))
        assert(coll is not dict and coll is not list)
    for section in to_delete:
        del coll[section]


if __name__ == "__main__":
    global verbosity

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
    verbosity = args.verbosity

    spack_toml = toml.load(args.input)

    descend(spack_toml)

    out_str = toml.dumps(spack_toml)
    if args.output != sys.stdout:
        with open(args.output, "w") as f:
            f.write(out_str)
    else:
        sys.stdout.write(out_str)
