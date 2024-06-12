import argparse
import sys
from collections import defaultdict
from typing import List

import spack.concretize
import spack.config as config
import spack.environment as ev
import spack.error
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
    dst_spec.constrain(extra_spec)


def _top_level_constraints_error(pkg_name, constraints):
    formatted_constraints = "\n\t".join(f"{spec} ({reason})" for spec, reason in constraints)
    print(
        f"""Conflicting user-specified constraints for {pkg_name}:
\t{formatted_constraints}
"""
    )


def _check_normalized_constraints(specs):
    with spack.concretize._as_unified(specs) as root:
        root.normalize()


def main():
    parser = argparse.ArgumentParser(description="Combine user specs and requirements")
    parser.add_argument("--organizing-root", help="Use this to order output specs")
    args = parser.parse_args()

    e = ev.active_environment()
    aggregated_constraints = defaultdict(list)
    for spec in e.user_specs:
        aggregated_constraints[spec.name].append((spec.copy(), "Environment speclist"))

    # Collect requirements and non-buildable externals
    for pkg_name, pkg_conf in config.get("packages", dict()).items():
        if pkg_name == "all":
            continue
        if "require" not in pkg_conf:
            continue
        for constraint_spec in _collect_always_constraints(pkg_name, pkg_conf):
            aggregated_constraints[pkg_name].append(
                (constraint_spec, "requirement from packages.yaml")
            )

        if not pkg_conf.get("buildable", True):
            externals = pkg_conf.get("externals", [])
            if len(externals) == 1:
                # If a package isn't buildable, and there's one spec for it, then
                # all of its constraints must apply (there is one possible exception
                # to this rule: if reuse is enabled and already-built instances of
                # the spec are available)
                aggregated_constraints[pkg_name].append(
                    (externals[0]["spec"], "external from packages.yaml")
                )

    # Collect develop specs
    for pkg_name, dev_conf in config.get("develop", dict()).items():
        aggregated_constraints[pkg_name].append((Spec(dev_conf["spec"]), "Develop spec"))

    # TODO: if there are constraints on virtuals, and a provider is in the
    # list of aggregated constraints, the virtual constraints should be
    # moved to the provider here.

    merged_constraints = dict()
    for pkg_name, per_pkg_constraints in aggregated_constraints.items():
        base_spec, reason = per_pkg_constraints[0]
        accumulated = base_spec.copy()
        for next_constraint in per_pkg_constraints[1:]:
            try:
                _merge_constraint(accumulated, next_constraint[0])
            except spack.error.UnsatisfiableSpecError:
                _top_level_constraints_error(pkg_name, per_pkg_constraints)
                sys.exit(1)
        merged_constraints[pkg_name] = accumulated

    if e.unify:
        _check_normalized_constraints(merged_constraints.values())

    ordered = list(merged_constraints.values())
    if args.organizing_root:
        ordered = _order_by_root(merged_constraints[args.organizing_root], merged_constraints)

    print("Aggregated constraints:")
    print("\t" + "\n\t".join(str(x) for x in ordered))


if __name__ == "__main__":
    main()
