import spack.environment as ev
import spack.config as config
from spack.spec import Spec
import argparse


def _collect_always_constraints(pkg_name, pkg_conf):
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
    parser = argparse.ArgumentParser(description='Combine user specs and requirements')
    parser.add_argument('--organizing-root', help='Use this to order output specs')
    args = parser.parse_args()

    e = ev.active_environment()
    aggregated_constraints = dict((x.name, Spec(x)) for x in e.user_specs)

    conf = config.get("packages")
    for pkg_name, pkg_conf in conf.items():
        if pkg_name == "all":
            continue
        if "require" not in pkg_conf:
            continue
        for constraint_spec in _collect_always_constraints(pkg_name, pkg_conf):
            if constraint_spec.name not in aggregated_constraints:
                aggregated_constraints[pkg_name] = constraint_spec
            else:
                _merge_constraint(aggregated_constraints[constraint_spec.name], constraint_spec)

    ordered = list(aggregated_constraints.values())
    if args.organizing_root:
        ordered = _order_by_root(aggregated_constraints[args.organizing_root], aggregated_constraints)

    print("Aggregated constraints:")
    print("\t" + "\n\t".join(str(x) for x in ordered))


if __name__ == "__main__":
    main()