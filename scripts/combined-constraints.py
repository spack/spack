import argparse
from collections import defaultdict
from typing import List

import spack.config as config
import spack.environment as ev
from spack.spec import Spec


def _collect_always_constraints(pkg_name, pkg_conf) -> List[Spec]:
    collected = []
    if "require" not in pkg_conf:
        return []
    requires = pkg_conf["require"]
    if isinstance(requires, str):
        return [Spec(requires)]

    for requirement in requires:
        if "when" in requirement:
            continue

        if "any_of" in requirement:
            result = requirement["any_of"]
        elif "one_of" in requirement:
            result = requirement["one_of"]
        elif "spec" in requirement:
            result = requirement["spec"]
        else:
            # Should not happen
            result = []

        if len(result) == 1:
            # For one_of/any_of with >1 possibility, it's hard to
            # produce a single spec that represents the combined
            # state: only collect singular constraints.
            result = [Spec(x) for x in result]
            for x in result:
                if not x.name:
                    x.name = pkg_name
            collected.extend(result)

    return collected


def _order_by_root(root, spec_dict):
    possible_dependencies = root.package_class.possible_dependencies(expand_virtuals=False)
    ordered = []
    all_provided = set()
    for x in spec_dict.values():
        all_provided.update(x.package_class.provided.keys())

    for x in possible_dependencies:
        if x in spec_dict or x in all_provided:
            ordered.append(spec_dict[x])
    return ordered


def _merge_constraint(dst_spec, extra_spec):
    # Note: this is for abstract specs which have git commit versions
    # that don't define a numbered-version equivalency like @...=1.0
    dst_spec.attach_git_version_lookup()
    extra_spec.attach_git_version_lookup()
    try:
        dst_spec.constrain(extra_spec)
    except:
        print(f"Failure to constrain {dst_spec} by {extra_spec}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Combine user specs and requirements")
    parser.add_argument("--organizing-root", help="Use this to order output specs")
    args = parser.parse_args()

    e = ev.active_environment()
    aggregated_constraints = defaultdict(list)
    for spec in e.user_specs:
        aggregated_constraints[spec.name].append((spec.copy(), "Environment speclist"))

    conf = config.get("packages")
    for pkg_name, pkg_conf in conf.items():
        if pkg_name == "all":
            continue
        if "require" not in pkg_conf:
            continue
        for constraint_spec in _collect_always_constraints(pkg_name, pkg_conf):
            aggregated_constraints[pkg_name].append(
                (constraint_spec, "require: from packages.yaml")
            )

    for pkg_name, dev_conf in config.get("develop", dict()).items():
        aggregated_constraints[pkg_name].append((Spec(dev_conf["spec"]), "Develop spec"))

    merged_constraints = dict()
    for pkg_name, per_pkg_constraints in aggregated_constraints.items():
        base_spec, reason = per_pkg_constraints[0]
        accumulated = base_spec.copy()
        for next_constraint in per_pkg_constraints[1:]:
            _merge_constraint(accumulated, next_constraint[0])
        merged_constraints[pkg_name] = accumulated

    ordered = list(merged_constraints.values())
    if args.organizing_root:
        ordered = _order_by_root(merged_constraints[args.organizing_root], merged_constraints)

    print("Aggregated constraints:")
    print("\t" + "\n\t".join(str(x) for x in ordered))


if __name__ == "__main__":
    main()
