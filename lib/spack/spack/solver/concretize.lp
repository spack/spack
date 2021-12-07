% Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% This logic program implements Spack's concretizer
%=============================================================================

%-----------------------------------------------------------------------------
% Generic constraints on nodes
%-----------------------------------------------------------------------------

% each node must have a single version
:- not 1 { version(PSID, Package, _) } 1, node(PSID, Package).

% each node must have a single platform, os and target
:- not 1 { node_platform(PSID, Package, _) } 1, node(PSID, Package), error("A node must have exactly one platform").
:- not 1 { node_os(PSID, Package, _) } 1, node(PSID, Package).
:- not 1 { node_target(PSID, Package, _) } 1, node(PSID, Package).

% each node has a single compiler associated with it
:- not 1 { node_compiler(PSID, Package, _) } 1, node(PSID, Package).
:- not 1 { node_compiler_version(PSID, Package, _, _) } 1, node(PSID, Package).

%-----------------------------------------------------------------------------
% Version semantics
%-----------------------------------------------------------------------------

% Versions are declared with a weight and an origin, which indicates where the
% version was declared (e.g. "package_py" or "external").
version_declared(Package, Version, Weight) :- version_declared(Package, Version, Weight, _).

% We can't emit the same version **with the same weight** from two different sources
:- version_declared(Package, Version, Weight, Origin1),
   version_declared(Package, Version, Weight, Origin2),
   Origin1 < Origin2,
   error("Internal error: two versions with identical weights").

% versions are declared w/priority -- declared with priority implies declared
version_declared(Package, Version) :- version_declared(Package, Version, _).

% If something is a package, it has only one version and that must be a
% declared version.
1 { version(PSID, Package, Version) : version_declared(Package, Version) } 1
 :- node(PSID, Package), error("Each node must have exactly one version").

% A virtual package may have or not a version, but never has more than one
:- virtual_node(PSID, Virtual), 2 { version(PSID, Virtual, _) }.

% If we select a deprecated version, mark the package as deprecated
deprecated(PSID, Package, Version) :- version(PSID, Package, Version), deprecated_version(Package, Version).

possible_version_weight(PSID, Package, Weight)
 :- version(PSID, Package, Version),
    version_declared(Package, Version, Weight).

1 { version_weight(PSID, Package, Weight) : possible_version_weight(PSID, Package, Weight) } 1 :- node(PSID, Package), error("Internal error: Package version must have a unique weight").

% version_satisfies implies that exactly one of the satisfying versions
1 { version(PSID, Package, Version) : version_satisfies(Package, Constraint, Version) } 1
  :- node_version_satisfies(PSID, Package, Constraint),
     error("no version satisfies the given constraints").
node_version_satisfies(PSID, Package, Constraint)
  :- version(PSID, Package, Version), version_satisfies(Package, Constraint, Version).

#defined version_satisfies/3.
#defined deprecated_version/2.

%-----------------------------------------------------------------------------
% Spec conditions and imposed constraints
%
% Given Spack directives like these:
%    depends_on("foo@1.0+bar", when="@2.0+variant")
%    provides("mpi@2:", when="@1.9:")
%
% The conditions are `@2.0+variant` and `@1.9:`, and the imposed constraints
% are `@1.0+bar` on `foo` and `@2:` on `mpi`.
%-----------------------------------------------------------------------------
% conditions are specified with `condition_requirement` and hold when
% corresponding spec attributes hold.

condition_holds(PSID, ID) :-
  condition(ID);
  attr(Name, PSID, A1) : condition_requirement(ID, Name, A1);
  attr(Name, PSID, A1, A2) : condition_requirement(ID, Name, A1, A2);
  attr(Name, PSID, A1, A2, A3) : condition_requirement(ID, Name, A1, A2, A3);
  process_space(PSID).

% condition_holds(PSID, ID) implies all imposed_constraints, unless do_not_impose(PSID, ID)
% is derived. This allows imposed constraints to be canceled in special cases.
impose(PSID, ID) :- condition_holds(PSID, ID), not do_not_impose(PSID, ID).

% conditions that hold impose constraints on other specs
attr(Name, PSID, Package)         :- impose(PSID, ID), imposed_constraint(ID, Name, Package).
attr(Name, PSID, Package, A1)     :- impose(PSID, ID), imposed_constraint(ID, Name, Package, A1).
attr(Name, PSID, Package, A1, A2) :- impose(PSID, ID), imposed_constraint(ID, Name, Package, A1, A2).

% we cannot have additional variant values when we are working with concrete specs
:- node(PSID, Package), hash(PSID, Package, Hash),
   variant_value(PSID, Package, Variant, Value),
   not imposed_constraint(Hash, "variant_value", Package, Variant, Value).

#defined condition/1.
#defined condition_requirement/3.
#defined condition_requirement/4.
#defined condition_requirement/5.
#defined imposed_constraint/3.
#defined imposed_constraint/4.
#defined imposed_constraint/5.

%-----------------------------------------------------------------------------
% Concrete specs
%-----------------------------------------------------------------------------
% TODO: I don't think this is used anywhere
% if a package is assigned a hash, it's concrete.
concrete(PSID, Package) :- hash(PSID, Package, _), node(PSID, Package).

%-----------------------------------------------------------------------------
% Dependency semantics
%-----------------------------------------------------------------------------
% Dependencies of any type imply that one package "depends on" another
depends_on(PSID, Package, Dependency)
 :- depends_on(PSID, Package, Dependency, _).

% a dependency holds if its condition holds and if it is not external or
% concrete. We chop off dependencies for externals, and dependencies of
% concrete specs don't need to be resolved -- they arise from the concrete
% specs themselves.
dependency_holds(PSID, Package, Dependency, Type) :-
  dependency_condition(ID, Package, Dependency),
  dependency_type(ID, Type),
  condition_holds(PSID, ID),
  build(PSID, Package),
  not external(PSID, Package).

% We cut off dependencies of externals (as we don't really know them).
% Don't impose constraints on dependencies that don't exist.
do_not_impose(PSID, ID) :-
  not dependency_holds(PSID, Package, Dependency, _),
  dependency_condition(ID, Package, Dependency),
  node(PSID, Package).

% declared dependencies are real if they're not virtual AND
% the package is not an external.
% They're only triggered if the associated dependnecy condition holds.
depends_on(PSID, Package, Dependency, Type)
 :- dependency_holds(PSID, Package, Dependency, Type),
    not virtual(Dependency).

% every root must be a node
node(PSID, Package) :- root(PSID, Package).

% if a node is defined with a process space ID, that PSID is a process space
process_space(PSID) :- root(PSID, _).

% dependencies imply new nodes
node(PSID, Dependency) :- node(PSID, Package), depends_on(PSID, Package, Dependency).

% all nodes in the graph must be reachable from some root
% this ensures a user can't say `zlib ^libiconv` (neither of which have any
% dependencies) and get a two-node unconnected graph
needed(PSID, Package) :- root(PSID, Package).
needed(PSID, Dependency) :- needed(PSID, Package),
                              depends_on(PSID, Package, Dependency).
:- node(PSID, Package), not needed(PSID, Package),
   error("All dependencies must be reachable from root").

% Avoid cycles in the DAG
% some combinations of conditional dependencies can result in cycles;
% this ensures that we solve around them
path(PSID, Parent, Child) :- depends_on(PSID, Parent, Child).
path(PSID, Parent, Descendant)
 :- path(PSID, Parent, A),
    depends_on(PSID, A, Descendant).
:- path(PSID, A, B), path(PSID, B, A),
   error("Cyclic dependencies are not allowed").

#defined error/1.

#defined dependency_type/2.
#defined dependency_condition/3.

%-----------------------------------------------------------------------------
% Conflicts
%-----------------------------------------------------------------------------

:- node(PSID, Package),
   conflict(Package, TriggerID, ConstraintID, _),
   condition_holds(PSID, TriggerID),
   condition_holds(PSID, ConstraintID),
   not external(PSID, Package),  % ignore conflicts for externals
   error("A conflict was triggered").

#defined conflict/4.

%-----------------------------------------------------------------------------
% Virtual dependencies
%-----------------------------------------------------------------------------

% if a package depends on a virtual, it's not external and we have a
% provider for that virtual then it depends on the provider
depends_on(PSID, Package, Provider, Type)
  :- dependency_holds(PSID, Package, Virtual, Type),
     provider(PSID, Provider, Virtual),
     not external(PSID, Package).

% dependencies on virtuals also imply that the virtual is a virtual node
virtual_node(PSID, Virtual)
  :- dependency_holds(PSID, Package, Virtual, Type),
     virtual(Virtual), not external(PSID, Package).

% If there's a virtual node, we must select one and only one provider.
% The provider must be selected among the possible providers.
1 { provider(PSID, Package, Virtual) : possible_provider(Package, Virtual) } 1
  :- virtual_node(PSID, Virtual), error("Virtual packages must be satisfied by a unique provider").

% virtual roots imply virtual nodes, and that one provider is a root
virtual_node(PSID, Virtual) :- virtual_root(PSID, Virtual).

% If we asked for a virtual root and we have a provider for that,
% then the provider is the root package.
root(PSID, Package) :- virtual_root(PSID, Virtual), provider(PSID, Package, Virtual).

% If we asked for a root package and that root provides a virtual,
% the root is a provider for that virtual. This rule is mostly relevant
% for environments that are concretized together (e.g. where we
% asks to install "mpich" and "hdf5+mpi" and we want "mpich" to
% be the mpi provider)
provider(PSID, Package, Virtual) :- node(PSID, Package), virtual_condition_holds(PSID, Package, Virtual).

% The provider provides the virtual if some provider condition holds.
virtual_condition_holds(PSID, Provider, Virtual) :-
   provider_condition(ID, Provider, Virtual),
   condition_holds(PSID, ID),
   virtual(Virtual).

% A package cannot be the actual provider for a virtual if it does not
% fulfill the conditions to provide that virtual
:- provider(PSID, Package, Virtual), not virtual_condition_holds(PSID, Package, Virtual),
   error("Internal error: virtual when provides not respected").

#defined possible_provider/2.

%-----------------------------------------------------------------------------
% Virtual dependency weights
%-----------------------------------------------------------------------------

% A provider may have different possible weights depending on whether it's an external
% or not, or on preferences expressed in packages.yaml etc. This rule ensures that
% we select the weight, among the possible ones, that minimizes the overall objective function.
1 { provider_weight(PSID, Dependency, Virtual, Weight, Reason) :
    possible_provider_weight(PSID, Dependency, Virtual, Weight, Reason) } 1
 :- provider(PSID, Dependency, Virtual), error("Internal error: package provider weights must be unique").

% Get rid or the reason for enabling the possible weight (useful for debugging)
provider_weight(PSID, Dependency, Virtual, Weight) :- provider_weight(PSID, Dependency, Virtual, Weight, _).

% A provider that is an external can use a weight of 0
possible_provider_weight(PSID, Dependency, Virtual, 0, "external")
  :- provider(PSID, Dependency, Virtual),
     external(PSID, Dependency).

% A provider mentioned in packages.yaml can use a weight
% according to its priority in the list of providers
possible_provider_weight(PSID, Dependency, Virtual, Weight, "packages_yaml")
  :- provider(PSID, Dependency, Virtual),
     depends_on(PSID, Package, Dependency),
     pkg_provider_preference(Package, Virtual, Dependency, Weight).

% A provider mentioned in the default configuration can use a weight
% according to its priority in the list of providers
possible_provider_weight(PSID, Dependency, Virtual, Weight, "default")
  :- provider(PSID, Dependency, Virtual),
     default_provider_preference(Virtual, Dependency, Weight).

% Any provider can use 100 as a weight, which is very high and discourage its use
possible_provider_weight(PSID, Dependency, Virtual, 100, "fallback") :- provider(PSID, Dependency, Virtual).

#defined possible_provider/2.
#defined provider_condition/3.

%-----------------------------------------------------------------------------
% Spec Attributes
%-----------------------------------------------------------------------------
% Equivalencies of the form:
%
%   name(Arg1, Arg2, ...) :- attr("name", PSID, Arg1, Arg2, ...).
%   attr("name", PSID, Arg1, Arg2, ...) :- name(Arg1, Arg2, ...).
%
% These allow us to easily define conditional dependency and conflict rules
% without enumerating all spec attributes every time.
node(PSID, Package)                          :- attr("node", PSID, Package).
hash(PSID, Package, Hash)                    :- attr("hash", PSID, Package, Hash).
version(PSID, Package, Version)              :- attr("version", PSID, Package, Version).
node_version_satisfies(PSID, Package, Constraint) :- attr("node_version_satisfies", PSID, Package, Constraint).
node_platform(PSID, Package, Platform)       :- attr("node_platform", PSID, Package, Platform).
node_os(PSID, Package, OS)                   :- attr("node_os", PSID, Package, OS).
node_target(PSID, Package, Target)           :- attr("node_target", PSID, Package, Target).
node_target_satisfies(PSID, Package, Target) :- attr("node_target_satisfies", PSID, Package, Target).
variant_value(PSID, Package, Variant, Value) :- attr("variant_value", PSID, Package, Variant, Value).
variant_set(PSID, Package, Variant, Value)   :- attr("variant_set", PSID, Package, Variant, Value).
node_flag(PSID, Package, FlagType, Flag)     :- attr("node_flag", PSID, Package, FlagType, Flag).
node_compiler(PSID, Package, Compiler)       :- attr("node_compiler", PSID, Package, Compiler).
depends_on(PSID, Package, Dependency, Type)  :- attr("depends_on", PSID, Package, Dependency, Type).
node_compiler_version(PSID, Package, Compiler, Version)
  :- attr("node_compiler_version", PSID, Package, Compiler, Version).
node_compiler_version_satisfies(PSID, Package, Compiler, Version)
  :- attr("node_compiler_version_satisfies", PSID, Package, Compiler, Version).

attr("node", PSID, Package)                          :- node(PSID, Package).
attr("hash", PSID, Package, Hash)                    :- hash(PSID, Package, Hash).
attr("version", PSID, Package, Version)              :- version(PSID, Package, Version).
attr("node_version_satisfies", PSID, Package, Constraint) :- node_version_satisfies(PSID, Package, Constraint).
attr("node_platform", PSID, Package, Platform)       :- node_platform(PSID, Package, Platform).
attr("node_os", PSID, Package, OS)                   :- node_os(PSID, Package, OS).
attr("node_target", PSID, Package, Target)           :- node_target(PSID, Package, Target).
attr("node_target_satisfies", PSID, Package, Target) :- node_target_satisfies(PSID, Package, Target).
attr("variant_value", PSID, Package, Variant, Value) :- variant_value(PSID, Package, Variant, Value).
attr("variant_set", PSID, Package, Variant, Value)   :- variant_set(PSID, Package, Variant, Value).
attr("node_flag", PSID, Package, FlagType, Flag)     :- node_flag(PSID, Package, FlagType, Flag).
attr("node_compiler", PSID, Package, Compiler)       :- node_compiler(PSID, Package, Compiler).
attr("depends_on", PSID, Package, Dependency, Type)  :- depends_on(PSID, Package, Dependency, Type).
attr("node_compiler_version", PSID, Package, Compiler, Version)
  :- node_compiler_version(PSID, Package, Compiler, Version).
attr("node_compiler_version_satisfies", PSID, Package, Compiler, Version)
  :- node_compiler_version_satisfies(PSID, Package, Compiler, Version).

% do not warn if generated program contains none of these.
#defined depends_on/4.
#defined declared_dependency/3.
#defined virtual/1.
#defined virtual_node/2.
#defined virtual_root/2.
#defined virtual_condition_holds/3.
#defined external/2.
#defined external_spec/2.
#defined external_version_declared/4.
#defined external_only/1.
#defined pkg_provider_preference/4.
#defined default_provider_preference/3.
#defined node_version_satisfies/3.
#defined node_compiler_version_satisfies/4.
#defined root/2.

%-----------------------------------------------------------------------------
% External semantics
%-----------------------------------------------------------------------------

% if a package is external its version must be one of the external versions
1 { external_version(PSID, Package, Version, Weight):
    version_declared(Package, Version, Weight, "external") } 1
    :- external(PSID, Package), error("External package version does not satisfy external spec").

version_weight(PSID, Package, Weight) :- external_version(PSID, Package, Version, Weight).
version(PSID, Package, Version) :- external_version(PSID, Package, Version, Weight).

% if a package is not buildable (external_only), only externals are allowed
external(PSID, Package) :- external_only(Package), node(PSID, Package).

% a package is a real_node if it is not external
% TODO: We don't use this anywhere
real_node(PSID, Package) :- node(PSID, Package), not external(PSID, Package).

% a package is external if we are using an external spec for it
external(PSID, Package) :- external_spec_selected(PSID, Package, _).

% we can't use the weight for an external version if we don't use the
% corresponding external spec.
:- version(PSID, Package, Version),
   version_weight(PSID, Package, Weight),
   version_declared(Package, Version, Weight, "external"),
   not external(PSID, Package),
   error("Internal error: external weight used for internal spec").

% determine if an external spec has been selected
external_spec_selected(PSID, Package, LocalIndex) :-
    external_conditions_hold(PSID, Package, LocalIndex),
    node(PSID, Package).

external_conditions_hold(PSID, Package, LocalIndex) :-
    possible_external(ID, Package, LocalIndex), condition_holds(PSID, ID).

% it cannot happen that a spec is external, but none of the external specs
% conditions hold.
:- external(PSID, Package),
   not external_conditions_hold(PSID, Package, _),
   error("External package does not satisfy external spec").

#defined possible_external/3.

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------
% a variant is a variant of a package if it is a variant under some condition
% and that condition holds
variant(PSID, Package, Variant) :- variant_condition(ID, Package, Variant),
                             condition_holds(PSID, ID).

% a variant cannot be set if it is not a variant on the package
:- variant_set(PSID, Package, Variant),
   not variant(PSID, Package, Variant),
   build(PSID, Package),
   error("Unsatisfied conditional variants cannot be set").

% a variant cannot take on a value if it is not a variant of the package
:- variant_value(PSID, Package, Variant, _),
   not variant(PSID, Package, Variant),
   build(PSID, Package),
   error("Unsatisfied conditional variants cannot take on a variant value").

% if a variant is sticky and not set its value is the default value
variant_value(PSID, Package, Variant, Value) :-
  variant(PSID, Package, Variant),
  not variant_set(PSID, Package, Variant),
  variant_sticky(Package, Variant),
  variant_default_value(PSID, Package, Variant, Value),
  build(PSID, Package).

% one variant value for single-valued variants.
1 {
  variant_value(PSID, Package, Variant, Value)
  : variant_possible_value(Package, Variant, Value)
} 1
 :- node(PSID, Package),
    variant(PSID, Package, Variant),
    variant_single_value(Package, Variant),
    build(PSID, Package),
    error("Single valued variants must have a single value").

% at least one variant value for multi-valued variants.
1 {
 variant_value(PSID, Package, Variant, Value)
 : variant_possible_value(Package, Variant, Value)
}
 :- node(PSID, Package),
    variant(PSID, Package, Variant),
    not variant_single_value(Package, Variant),
    build(PSID, Package),
    error("Internal error: All variants must have a value").

% if a variant is set to anything, it is considered 'set'.
variant_set(PSID, Package, Variant) :- variant_set(PSID, Package, Variant, _).

% A variant cannot have a value that is not also a possible value
% This only applies to packages we need to build -- concrete packages may
% have been built w/different variants from older/different package versions.
:- variant_value(PSID, Package, Variant, Value),
   not variant_possible_value(Package, Variant, Value),
   build(PSID, Package),
   error("Variant set to invalid value").

% Some multi valued variants accept multiple values from disjoint sets.
% Ensure that we respect that constraint and we don't pick values from more
% than one set at once
:- variant_value(PSID, Package, Variant, Value1),
   variant_value(PSID, Package, Variant, Value2),
   variant_value_from_disjoint_sets(Package, Variant, Value1, Set1),
   variant_value_from_disjoint_sets(Package, Variant, Value2, Set2),
   Set1 < Set2,
   build(PSID, Package),
   error("Variant values selected from multiple disjoint sets").

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(PSID, Package, Variant, Value)
 :- node(PSID, Package),
    variant(PSID, Package, Variant),
    variant_set(PSID, Package, Variant, Value).

% The rules below allow us to prefer default values for variants
% whenever possible. If a variant is set in a spec, or if it is
% specified in an external, we score it as if it was a default value.
variant_not_default(PSID, Package, Variant, Value)
 :- variant_value(PSID, Package, Variant, Value),
    not variant_default_value(PSID, Package, Variant, Value),
    % variants set explicitly on the CLI don't count as non-default
    not variant_set(PSID, Package, Variant, Value),
    % variants set on externals that we could use don't count as non-default
    % this makes spack prefer to use an external over rebuilding with the
    % default configuration
    not external_with_variant_set(PSID, Package, Variant, Value),
    node(PSID, Package).


% A default variant value that is not used
variant_default_not_used(PSID, Package, Variant, Value)
  :- variant_default_value(PSID, Package, Variant, Value),
     not variant_value(PSID, Package, Variant, Value),
     node(PSID, Package).

% The variant is set in an external spec
% TODO: I think this has a subtle bug
% What if the package is set external by a different external condition
% than the one that conveys the requirement?
external_with_variant_set(PSID, Package, Variant, Value)
 :- variant_value(PSID, Package, Variant, Value),
    condition_requirement(ID, "variant_value", Package, Variant, Value),
    possible_external(ID, Package, _),
    external(PSID, Package),
    node(PSID, Package).

% The default value for a variant in a package is what is prescribed:
%
% 1. On the command line
% 2. In packages.yaml (if there's no command line settings)
% 3. In the package.py file (if there are no settings in
%    packages.yaml and the command line)
%
variant_default_value(PSID, Package, Variant, Value)
 :- variant_default_value_from_package_py(Package, Variant, Value),
    not variant_default_value_from_packages_yaml(Package, Variant, _),
    not variant_default_value_from_cli(PSID, Package, Variant, _),
    node(PSID, Package).

variant_default_value(PSID, Package, Variant, Value)
 :- variant_default_value_from_packages_yaml(Package, Variant, Value),
    not variant_default_value_from_cli(PSID, Package, Variant, _),
    node(PSID, Package).

variant_default_value(PSID, Package, Variant, Value) :- variant_default_value_from_cli(PSID, Package, Variant, Value).

% Treat 'none' in a special way - it cannot be combined with other
% values even if the variant is multi-valued
:- 2 {
     variant_value(PSID, Package, Variant, Value) : variant_possible_value(Package, Variant, Value)
   },
   variant_value(PSID, Package, Variant, "none"),
   build(PSID, Package),
   error("Variant value 'none' cannot be combined with any other value").

% patches and dev_path are special variants -- they don't have to be
% declared in the package, so we just allow them to spring into existence
% when assigned a value.
auto_variant("dev_path").
auto_variant("patches").
variant(PSID, Package, Variant)
  :- variant_set(PSID, Package, Variant, _), auto_variant(Variant).
variant_single_value(Package, "dev_path")
  :- variant_set(PSID, Package, "dev_path", _).

% suppress warnings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant/3.
#defined variant_sticky/2.
#defined variant_set/4.
#defined variant_condition/3.
#defined variant_single_value/2.
#defined variant_default_value/4.
#defined variant_possible_value/3.
#defined variant_default_value_from_cli/4.
#defined variant_default_value_from_packages_yaml/3.
#defined variant_default_value_from_package_py/3.
#defined variant_value_from_disjoint_sets/4.

%-----------------------------------------------------------------------------
% Platform semantics
%-----------------------------------------------------------------------------

% if no platform is set, fall back to the default
% TODO: rename node_platform_default -- node_* implies attribute of node
node_platform(PSID, Package, Platform)
 :- node(PSID, Package),
    not node_platform_set(PSID, Package),
    node_platform_default(Platform).

% setting platform on a node is a hard constraint
node_platform(PSID, Package, Platform)
 :- node(PSID, Package), node_platform_set(PSID, Package, Platform).

% platform is set if set to anything
node_platform_set(PSID, Package) :- node_platform_set(PSID, Package, _).

#defined node_platform_set/3.  % avoid warnings

%-----------------------------------------------------------------------------
% OS semantics
%-----------------------------------------------------------------------------
% convert weighted OS declarations to simple one
os(OS) :- os(OS, _).

% one os per node
1 { node_os(PSID, Package, OS) : os(OS) } 1 :-
   node(PSID, Package), error("Each node must have exactly one OS").

% can't have a non-buildable OS on a node we need to build
:- build(PSID, Package), node_os(PSID, Package, OS), not buildable_os(OS),
   error("No available OS can be built for").

% can't have dependencies on incompatible OS's
:- depends_on(PSID, Package, Dependency),
   node_os(PSID, Package, PackageOS),
   node_os(PSID, Dependency, DependencyOS),
   not os_compatible(PackageOS, DependencyOS),
   build(PSID, Package),
   error("Dependencies must have compatible OS's with their dependents").

% give OS choice weights according to os declarations
node_os_weight(PSID, Package, Weight)
 :- node(PSID, Package),
    node_os(PSID, Package, OS),
    os(OS, Weight).

% match semantics for OS's
node_os_match(PSID, Package, Dependency) :-
   depends_on(PSID, Package, Dependency), node_os(PSID, Package, OS), node_os(PSID, Dependency, OS).
node_os_mismatch(PSID, Package, Dependency) :-
   depends_on(PSID, Package, Dependency), not node_os_match(PSID, Package, Dependency).

% every OS is compatible with itself. We can use `os_compatible` to declare
os_compatible(OS, OS) :- os(OS).

% OS compatibility rules for reusing solves.
% catalina binaries can be used on bigsur. Direction is package -> dependency.
os_compatible("bigsur", "catalina").

% If an OS is set explicitly respect the value
node_os(PSID, Package, OS) :- node_os_set(PSID, Package, OS), node(PSID, Package).

#defined node_os_set/3.
#defined os_compatible/2.

%-----------------------------------------------------------------------------
% Target semantics
%-----------------------------------------------------------------------------
% Each node has only one target chosen among the known targets
1 { node_target(PSID, Package, Target) : target(Target) } 1 :- node(PSID, Package), error("Each node must have exactly one target").

% If a node must satisfy a target constraint the choice is reduced among the targets
% that satisfy that constraint
1 { node_target(PSID, Package, Target) : target_satisfies(Constraint, Target) } 1
  :- node_target_satisfies(PSID, Package, Constraint), error("Each node must have exactly one target").

% If a node has a target and the target satisfies a constraint, then the target
% associated with the node satisfies the same constraint
node_target_satisfies(PSID, Package, Constraint)
  :- node_target(PSID, Package, Target), target_satisfies(Constraint, Target).

#defined target_satisfies/2.

% The target weight is either the default target weight
% or a more specific per-package weight if set
target_weight(PSID, Target, Package, Weight)
  :- default_target_weight(Target, Weight),
     node(PSID, Package),
     not derive_target_from_parent(PSID, _, Package),
     not package_target_weight(PSID, Target, Package, _).

% TODO: Need to account for the case of more than one parent
% TODO: each of which sets different targets
target_weight(PSID, Target, Dependency, Weight)
  :- depends_on(PSID, Package, Dependency),
     derive_target_from_parent(PSID, Package, Dependency),
     target_weight(PSID, Target, Package, Weight).

target_weight(PSID, Target, Package, Weight)
  :- package_target_weight(PSID, Target, Package, Weight).

% can't use targets on node if the compiler for the node doesn't support them
:- node_target(PSID, Package, Target),
   not compiler_supports_target(Compiler, Version, Target),
   node_compiler(PSID, Package, Compiler),
   node_compiler_version(PSID, Package, Compiler, Version),
   build(PSID, Package),
   error("No satisfying compiler available is compatible with a satisfying target").

% if a target is set explicitly, respect it
node_target(PSID, Package, Target)
 :- node(PSID, Package), node_target_set(PSID, Package, Target).

% each node has the weight of its assigned target
node_target_weight(PSID, Package, Weight)
 :- node(PSID, Package),
    node_target(PSID, Package, Target),
    target_weight(PSID, Target, Package, Weight).

derive_target_from_parent(PSID, Parent, Package)
  :- depends_on(PSID, Parent, Package),
     not package_target_weight(PSID, _, Package, _).

% compatibility rules for targets among nodes
node_target_match(PSID, Parent, Dependency)
  :- depends_on(PSID, Parent, Dependency),
     node_target(PSID, Parent, Target),
     node_target(PSID, Dependency, Target).

node_target_mismatch(PSID, Parent, Dependency)
  :- depends_on(PSID, Parent, Dependency),
     not node_target_match(PSID, Parent, Dependency).

% disallow reusing concrete specs that don't have a compatible target
:- node(PSID, Package), node_target(PSID, Package, Target), not target(Target),
   error("No satisfying package's target is compatible with this machine").

#defined node_target_set/3.
#defined package_target_weight/4.

%-----------------------------------------------------------------------------
% Compiler semantics
%-----------------------------------------------------------------------------
compiler(Compiler) :- compiler_version(Compiler, _).

% There must be only one compiler set per built node. The compiler
% is chosen among available versions.
1 { node_compiler_version(PSID, Package, Compiler, Version) : compiler_version(Compiler, Version) } 1 :-
    node(PSID, Package),
    build(PSID, Package),
    error("Each node must have exactly one compiler").

% Sometimes we just need to know the compiler and not the version
node_compiler(PSID, Package, Compiler) :- node_compiler_version(PSID, Package, Compiler, _).

% We can't have a compiler be enforced and select the version from another compiler
:- node_compiler(PSID, Package, Compiler1),
   node_compiler_version(PSID, Package, Compiler2, _),
   Compiler1 != Compiler2,
   error("Internal error: mismatch between selected compiler and compiler version").

% If the compiler of a node must satisfy a constraint, then its version
% must be chosen among the ones that satisfy said constraint
1 { node_compiler_version(PSID, Package, Compiler, Version)
    : compiler_version_satisfies(Compiler, Constraint, Version) } 1 :-
    node_compiler_version_satisfies(PSID, Package, Compiler, Constraint),
    error("Internal error: node compiler version mismatch").

% If the node is associated with a compiler and the compiler satisfy a constraint, then
% the compiler associated with the node satisfy the same constraint
node_compiler_version_satisfies(PSID, Package, Compiler, Constraint)
  :- node_compiler_version(PSID, Package, Compiler, Version),
     compiler_version_satisfies(Compiler, Constraint, Version),
     build(PSID, Package).

#defined compiler_version_satisfies/3.

% If the compiler version was set from the command line,
% respect it verbatim
node_compiler_version(PSID, Package, Compiler, Version) :- node_compiler_version_set(PSID, Package, Compiler, Version).

% Cannot select a compiler if it is not supported on the OS
% Compilers that are explicitly marked as allowed
% are excluded from this check
:- node_compiler_version(PSID, Package, Compiler, Version), node_os(PSID, Package, OS),
   not compiler_supports_os(Compiler, Version, OS),
   not allow_compiler(Compiler, Version),
   build(PSID, Package),
   error("No satisfying compiler available is compatible with a satisfying os").

% If a package and one of its dependencies don't have the
% same compiler there's a mismatch.
compiler_match(PSID, Package, Dependency)
  :- depends_on(PSID, Package, Dependency),
     node_compiler_version(PSID, Package, Compiler, Version),
     node_compiler_version(PSID, Dependency, Compiler, Version).

compiler_mismatch(PSID, Package, Dependency)
  :- depends_on(PSID, Package, Dependency),
     not compiler_match(PSID, Package, Dependency).

#defined node_compiler_version_set/4.
#defined compiler_supports_os/3.
#defined allow_compiler/2.

% compilers weighted by preference according to packages.yaml
% TODO rename node_compiler_preference, it's package specific not node
% specific
compiler_weight(PSID, Package, Weight)
 :- node_compiler_version(PSID, Package, Compiler, V),
    node_compiler_preference(Package, Compiler, V, Weight).
compiler_weight(PSID, Package, Weight)
 :- node_compiler_version(PSID, Package, Compiler, V),
    not node_compiler_preference(Package, Compiler, V, _),
    default_compiler_preference(Compiler, V, Weight).
compiler_weight(PSID, Package, 100)
 :- node_compiler_version(PSID, Package, Compiler, Version),
    not node_compiler_preference(Package, Compiler, Version, _),
    not default_compiler_preference(Compiler, Version, _).

#defined node_compiler_preference/4.
#defined default_compiler_preference/3.

%-----------------------------------------------------------------------------
% Compiler flags
%-----------------------------------------------------------------------------
% propagate flags when compilers match
% TODO: What is flag_type doing here?
inherit_flags(PSID, Package, Dependency)
 :- depends_on(PSID, Package, Dependency),
    node_compiler(PSID, Package, Compiler),
    node_compiler(PSID, Dependency, Compiler),
    compiler(Compiler), flag_type(FlagType).
node_flag_inherited(PSID, Dependency, FlagType, Flag)
 :- node_flag_set(PSID, Package, FlagType, Flag),
    inherit_flags(PSID, Package, Dependency).
node_flag_inherited(PSID, Dependency, FlagType, Flag)
 :- node_flag_inherited(PSID, Package, FlagType, Flag),
    inherit_flags(PSID, Package, Dependency).

% node with flags set to anythingg is "set"
node_flag_set(PSID, Package) :- node_flag_set(PSID, Package, _, _).

% remember where flags came from
node_flag_source(PSID, Package, Package) :- node_flag_set(PSID, Package).
node_flag_source(PSID, Dependency, Q)
 :- node_flag_source(PSID, Package, Q),
    inherit_flags(PSID, Package, Dependency).

% compiler flags from compilers.yaml are put on nodes if compiler matches
% TODO: compilers could differ only in flags. Need a compiler ID to
% differentiate
node_flag(PSID, Package, FlagType, Flag)
 :- not node_flag_set(PSID, Package),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    node_compiler_version(PSID, Package, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

% TODO: This doesn't appear to be used
node_flag_compiler_default(PSID, Package)
 :- not node_flag_set(PSID, Package),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    node_compiler_version(PSID, Package, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

% if a flag is set to something or inherited, it's included
node_flag(PSID, Package, FlagType, Flag) :- node_flag_set(PSID, Package, FlagType, Flag).
node_flag(PSID, Package, FlagType, Flag)
 :- node_flag_inherited(PSID, Package, FlagType, Flag).

% if no node flags are set for a type, there are no flags.
no_flags(PSID, Package, FlagType)
 :- not node_flag(PSID, Package, FlagType, _), node(PSID, Package), flag_type(FlagType).

#defined compiler_version_flag/4.
#defined node_flag/4.
#defined node_flag_set/4.


%-----------------------------------------------------------------------------
% Installed packages
%-----------------------------------------------------------------------------
% the solver is free to choose at most one installed hash for each package
{ hash(PSID, Package, Hash) : installed_hash(Package, Hash) } 1
 :- node(PSID, Package), error("Internal error: package must resolve to at most one hash").

% if a hash is selected, we impose all the constraints that implies
impose(PSID, Hash) :- hash(PSID, Package, Hash).

% if we haven't selected a hash for a package, we'll be building it
build(PSID, Package)
 :- not hash(PSID, Package, _),
    node(PSID, Package),
    not handled_by_another_process_space(PSID, Package).

% Minimizing builds is tricky. We want a minimizing criterion

% because we want to reuse what is avaialble, but
% we also want things that are built to stick to *default preferences* from
% the package and from the user. We therefore treat built specs differently and apply
% a different set of optimization criteria to them. Spack's *first* priority is to
% reuse what it *can*, but if it builds something, the built specs will respect
% defaults and preferences.  This is implemented by bumping the priority of optimization
% criteria for built specs -- so that they take precedence over the otherwise
% topmost-priority criterion to reuse what is installed.
%
% The priority ranges are:
%   300+        Unshifted priorities that supersede build nodes.
%   200 - 299   Shifted priorities for build nodes; correspond to priorities 0 - 99.
%   100 - 199   Unshifted priorities. Currently only includes minimizing #builds.
%   0   -  99   Priorities for non-built nodes.
build_priority(PSID, Package, 200)
 :- build(PSID, Package), node(PSID, Package).
build_priority(PSID, Package, 0)
 :- not build(PSID, Package), node(PSID, Package).

#defined installed_hash/2.

%-----------------------------------------------------------------------------
% How many of each package do we need?
%-----------------------------------------------------------------------------
% If two roots provide the same spec for the same package,
% we only count it once in the optimizations
% because we only have to build it once
% We will then minimize within each package
% for the number of PSIDs that are not handled by another PSID
roots_equivalent_for_package(PSID1, PSID2, Package)
 :- node(PSID1, Package);
    node(PSID2, Package);
    attr(Name, PSID1, Package) : attr(Name, PSID2, Package);
    attr(Name, PSID1, Package, A1) : attr(Name, PSID2, Package, A1);
    attr(Name, PSID1, Package, A1, A2) : attr(Name, PSID2, Package, A1, A2);
    attr(Name, PSID2, Package) : attr(Name, PSID1, Package);
    attr(Name, PSID2, Package, A1) : attr(Name, PSID1, Package, A1);
    attr(Name, PSID2, Package, A1, A2) : attr(Name, PSID1, Package, A1, A2).

prefer_satisfier(ID1, ID2, Package)
 :- roots_equivalent_for_package(ID1, ID2, Package),
    ID1 < ID2.

handled_by_another_process_space(PSID, Package)
 :- node(PSID, Package),
    prefer_satisfier(_, PSID, Package).

% Only want to penalize the optimization for duplicates
% Don't penalize for the first instance of a given package.
% Arbitrarily choosing the "lowest" PSID to not penalize
duplicate(PSID, Package)
 :- node(PSID, Package),
    node(OtherPSID, Package),
    PSID != OtherPSID,
    not roots_equivalent_for_package(PSID, OtherPSID, Package),
    PSID > OtherPSID.

%-----------------------------------------------------------------------------
% How to optimize the spec (high to low priority)
%-----------------------------------------------------------------------------
% Each criterion below has:
%   1. an opt_criterion(ID, Name) fact that describes the criterion, and
%   2. a `#minimize{ 0@2 : #true }.` statement that ensures the criterion
%      is displayed (clingo doesn't display sums over empty sets by default)

% Try to minimize the number of nodes of a given package
opt_criterion(300, "agreement of nodes across process spaces").
#minimize { 0@300: #true }.
#minimize { 1@300,Package,PSID : duplicate(PSID, Package) }.

% Try hard to reuse installed packages (i.e., minimize the number built)
opt_criterion(100, "number of packages to build (vs. reuse)").
#minimize { 0@100: #true }.
#minimize { 1@100,Package,PSID : build(PSID, Package), optimize_for_reuse() }.
#defined optimize_for_reuse/0.

% Minimize the number of deprecated versions being used
opt_criterion(15, "deprecated versions used").
#minimize{ 0@215: #true }.
#minimize{ 0@15: #true }.
#minimize{
    1@15+Priority,Package,PSID
    : deprecated(PSID, Package, _),
      build_priority(PSID, Package, Priority)
}.

% Minimize the:
% 1. Version weight
% 2. Number of variants with a non default value, if not set
% for the root(PSID, Package)
opt_criterion(14, "version weight").
#minimize{ 0@214: #true }.
#minimize{ 0@14: #true }.
#minimize {
    Weight@14+Priority,PSID
    : root(PSID, Package),version_weight(PSID, Package, Weight),
      build_priority(PSID, Package, Priority)
}.

opt_criterion(13, "number of non-default variants (roots)").
#minimize{ 0@213: #true }.
#minimize{ 0@13: #true }.
#minimize {
    1@13+Priority,Package,Variant,Value,PSID
    : variant_not_default(PSID, Package, Variant, Value),
      root(PSID, Package),
      build_priority(PSID, Package, Priority)
}.

opt_criterion(12, "preferred providers for roots").
#minimize{ 0@212 : #true }.
#minimize{ 0@12: #true }.
#minimize{
    Weight@12+Priority,Provider,Virtual,PSID
    : provider_weight(PSID, Provider, Virtual, Weight),
      root(PSID, Provider),
      build_priority(PSID, Provider, Priority)
}.

opt_criterion(11, "default values of variants not being used (roots)").
#minimize{ 0@211: #true }.
#minimize{ 0@11: #true }.
#minimize{
    1@11+Priority,Package,Variant,Value,PSID
    : variant_default_not_used(PSID, Package, Variant, Value),
      root(PSID, Package),
      build_priority(PSID, Package, Priority)
}.

% Try to use default variants or variants that have been set
opt_criterion(10, "number of non-default variants (non-roots)").
#minimize{ 0@210: #true }.
#minimize{ 0@10: #true }.
#minimize {
    1@10+Priority,Package,Variant,Value,PSID
    : variant_not_default(PSID, Package, Variant, Value),
      not root(PSID, Package),
      build_priority(PSID, Package, Priority)
}.

% Minimize the weights of the providers, i.e. use as much as
% possible the most preferred providers
opt_criterion(9, "preferred providers (non-roots)").
#minimize{ 0@209: #true }.
#minimize{ 0@9: #true }.
#minimize{
    Weight@9+Priority,Provider,Virtual,PSID
    : provider_weight(PSID, Provider, Virtual, Weight), not root(PSID, Provider),
      build_priority(PSID, Provider, Priority)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(8, "compiler mismatches").
#minimize{ 0@208: #true }.
#minimize{ 0@8: #true }.
#minimize{
    1@8+Priority,Package,Dependency,PSID
    : compiler_mismatch(PSID, Package, Dependency),
      build_priority(RootId, Package, Priority)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(7, "OS mismatches").
#minimize{ 0@207: #true }.
#minimize{ 0@7: #true }.
#minimize{
    1@7+Priority,Package,Dependency,PSID
    : node_os_mismatch(PSID, Package, Dependency),
      build_priority(PSID, Package, Priority)
}.

opt_criterion(6, "non-preferred OS's").
#minimize{ 0@206: #true }.
#minimize{ 0@6: #true }.
#minimize{
    Weight@6+Priority,Package,PSID
    : node_os_weight(PSID, Package, Weight),
      build_priority(PSID, Package, Priority)
}.

% Choose more recent versions for nodes
opt_criterion(5, "version badness").
#minimize{ 0@205: #true }.
#minimize{ 0@5: #true }.
#minimize{
    Weight@5+Priority,Package,PSID
    : version_weight(PSID, Package, Weight),
      build_priority(PSID, Package, Priority)
}.

% Try to use all the default values of variants
opt_criterion(4, "default values of variants not being used (non-roots)").
#minimize{ 0@204: #true }.
#minimize{ 0@4: #true }.
#minimize{
    1@4+Priority,Package,Variant,Value,PSID
    : variant_default_not_used(PSID, Package, Variant, Value),
      not root(PSID, Package),
      build_priority(PSID, Package, Priority)
}.

% Try to use preferred compilers
opt_criterion(3, "non-preferred compilers").
#minimize{ 0@203: #true }.
#minimize{ 0@3: #true }.
#minimize{
    Weight@3+Priority,Package,PSID
    : compiler_weight(PSID, Package, Weight),
      build_priority(PSID, Package, Priority)
}.

% Minimize the number of mismatches for targets in the DAG, try
% to select the preferred target.
opt_criterion(2, "target mismatches").
#minimize{ 0@202: #true }.
#minimize{ 0@2: #true }.
#minimize{
    1@2+Priority,Package,Dependency,PSID
    : node_target_mismatch(PSID, Package, Dependency),
      build_priority(PSID, Package, Priority)
}.

opt_criterion(1, "non-preferred targets").
#minimize{ 0@201: #true }.
#minimize{ 0@1: #true }.
#minimize{
    Weight@1+Priority,Package,PSID
    : node_target_weight(PSID, Package, Weight),
      build_priority(PSID, Package, Priority)
}.

%-----------------
% Domain heuristic
%-----------------
#heuristic version(PSID, Package, Version) : version_declared(Package, Version, 0), node(PSID, Package). [10, true]
#heuristic version_weight(PSID, Package, 0) : version_declared(Package, Version, 0), node(PSID, Package). [10, true]
#heuristic node_target(PSID, Package, Target) : default_target_weight(Target, 0), node(PSID, Package). [10, true]
#heuristic node_target_weight(PSID, Package, 0) : node(PSID, Package). [10, true]
#heuristic variant_value(PSID, Package, Variant, Value) : variant_default_value(PSID, Package, Variant, Value), node(PSID, Package). [10, true]
#heuristic provider(PSID, Package, Virtual) : possible_provider_weight(PSID, Package, Virtual, 0, _), virtual_node(PSID, Virtual). [10, true]
#heuristic node(PSID, Package) : possible_provider_weight(PSID, Package, Virtual, 0, _), virtual_node(PSID, Virtual). [10, true]
