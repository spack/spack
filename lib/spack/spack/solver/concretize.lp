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
:- not 1 { version(Package, _) } 1, node(Package).

% each node must have a single platform, os and target
:- not 1 { node_platform(Package, _) } 1, node(Package), error("A node must have exactly one platform").
:- not 1 { node_os(Package, _) } 1, node(Package).
:- not 1 { node_target(Package, _) } 1, node(Package).

% each node has a single compiler associated with it
:- not 1 { node_compiler(Package, _) } 1, node(Package).
:- not 1 { node_compiler_version(Package, _, _) } 1, node(Package).

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
1 { version(Package, Version) : version_declared(Package, Version) } 1
 :- node(Package), error("Each node must have exactly one version").

% A virtual package may have or not a version, but never has more than one
:- virtual_node(Package), 2 { version(Package, _) }.

% If we select a deprecated version, mark the package as deprecated
deprecated(Package, Version) :- version(Package, Version), deprecated_version(Package, Version).

possible_version_weight(Package, Weight)
 :- version(Package, Version),
    version_declared(Package, Version, Weight).

1 { version_weight(Package, Weight) : possible_version_weight(Package, Weight) } 1 :- node(Package), error("Internal error: Package version must have a unique weight").

% version_satisfies implies that exactly one of the satisfying versions
% is the package's version, and vice versa.
1 { version(Package, Version) : version_satisfies(Package, Constraint, Version) } 1
  :- version_satisfies(Package, Constraint),
     error("no version satisfies the given constraints").
version_satisfies(Package, Constraint)
  :- version(Package, Version), version_satisfies(Package, Constraint, Version).

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
condition_holds(ID) :-
  condition(ID);
  attr(Name, A1)         : condition_requirement(ID, Name, A1);
  attr(Name, A1, A2)     : condition_requirement(ID, Name, A1, A2);
  attr(Name, A1, A2, A3) : condition_requirement(ID, Name, A1, A2, A3).

% condition_holds(ID) implies all imposed_constraints, unless do_not_impose(ID)
% is derived. This allows imposed constraints to be canceled in special cases.
impose(ID) :- condition_holds(ID), not do_not_impose(ID).

% conditions that hold impose constraints on other specs
attr(Name, A1)         :- impose(ID), imposed_constraint(ID, Name, A1).
attr(Name, A1, A2)     :- impose(ID), imposed_constraint(ID, Name, A1, A2).
attr(Name, A1, A2, A3) :- impose(ID), imposed_constraint(ID, Name, A1, A2, A3).

% we cannot have additional variant values when we are working with concrete specs
:- node(Package), hash(Package, Hash),
   variant_value(Package, Variant, Value),
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
% if a package is assigned a hash, it's concrete.
concrete(Package) :- hash(Package, _), node(Package).

%-----------------------------------------------------------------------------
% Dependency semantics
%-----------------------------------------------------------------------------
% Dependencies of any type imply that one package "depends on" another
depends_on(Package, Dependency) :- depends_on(Package, Dependency, _).

% a dependency holds if its condition holds and if it is not external or
% concrete. We chop off dependencies for externals, and dependencies of
% concrete specs don't need to be resolved -- they arise from the concrete
% specs themselves.
dependency_holds(Package, Dependency, Type) :-
  dependency_condition(ID, Package, Dependency),
  dependency_type(ID, Type),
  condition_holds(ID),
  build(Package),
  not external(Package).

% We cut off dependencies of externals (as we don't really know them).
% Don't impose constraints on dependencies that don't exist.
do_not_impose(ID) :-
  not dependency_holds(Package, Dependency, _),
  dependency_condition(ID, Package, Dependency).

% declared dependencies are real if they're not virtual AND
% the package is not an external.
% They're only triggered if the associated dependnecy condition holds.
depends_on(Package, Dependency, Type)
 :- dependency_holds(Package, Dependency, Type),
    not virtual(Dependency).

% every root must be a node
node(Package) :- root(Package).

% dependencies imply new nodes
node(Dependency) :- node(Package), depends_on(Package, Dependency).

% all nodes in the graph must be reachable from some root
% this ensures a user can't say `zlib ^libiconv` (neither of which have any
% dependencies) and get a two-node unconnected graph
needed(Package) :- root(Package).
needed(Dependency) :- needed(Package), depends_on(Package, Dependency).
:- node(Package), not needed(Package),
   error("All dependencies must be reachable from root").

% Avoid cycles in the DAG
% some combinations of conditional dependencies can result in cycles;
% this ensures that we solve around them
path(Parent, Child) :- depends_on(Parent, Child).
path(Parent, Descendant) :- path(Parent, A), depends_on(A, Descendant).
:- path(A, B), path(B, A), error("Cyclic dependencies are not allowed").

#defined error/1.

#defined dependency_type/2.
#defined dependency_condition/3.

%-----------------------------------------------------------------------------
% Conflicts
%-----------------------------------------------------------------------------
:- node(Package),
   conflict(Package, TriggerID, ConstraintID),
   condition_holds(TriggerID),
   condition_holds(ConstraintID),
   not external(Package),  % ignore conflicts for externals
   error("A conflict was triggered").

#defined conflict/3.

%-----------------------------------------------------------------------------
% Virtual dependencies
%-----------------------------------------------------------------------------

% if a package depends on a virtual, it's not external and we have a
% provider for that virtual then it depends on the provider
depends_on(Package, Provider, Type)
  :- dependency_holds(Package, Virtual, Type),
     provider(Provider, Virtual),
     not external(Package).

% dependencies on virtuals also imply that the virtual is a virtual node
virtual_node(Virtual)
  :- dependency_holds(Package, Virtual, Type),
     virtual(Virtual), not external(Package).

% If there's a virtual node, we must select one and only one provider.
% The provider must be selected among the possible providers.
1 { provider(Package, Virtual) : possible_provider(Package, Virtual) } 1
  :- virtual_node(Virtual), error("Virtual packages must be satisfied by a unique provider").

% virtual roots imply virtual nodes, and that one provider is a root
virtual_node(Virtual) :- virtual_root(Virtual).

% If we asked for a virtual root and we have a provider for that,
% then the provider is the root package.
root(Package) :- virtual_root(Virtual), provider(Package, Virtual).

% If we asked for a root package and that root provides a virtual,
% the root is a provider for that virtual. This rule is mostly relevant
% for environments that are concretized together (e.g. where we
% asks to install "mpich" and "hdf5+mpi" and we want "mpich" to
% be the mpi provider)
provider(Package, Virtual) :- node(Package), virtual_condition_holds(Package, Virtual).

% The provider provides the virtual if some provider condition holds.
virtual_condition_holds(Provider, Virtual) :-
   provider_condition(ID, Provider, Virtual),
   condition_holds(ID),
   virtual(Virtual).

% A package cannot be the actual provider for a virtual if it does not
% fulfill the conditions to provide that virtual
:- provider(Package, Virtual), not virtual_condition_holds(Package, Virtual),
   error("Internal error: virtual when provides not respected").

#defined possible_provider/2.

%-----------------------------------------------------------------------------
% Virtual dependency weights
%-----------------------------------------------------------------------------

% A provider may have different possible weights depending on whether it's an external
% or not, or on preferences expressed in packages.yaml etc. This rule ensures that
% we select the weight, among the possible ones, that minimizes the overall objective function.
1 { provider_weight(Dependency, Virtual, Weight, Reason) :
    possible_provider_weight(Dependency, Virtual, Weight, Reason) } 1
 :- provider(Dependency, Virtual), error("Internal error: package provider weights must be unique").

% Get rid or the reason for enabling the possible weight (useful for debugging)
provider_weight(Dependency, Virtual, Weight) :- provider_weight(Dependency, Virtual, Weight, _).

% A provider that is an external can use a weight of 0
possible_provider_weight(Dependency, Virtual, 0, "external")
  :- provider(Dependency, Virtual),
     external(Dependency).

% A provider mentioned in packages.yaml can use a weight
% according to its priority in the list of providers
possible_provider_weight(Dependency, Virtual, Weight, "packages_yaml")
  :- provider(Dependency, Virtual),
     depends_on(Package, Dependency),
     pkg_provider_preference(Package, Virtual, Dependency, Weight).

% A provider mentioned in the default configuration can use a weight
% according to its priority in the list of providers
possible_provider_weight(Dependency, Virtual, Weight, "default")
  :- provider(Dependency, Virtual),
     default_provider_preference(Virtual, Dependency, Weight).

% Any provider can use 100 as a weight, which is very high and discourage its use
possible_provider_weight(Dependency, Virtual, 100, "fallback") :- provider(Dependency, Virtual).

#defined possible_provider/2.
#defined provider_condition/3.
#defined required_provider_condition/3.
#defined required_provider_condition/4.
#defined required_provider_condition/5.

%-----------------------------------------------------------------------------
% Spec Attributes
%-----------------------------------------------------------------------------
% Equivalencies of the form:
%
%   name(Arg1, Arg2, ...) :- attr("name", Arg1, Arg2, ...).
%   attr("name", Arg1, Arg2, ...) :- name(Arg1, Arg2, ...).
%
% These allow us to easily define conditional dependency and conflict rules
% without enumerating all spec attributes every time.
node(Package)                          :- attr("node", Package).
hash(Package, Hash)                    :- attr("hash", Package, Hash).
version(Package, Version)              :- attr("version", Package, Version).
version_satisfies(Package, Constraint) :- attr("version_satisfies", Package, Constraint).
node_platform(Package, Platform)       :- attr("node_platform", Package, Platform).
node_os(Package, OS)                   :- attr("node_os", Package, OS).
node_target(Package, Target)           :- attr("node_target", Package, Target).
node_target_satisfies(Package, Target) :- attr("node_target_satisfies", Package, Target).
variant_value(Package, Variant, Value) :- attr("variant_value", Package, Variant, Value).
variant_set(Package, Variant, Value)   :- attr("variant_set", Package, Variant, Value).
node_flag(Package, FlagType, Flag)     :- attr("node_flag", Package, FlagType, Flag).
node_compiler(Package, Compiler)       :- attr("node_compiler", Package, Compiler).
depends_on(Package, Dependency, Type)  :- attr("depends_on", Package, Dependency, Type).
node_compiler_version(Package, Compiler, Version)
  :- attr("node_compiler_version", Package, Compiler, Version).
node_compiler_version_satisfies(Package, Compiler, Version)
  :- attr("node_compiler_version_satisfies", Package, Compiler, Version).

attr("node", Package)                          :- node(Package).
attr("hash", Package, Hash)                    :- hash(Package, Hash).
attr("version", Package, Version)              :- version(Package, Version).
attr("version_satisfies", Package, Constraint) :- version_satisfies(Package, Constraint).
attr("node_platform", Package, Platform)       :- node_platform(Package, Platform).
attr("node_os", Package, OS)                   :- node_os(Package, OS).
attr("node_target", Package, Target)           :- node_target(Package, Target).
attr("node_target_satisfies", Package, Target) :- node_target_satisfies(Package, Target).
attr("variant_value", Package, Variant, Value) :- variant_value(Package, Variant, Value).
attr("variant_set", Package, Variant, Value)   :- variant_set(Package, Variant, Value).
attr("node_flag", Package, FlagType, Flag)     :- node_flag(Package, FlagType, Flag).
attr("node_compiler", Package, Compiler)       :- node_compiler(Package, Compiler).
attr("depends_on", Package, Dependency, Type)  :- depends_on(Package, Dependency, Type).
attr("node_compiler_version", Package, Compiler, Version)
  :- node_compiler_version(Package, Compiler, Version).
attr("node_compiler_version_satisfies", Package, Compiler, Version)
  :- node_compiler_version_satisfies(Package, Compiler, Version).

% do not warn if generated program contains none of these.
#defined depends_on/3.
#defined declared_dependency/3.
#defined virtual/1.
#defined virtual_node/1.
#defined virtual_root/1.
#defined virtual_condition_holds/2.
#defined external/1.
#defined external_spec/2.
#defined external_version_declared/4.
#defined external_only/1.
#defined pkg_provider_preference/4.
#defined default_provider_preference/3.
#defined version_satisfies/2.
#defined node_compiler_version_satisfies/3.
#defined root/1.

%-----------------------------------------------------------------------------
% External semantics
%-----------------------------------------------------------------------------

% if a package is external its version must be one of the external versions
1 { external_version(Package, Version, Weight):
    version_declared(Package, Version, Weight, "external") } 1
    :- external(Package), error("External package version does not satisfy external spec").

version_weight(Package, Weight) :- external_version(Package, Version, Weight).
version(Package, Version) :- external_version(Package, Version, Weight).

% if a package is not buildable (external_only), only externals are allowed
external(Package) :- external_only(Package), node(Package).

% a package is a real_node if it is not external
real_node(Package) :- node(Package), not external(Package).

% a package is external if we are using an external spec for it
external(Package) :- external_spec_selected(Package, _).

% we can't use the weight for an external version if we don't use the
% corresponding external spec.
:- version(Package, Version),
   version_weight(Package, Weight),
   version_declared(Package, Version, Weight, "external"),
   not external(Package),
   error("Internal error: external weight used for internal spec").

% determine if an external spec has been selected
external_spec_selected(Package, LocalIndex) :-
    external_conditions_hold(Package, LocalIndex),
    node(Package).

external_conditions_hold(Package, LocalIndex) :-
    possible_external(ID, Package, LocalIndex), condition_holds(ID).

% it cannot happen that a spec is external, but none of the external specs
% conditions hold.
:- external(Package), not external_conditions_hold(Package, _),
   error("External package does not satisfy external spec").

#defined possible_external/3.
#defined external_spec_index/3.
#defined external_spec_condition/3.
#defined external_spec_condition/4.
#defined external_spec_condition/5.

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------
% a variant is a variant of a package if it is a variant under some condition
% and that condition holds
variant(Package, Variant) :- variant_condition(ID, Package, Variant),
                             condition_holds(ID).

% a variant cannot be set if it is not a variant on the package
:- variant_set(Package, Variant),
   not variant(Package, Variant),
   build(Package),
   error("Unsatisfied conditional variants cannot be set").

% a variant cannot take on a value if it is not a variant of the package
:- variant_value(Package, Variant, _),
   not variant(Package, Variant),
   build(Package),
   error("Unsatisfied conditional variants cannot take on a variant value").

% if a variant is sticky and not set its value is the default value
variant_value(Package, Variant, Value) :-
  variant(Package, Variant),
  not variant_set(Package, Variant),
  variant_sticky(Package, Variant),
  variant_default_value(Package, Variant, Value),
  build(Package).

% one variant value for single-valued variants.
1 {
  variant_value(Package, Variant, Value)
  : variant_possible_value(Package, Variant, Value)
} 1
 :- node(Package),
    variant(Package, Variant),
    variant_single_value(Package, Variant),
    build(Package),
    error("Single valued variants must have a single value").

% at least one variant value for multi-valued variants.
1 {
 variant_value(Package, Variant, Value)
 : variant_possible_value(Package, Variant, Value)
}
 :- node(Package),
    variant(Package, Variant),
    not variant_single_value(Package, Variant),
    build(Package),
    error("Internal error: All variants must have a value").

% if a variant is set to anything, it is considered 'set'.
variant_set(Package, Variant) :- variant_set(Package, Variant, _).

% A variant cannot have a value that is not also a possible value
% This only applies to packages we need to build -- concrete packages may
% have been built w/different variants from older/different package versions.
:- variant_value(Package, Variant, Value),
   not variant_possible_value(Package, Variant, Value),
   build(Package),
   error("Variant set to invalid value").

% Some multi valued variants accept multiple values from disjoint sets.
% Ensure that we respect that constraint and we don't pick values from more
% than one set at once
:- variant_value(Package, Variant, Value1),
   variant_value(Package, Variant, Value2),
   variant_value_from_disjoint_sets(Package, Variant, Value1, Set1),
   variant_value_from_disjoint_sets(Package, Variant, Value2, Set2),
   Set1 < Set2,
   build(Package),
   error("Variant values selected from multiple disjoint sets").

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(Package, Variant, Value)
 :- node(Package),
    variant(Package, Variant),
    variant_set(Package, Variant, Value).

% The rules below allow us to prefer default values for variants
% whenever possible. If a variant is set in a spec, or if it is
% specified in an external, we score it as if it was a default value.
variant_not_default(Package, Variant, Value)
 :- variant_value(Package, Variant, Value),
    not variant_default_value(Package, Variant, Value),
    % variants set explicitly on the CLI don't count as non-default
    not variant_set(Package, Variant, Value),
    % variants set on externals that we could use don't count as non-default
    % this makes spack prefer to use an external over rebuilding with the
    % default configuration
    not external_with_variant_set(Package, Variant, Value),
    node(Package).


% A default variant value that is not used
variant_default_not_used(Package, Variant, Value)
  :- variant_default_value(Package, Variant, Value),
     not variant_value(Package, Variant, Value),
     node(Package).

% The variant is set in an external spec
external_with_variant_set(Package, Variant, Value)
 :- variant_value(Package, Variant, Value),
    condition_requirement(ID, "variant_value", Package, Variant, Value),
    possible_external(ID, Package, _),
    external(Package),
    node(Package).

% The default value for a variant in a package is what is prescribed:
%
% 1. On the command line
% 2. In packages.yaml (if there's no command line settings)
% 3. In the package.py file (if there are no settings in
%    packages.yaml and the command line)
%
variant_default_value(Package, Variant, Value)
 :- variant_default_value_from_package_py(Package, Variant, Value),
    not variant_default_value_from_packages_yaml(Package, Variant, _),
    not variant_default_value_from_cli(Package, Variant, _).

variant_default_value(Package, Variant, Value)
 :- variant_default_value_from_packages_yaml(Package, Variant, Value),
    not variant_default_value_from_cli(Package, Variant, _).

variant_default_value(Package, Variant, Value) :- variant_default_value_from_cli(Package, Variant, Value).

% Treat 'none' in a special way - it cannot be combined with other
% values even if the variant is multi-valued
:- 2 {
     variant_value(Package, Variant, Value) : variant_possible_value(Package, Variant, Value)
   },
   variant_value(Package, Variant, "none"),
   build(Package),
   error("Variant value 'none' cannot be combined with any other value").

% patches and dev_path are special variants -- they don't have to be
% declared in the package, so we just allow them to spring into existence
% when assigned a value.
auto_variant("dev_path").
auto_variant("patches").
variant(Package, Variant)
  :- variant_set(Package, Variant, _), auto_variant(Variant).
variant_single_value(Package, "dev_path")
  :- variant_set(Package, "dev_path", _).

% suppress warnings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant/2.
#defined variant_sticky/2.
#defined variant_set/3.
#defined variant_condition/3.
#defined variant_single_value/2.
#defined variant_default_value/3.
#defined variant_possible_value/3.
#defined variant_default_value_from_cli/3.
#defined variant_default_value_from_packages_yaml/3.
#defined variant_default_value_from_package_py/3.
#defined variant_value_from_disjoint_sets/4.

%-----------------------------------------------------------------------------
% Platform semantics
%-----------------------------------------------------------------------------

% if no platform is set, fall back to the default
node_platform(Package, Platform)
 :- node(Package),
    not node_platform_set(Package),
    node_platform_default(Platform).

% setting platform on a node is a hard constraint
node_platform(Package, Platform)
 :- node(Package), node_platform_set(Package, Platform).

% platform is set if set to anything
node_platform_set(Package) :- node_platform_set(Package, _).

#defined node_platform_set/2.  % avoid warnings

%-----------------------------------------------------------------------------
% OS semantics
%-----------------------------------------------------------------------------
% convert weighted OS declarations to simple one
os(OS) :- os(OS, _).

% one os per node
1 { node_os(Package, OS) : os(OS) } 1 :-
   node(Package), error("Each node must have exactly one OS").

% can't have a non-buildable OS on a node we need to build
:- build(Package), node_os(Package, OS), not buildable_os(OS),
   error("No available OS can be built for").

% can't have dependencies on incompatible OS's
:- depends_on(Package, Dependency),
   node_os(Package, PackageOS),
   node_os(Dependency, DependencyOS),
   not os_compatible(PackageOS, DependencyOS),
   build(Package),
   error("Dependencies must have compatible OS's with their dependents").

% give OS choice weights according to os declarations
node_os_weight(Package, Weight)
 :- node(Package),
    node_os(Package, OS),
    os(OS, Weight).

% match semantics for OS's
node_os_match(Package, Dependency) :-
   depends_on(Package, Dependency), node_os(Package, OS), node_os(Dependency, OS).
node_os_mismatch(Package, Dependency) :-
   depends_on(Package, Dependency), not node_os_match(Package, Dependency).

% every OS is compatible with itself. We can use `os_compatible` to declare
os_compatible(OS, OS) :- os(OS).

% OS compatibility rules for reusing solves.
% catalina binaries can be used on bigsur. Direction is package -> dependency.
os_compatible("bigsur", "catalina").

% If an OS is set explicitly respect the value
node_os(Package, OS) :- node_os_set(Package, OS), node(Package).

#defined node_os_set/2.
#defined os_compatible/2.

%-----------------------------------------------------------------------------
% Target semantics
%-----------------------------------------------------------------------------

% Each node has only one target chosen among the known targets
1 { node_target(Package, Target) : target(Target) } 1 :- node(Package), error("Each node must have exactly one target").

% If a node must satisfy a target constraint the choice is reduced among the targets
% that satisfy that constraint
1 { node_target(Package, Target) : target_satisfies(Constraint, Target) } 1
  :- node_target_satisfies(Package, Constraint), error("Each node must have exactly one target").

% If a node has a target and the target satisfies a constraint, then the target
% associated with the node satisfies the same constraint
node_target_satisfies(Package, Constraint)
  :- node_target(Package, Target), target_satisfies(Constraint, Target).

% If a node has a target, all of its dependencies must be compatible with that target
:- depends_on(Package, Dependency),
   node_target(Package, ParentT),
   node_target(Dependency, ChildT),
   not target_compatible(ParentT, ChildT),
   error("Dependency node targets must be compatible with dependent targets").

% target_compatible(T1, T2) means code for T2 can run on T1
% This order is dependent -> dependency in the node DAG, which
% is contravariant with the target DAG.
target_compatible(Target, Target) :- target(Target).
target_compatible(Child, Parent) :- target_parent(Child, Parent).
target_compatible(Descendent, Ancestor)
  :- target_parent(Target, Ancestor),
     target_compatible(Descendent, Target),
     target(Target).

#defined target_satisfies/2.
#defined target_parent/2.

% The target weight is either the default target weight
% or a more specific per-package weight if set
target_weight(Target, Package, Weight)
  :- default_target_weight(Target, Weight),
     node(Package),
     not derive_target_from_parent(_, Package),
     not package_target_weight(Target, Package, _).

% TODO: Need to account for the case of more than one parent
% TODO: each of which sets different targets
target_weight(Target, Dependency, Weight)
  :- depends_on(Package, Dependency),
     derive_target_from_parent(Package, Dependency),
     target_weight(Target, Package, Weight).

target_weight(Target, Package, Weight)
  :- package_target_weight(Target, Package, Weight).

% can't use targets on node if the compiler for the node doesn't support them
:- node_target(Package, Target),
   not compiler_supports_target(Compiler, Version, Target),
   node_compiler(Package, Compiler),
   node_compiler_version(Package, Compiler, Version),
   build(Package),
   error("No satisfying compiler available is compatible with a satisfying target").

% if a target is set explicitly, respect it
node_target(Package, Target)
 :- node(Package), node_target_set(Package, Target).

% each node has the weight of its assigned target
node_target_weight(Package, Weight)
 :- node(Package),
    node_target(Package, Target),
    target_weight(Target, Package, Weight).

derive_target_from_parent(Parent, Package)
  :- depends_on(Parent, Package),
     not package_target_weight(_, Package, _).

% compatibility rules for targets among nodes
node_target_match(Parent, Dependency)
  :- depends_on(Parent, Dependency),
     node_target(Parent, Target),
     node_target(Dependency, Target).

node_target_mismatch(Parent, Dependency)
  :- depends_on(Parent, Dependency),
     not node_target_match(Parent, Dependency).

% disallow reusing concrete specs that don't have a compatible target
:- node(Package), node_target(Package, Target), not target(Target),
   error("No satisfying package's target is compatible with this machine").

#defined node_target_set/2.
#defined package_target_weight/3.

%-----------------------------------------------------------------------------
% Compiler semantics
%-----------------------------------------------------------------------------
compiler(Compiler) :- compiler_version(Compiler, _).

% There must be only one compiler set per built node. The compiler
% is chosen among available versions.
1 { node_compiler_version(Package, Compiler, Version) : compiler_version(Compiler, Version) } 1 :-
    node(Package),
    build(Package),
    error("Each node must have exactly one compiler").

% Sometimes we just need to know the compiler and not the version
node_compiler(Package, Compiler) :- node_compiler_version(Package, Compiler, _).

% We can't have a compiler be enforced and select the version from another compiler
:- node_compiler(Package, Compiler1),
   node_compiler_version(Package, Compiler2, _),
   Compiler1 != Compiler2,
   error("Internal error: mismatch between selected compiler and compiler version").

% If the compiler of a node must satisfy a constraint, then its version
% must be chosen among the ones that satisfy said constraint
1 { node_compiler_version(Package, Compiler, Version)
    : compiler_version_satisfies(Compiler, Constraint, Version) } 1 :-
    node_compiler_version_satisfies(Package, Compiler, Constraint),
    error("Internal error: node compiler version mismatch").

% If the node is associated with a compiler and the compiler satisfy a constraint, then
% the compiler associated with the node satisfy the same constraint
node_compiler_version_satisfies(Package, Compiler, Constraint)
  :- node_compiler_version(Package, Compiler, Version),
     compiler_version_satisfies(Compiler, Constraint, Version),
     build(Package).

#defined compiler_version_satisfies/3.

% If the compiler version was set from the command line,
% respect it verbatim
node_compiler_version(Package, Compiler, Version) :- node_compiler_version_set(Package, Compiler, Version).

% Cannot select a compiler if it is not supported on the OS
% Compilers that are explicitly marked as allowed
% are excluded from this check
:- node_compiler_version(Package, Compiler, Version), node_os(Package, OS),
   not compiler_supports_os(Compiler, Version, OS),
   not allow_compiler(Compiler, Version),
   build(Package),
   error("No satisfying compiler available is compatible with a satisfying os").

% If a package and one of its dependencies don't have the
% same compiler there's a mismatch.
compiler_match(Package, Dependency)
  :- depends_on(Package, Dependency),
     node_compiler_version(Package, Compiler, Version),
     node_compiler_version(Dependency, Compiler, Version).

compiler_mismatch(Package, Dependency)
  :- depends_on(Package, Dependency),
     not compiler_match(Package, Dependency).

#defined node_compiler_set/2.
#defined node_compiler_version_set/3.
#defined compiler_supports_os/3.
#defined allow_compiler/2.

% compilers weighted by preference according to packages.yaml
compiler_weight(Package, Weight)
 :- node_compiler_version(Package, Compiler, V),
    node_compiler_preference(Package, Compiler, V, Weight).
compiler_weight(Package, Weight)
 :- node_compiler_version(Package, Compiler, V),
    not node_compiler_preference(Package, Compiler, V, _),
    default_compiler_preference(Compiler, V, Weight).
compiler_weight(Package, 100)
 :- node_compiler_version(Package, Compiler, Version),
    not node_compiler_preference(Package, Compiler, Version, _),
    not default_compiler_preference(Compiler, Version, _).

#defined node_compiler_preference/4.
#defined default_compiler_preference/3.

%-----------------------------------------------------------------------------
% Compiler flags
%-----------------------------------------------------------------------------
% propagate flags when compilers match
inherit_flags(Package, Dependency)
 :- depends_on(Package, Dependency),
    node_compiler(Package, Compiler),
    node_compiler(Dependency, Compiler),
    compiler(Compiler), flag_type(FlagType).
node_flag_inherited(Dependency, FlagType, Flag)
 :- node_flag_set(Package, FlagType, Flag), inherit_flags(Package, Dependency).
node_flag_inherited(Dependency, FlagType, Flag)
 :- node_flag_inherited(Package, FlagType, Flag),
    inherit_flags(Package, Dependency).

% node with flags set to anythingg is "set"
node_flag_set(Package) :- node_flag_set(Package, _, _).

% remember where flags came from
node_flag_source(Package, Package) :- node_flag_set(Package).
node_flag_source(Dependency, Q)
 :- node_flag_source(Package, Q), inherit_flags(Package, Dependency).

% compiler flags from compilers.yaml are put on nodes if compiler matches
node_flag(Package, FlagType, Flag)
 :- not node_flag_set(Package),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    node_compiler_version(Package, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

node_flag_compiler_default(Package)
 :- not node_flag_set(Package),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    node_compiler_version(Package, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

% if a flag is set to something or inherited, it's included
node_flag(Package, FlagType, Flag) :- node_flag_set(Package, FlagType, Flag).
node_flag(Package, FlagType, Flag)
 :- node_flag_inherited(Package, FlagType, Flag).

% if no node flags are set for a type, there are no flags.
no_flags(Package, FlagType)
 :- not node_flag(Package, FlagType, _), node(Package), flag_type(FlagType).

#defined compiler_version_flag/4.
#defined node_flag/3.
#defined node_flag_set/3.


%-----------------------------------------------------------------------------
% Installed packages
%-----------------------------------------------------------------------------
% the solver is free to choose at most one installed hash for each package
{ hash(Package, Hash) : installed_hash(Package, Hash) } 1
 :- node(Package), error("Internal error: package must resolve to at most one hash").

% if a hash is selected, we impose all the constraints that implies
impose(Hash) :- hash(Package, Hash).

% if we haven't selected a hash for a package, we'll be building it
build(Package) :- not hash(Package, _), node(Package).

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
%   200+        Shifted priorities for build nodes; correspond to priorities 0 - 99.
%   100 - 199   Unshifted priorities. Currently only includes minimizing #builds.
%   0   -  99   Priorities for non-built nodes.
build_priority(Package, 200) :- build(Package), node(Package).
build_priority(Package, 0)   :- not build(Package), node(Package).

#defined installed_hash/2.

%-----------------------------------------------------------------------------
% How to optimize the spec (high to low priority)
%-----------------------------------------------------------------------------
% Each criterion below has:
%   1. an opt_criterion(ID, Name) fact that describes the criterion, and
%   2. a `#minimize{ 0@2 : #true }.` statement that ensures the criterion
%      is displayed (clingo doesn't display sums over empty sets by default)

% Try hard to reuse installed packages (i.e., minimize the number built)
opt_criterion(100, "number of packages to build (vs. reuse)").
#minimize { 0@100: #true }.
#minimize { 1@100,Package : build(Package), optimize_for_reuse() }.
#defined optimize_for_reuse/0.

% Minimize the number of deprecated versions being used
opt_criterion(15, "deprecated versions used").
#minimize{ 0@215: #true }.
#minimize{ 0@15: #true }.
#minimize{
    1@15+Priority,Package
    : deprecated(Package, _),
      build_priority(Package, Priority)
}.

% Minimize the:
% 1. Version weight
% 2. Number of variants with a non default value, if not set
% for the root(Package)
opt_criterion(14, "version weight").
#minimize{ 0@214: #true }.
#minimize{ 0@14: #true }.
#minimize {
    Weight@14+Priority
    : root(Package),version_weight(Package, Weight),
      build_priority(Package, Priority)
}.

opt_criterion(13, "number of non-default variants (roots)").
#minimize{ 0@213: #true }.
#minimize{ 0@13: #true }.
#minimize {
    1@13+Priority,Package,Variant,Value
    : variant_not_default(Package, Variant, Value),
      root(Package),
      build_priority(Package, Priority)
}.

opt_criterion(12, "preferred providers for roots").
#minimize{ 0@212 : #true }.
#minimize{ 0@12: #true }.
#minimize{
    Weight@12+Priority,Provider,Virtual
    : provider_weight(Provider, Virtual, Weight),
      root(Provider),
      build_priority(Provider, Priority)
}.

opt_criterion(11, "default values of variants not being used (roots)").
#minimize{ 0@211: #true }.
#minimize{ 0@11: #true }.
#minimize{
    1@11+Priority,Package,Variant,Value
    : variant_default_not_used(Package, Variant, Value),
      root(Package),
      build_priority(Package, Priority)
}.

% Try to use default variants or variants that have been set
opt_criterion(10, "number of non-default variants (non-roots)").
#minimize{ 0@210: #true }.
#minimize{ 0@10: #true }.
#minimize {
    1@10+Priority,Package,Variant,Value
    : variant_not_default(Package, Variant, Value),
      not root(Package),
      build_priority(Package, Priority)
}.

% Minimize the weights of the providers, i.e. use as much as
% possible the most preferred providers
opt_criterion(9, "preferred providers (non-roots)").
#minimize{ 0@209: #true }.
#minimize{ 0@9: #true }.
#minimize{
    Weight@9+Priority,Provider,Virtual
    : provider_weight(Provider, Virtual, Weight), not root(Provider),
      build_priority(Provider, Priority)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(8, "compiler mismatches").
#minimize{ 0@208: #true }.
#minimize{ 0@8: #true }.
#minimize{
    1@8+Priority,Package,Dependency
    : compiler_mismatch(Package, Dependency),
      build_priority(Package, Priority)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(7, "OS mismatches").
#minimize{ 0@207: #true }.
#minimize{ 0@7: #true }.
#minimize{
    1@7+Priority,Package,Dependency
    : node_os_mismatch(Package, Dependency),
      build_priority(Package, Priority)
}.

opt_criterion(6, "non-preferred OS's").
#minimize{ 0@206: #true }.
#minimize{ 0@6: #true }.
#minimize{
    Weight@6+Priority,Package
    : node_os_weight(Package, Weight),
      build_priority(Package, Priority)
}.

% Choose more recent versions for nodes
opt_criterion(5, "version badness").
#minimize{ 0@205: #true }.
#minimize{ 0@5: #true }.
#minimize{
    Weight@5+Priority,Package
    : version_weight(Package, Weight),
      build_priority(Package, Priority)
}.

% Try to use all the default values of variants
opt_criterion(4, "default values of variants not being used (non-roots)").
#minimize{ 0@204: #true }.
#minimize{ 0@4: #true }.
#minimize{
    1@4+Priority,Package,Variant,Value
    : variant_default_not_used(Package, Variant, Value),
      not root(Package),
      build_priority(Package, Priority)
}.

% Try to use preferred compilers
opt_criterion(3, "non-preferred compilers").
#minimize{ 0@203: #true }.
#minimize{ 0@3: #true }.
#minimize{
    Weight@3+Priority,Package
    : compiler_weight(Package, Weight),
      build_priority(Package, Priority)
}.

% Minimize the number of mismatches for targets in the DAG, try
% to select the preferred target.
opt_criterion(2, "target mismatches").
#minimize{ 0@202: #true }.
#minimize{ 0@2: #true }.
#minimize{
    1@2+Priority,Package,Dependency
    : node_target_mismatch(Package, Dependency),
      build_priority(Package, Priority)
}.

opt_criterion(1, "non-preferred targets").
#minimize{ 0@201: #true }.
#minimize{ 0@1: #true }.
#minimize{
    Weight@1+Priority,Package
    : node_target_weight(Package, Weight),
      build_priority(Package, Priority)
}.

%-----------------
% Domain heuristic
%-----------------
#heuristic version(Package, Version) : version_declared(Package, Version, 0), node(Package). [10, true]
#heuristic version_weight(Package, 0) : version_declared(Package, Version, 0), node(Package). [10, true]
#heuristic node_target(Package, Target) : default_target_weight(Target, 0), node(Package). [10, true]
#heuristic node_target_weight(Package, 0) : node(Package). [10, true]
#heuristic variant_value(Package, Variant, Value) : variant_default_value(Package, Variant, Value), node(Package). [10, true]
#heuristic provider(Package, Virtual) : possible_provider_weight(Package, Virtual, 0, _), virtual_node(Virtual). [10, true]
#heuristic node(Package) : possible_provider_weight(Package, Virtual, 0, _), virtual_node(Virtual). [10, true]
