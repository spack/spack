% Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% This logic program implements Spack's concretizer
%=============================================================================

%-----------------------------------------------------------------------------
% Map literal input specs to facts that drive the solve
%-----------------------------------------------------------------------------

% Give clingo the choice to solve an input spec or not
{ literal_solved(ID) } :- literal(ID).
literal_not_solved(ID) :- not literal_solved(ID), literal(ID).

% If concretize_everything() is a fact, then we cannot have unsolved specs
:- literal_not_solved(ID), concretize_everything.

% Make a problem with "zero literals solved" unsat. This is to trigger
% looking for solutions to the ASP problem with "errors", which results
% in better reporting for users. See #30669 for details.
1 { literal_solved(ID) : literal(ID) }.

opt_criterion(300, "number of input specs not concretized").
#minimize{ 0@300: #true }.
#minimize { 1@300,ID : literal_not_solved(ID) }.

% TODO GBB: This assumes build deps from CLI go in PSID=0

% Map constraint on the literal ID to the correct PSID
attr(Name, A1, 0)             :- literal(LiteralID, Name, A1), literal_solved(LiteralID).
attr(Name, A1, 0, A2)         :- literal(LiteralID, Name, A1, A2), literal_solved(LiteralID).
attr(Name, A1, 0, A2, A3)     :- literal(LiteralID, Name, A1, A2, A3), literal_solved(LiteralID).
attr(Name, A1, 0, A2, A3, A4) :- literal(LiteralID, Name, A1, A2, A3, A4), literal_solved(LiteralID).
attr(Name, A1, 0, A2, A3, A4, A5) :- literal(LiteralID, Name, A1, A2, A3, A4, A5), literal_solved(LiteralID).

#defined concretize_everything/0.
#defined literal/1.
#defined literal/3.
#defined literal/4.
#defined literal/5.
#defined literal/6.
#defined literal/7.

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
   internal_error("Two versions with identical weights").

% We cannot use a version declared for an installed package if we end up building it
:- version_declared(Package, Version, Weight, "installed"),
   attr("version", Package, PSID, Version),
   version_weight(Package, PSID, Weight),
   not attr("hash", Package, PSID, _),
   internal_error("Reuse version weight used for built package").

% versions are declared w/priority -- declared with priority implies declared
version_declared(Package, Version) :- version_declared(Package, Version, _).

% a spec with a git hash version is equivalent to one with the same matched version
version_satisfies(Package, Constraint, HashVersion) :- version_satisfies(Package, Constraint, EquivalentVersion),
  version_equivalent(Package, HashVersion, EquivalentVersion).
#defined version_equivalent/3.

% If something is a package, it has only one version and that must be a
% declared version.
% We allow clingo to choose any version(s), and infer an error if there
% is not precisely one version chosen. Error facts are heavily optimized
% against to ensure they cannot be inferred when a non-error solution is
% possible
{ attr("version", Package, PSID, Version) : version_declared(Package, Version) }
 :- attr("node", Package, PSID).
error(2, "No version for '{0}' satisfies '@{1}' and '@{2}'", Package, Version1, Version2)
  :- attr("node", Package, PSID),
     attr("version", Package, PSID, Version1),
     attr("version", Package, PSID, Version2),
     Version1 < Version2.  % see[1]

error(2, "No versions available for package '{0}'", Package)
  :- attr("node", Package, PSID), not attr("version", Package, PSID, _).

% A virtual package may or may not have a version, but never has more than one
error(2, "No version for '{0}' satisfies '@{1}' and '@{2}'", Virtual, Version1, Version2)
  :- attr("virtual_node", Virtual, PSID),
     attr("version", Virtual, PSID, Version1),
     attr("version", Virtual, PSID, Version2),
     Version1 < Version2. % see[1]

% If we select a deprecated version, mark the package as deprecated
attr("deprecated", Package, PSID, Version) :-
     attr("version", Package, PSID, Version),
     deprecated_version(Package, Version).

possible_version_weight(Package, PSID, Weight)
 :- attr("version", Package, PSID, Version),
    version_declared(Package, Version, Weight).

% we can't use the weight for an external version if we don't use the
% corresponding external spec.
:- attr("version", Package, PSID, Version),
   version_weight(Package, PSID, Weight),
   version_declared(Package, Version, Weight, "external"),
   not external(Package, PSID),
   internal_error("External weight used for built package").

% we can't use a weight from an installed spec if we are building it
% and vice-versa
:- attr("version", Package, PSID, Version),
   version_weight(Package, PSID, Weight),
   version_declared(Package, Version, Weight, "installed"),
   build(Package, PSID),
   internal_error("Reuse version weight used for build package").

:- attr("version", Package, PSID, Version),
   version_weight(Package, PSID, Weight),
   not version_declared(Package, Version, Weight, "installed"),
   not build(Package, PSID),
   internal_error("Build version weight used for reused package").

1 { version_weight(Package, PSID, Weight) : version_declared(Package, Version, Weight) } 1
  :- attr("version", Package, PSID, Version),
     attr("node", Package, PSID).

% node_version_satisfies implies that exactly one of the satisfying versions
% is the package's version, and vice versa.
% While this choice rule appears redundant with the initial choice rule for
% versions, virtual nodes with version constraints require this rule to be
% able to choose versions
{ attr("version", Package, PSID, Version) : version_satisfies(Package, Constraint, Version) }
  :- attr("node_version_satisfies", Package, PSID, Constraint).

% If there is at least a version that satisfy the constraint, impose a lower
% bound on the choice rule to avoid false positives with the error below
1 { attr("version", Package, PSID, Version) : version_satisfies(Package, Constraint, Version) }
  :- attr("node_version_satisfies", Package, PSID, Constraint),
     version_satisfies(Package, Constraint, _).

% More specific error message if the version cannot satisfy some constraint
% Otherwise covered by `no_version_error` and `versions_conflict_error`.
error(1, "No valid version for '{0}' satisfies '@{1}'", Package, Constraint)
  :- attr("node_version_satisfies", Package, PSID, Constraint),
     C = #count{ Version : attr("version", Package, PSID, Version), version_satisfies(Package, Constraint, Version)},
     C < 1.

attr("node_version_satisfies", Package, PSID, Constraint)
  :- attr("version", Package, PSID, Version), version_satisfies(Package, Constraint, Version).

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
condition_holds(ID, PSID) :-
  condition(ID, _);
  psid(PSID);
  attr(Name, A1, PSID)                 : condition_requirement(ID, Name, A1);
  attr(Name, A1, PSID, A2)             : condition_requirement(ID, Name, A1, A2);
  attr(Name, A1, PSID, A2, A3)         : condition_requirement(ID, Name, A1, A2, A3);
  attr(Name, A1, PSID, A2, A3, A4)     : condition_requirement(ID, Name, A1, A2, A3, A4);
  attr(Name, A1, PSID, A2, A3, A4, A5) : condition_requirement(ID, Name, A1, A2, A3, A4, A5).

psid(0).
%psid(1).

% condition_holds(ID) implies all imposed_constraints, unless do_not_impose(ID)
% is derived. This allows imposed constraints to be canceled in special cases.
impose(ID, PSID) :- imposed_psid(ID, PSID), not do_not_impose(ID, PSID).

% conditions that hold impose constraints on other specs
attr(Name, A1, PSID)                 :- impose(ID, PSID), imposed_constraint(ID, Name, A1).
attr(Name, A1, PSID, A2)             :- impose(ID, PSID), imposed_constraint(ID, Name, A1, A2).
attr(Name, A1, PSID, A2, A3)         :- impose(ID, PSID), imposed_constraint(ID, Name, A1, A2, A3).
attr(Name, A1, PSID, A2, A3, A4)     :- impose(ID, PSID), imposed_constraint(ID, Name, A1, A2, A3, A4).
attr(Name, A1, PSID, A2, A3, A4, A5) :- impose(ID, PSID), imposed_constraint(ID, Name, A1, A2, A3, A4, A5).

% we cannot have additional variant values when we are working with concrete specs
:- attr("node", Package, PSID), attr("hash", Package, PSID, Hash),
   attr("variant_value", Package, PSID, Variant, Value),
   not imposed_constraint(Hash, "variant_value", Package, Variant, Value),
   internal_error("imposed hash without imposing all variant values").

% we cannot have additional flag values when we are working with concrete specs
:- attr("node", Package, PSID), attr("hash", Package, PSID, Hash),
   attr("node_flag", Package, PSID, FlagType, Flag),
   not imposed_constraint(Hash, "node_flag", Package, FlagType, Flag),
   internal_error("imposed hash without imposing all flag values").

#defined condition/2.
#defined condition_requirement/3.
#defined condition_requirement/4.
#defined condition_requirement/5.
#defined condition_requirement/6.
#defined condition_requirement/7.
#defined imposed_constraint/3.
#defined imposed_constraint/4.
#defined imposed_constraint/5.
#defined imposed_constraint/6.
#defined imposed_constraint/7.

%-----------------------------------------------------------------------------
% Dependency semantics
%-----------------------------------------------------------------------------
% Dependencies of any type imply that one package "depends on" another
depends_on(Package, PSID1, Dependency, PSID2) :- attr("depends_on", Package, PSID1, Dependency, PSID2, _).

attr("depends_on", Package, PSID, Dependency, PSID, Type)
 :- depends_on_unknown(Package, PSID, Dependency, Type),
    Type != "build".

% TODO GBB how do we associate the imposed constraints on deps with their psids
% since this allows them to pick new ones
1 { attr("depends_on", Package, PSID1, Dependency, PSID2, "build") : psid(PSID2) } 1
 :- depends_on_unknown(Package, PSID1, Dependency, "build"),
    C = #count{ Type: depends_on_unknown(Package, PSID1, Depenency, Type) },
    C = 1,
    internal_error("not enough process spaces for reused hashes").

#defined depends_on_unknown/4.

% a dependency holds if its condition holds and if it is not external or
% concrete. We chop off dependencies for externals, and dependencies of
% concrete specs don't need to be resolved -- they arise from the concrete
% specs themselves.
dependency_holds(Package, PSID, Dependency, PSID, Type) :-
  dependency_condition(ID, Package, Dependency),
  dependency_type(ID, Type),
  build(Package, PSID),
  not external(Package, PSID),
  condition_holds(ID, PSID),
  Type != "build".

% If it holds as a build dep and as another dep, we keep it in one PSID
dependency_holds(Package, PSID, Dependency, PSID, "build") :-
  dependency_condition(ID, Package, Dependency),
  dependency_type(ID, "build"),
  dependency_type(ID, Type),
  Type != "build",
  build(Package, PSID),
  not external(Package, PSID),
  condition_holds(ID, PSID).

1 { dependency_holds(Package, PSID, Dependency, PSID2, "build") : psid(PSID2) } 1
 :- dependency_condition(ID, Package, Dependency),
    dependency_type(ID, "build"),
    build(Package, PSID),
    not external(Package, PSID),
    condition_holds(ID, PSID),
    C = #count{ Type : dependency_type(ID, Type) },
    C = 1,
    internal_error("Not enough process spaces"). % this is only a build dep, otherwise we unify it for now

% TODO GBB: split nodes for build+run or build+link deps

% track which process space a condition imposes on
imposed_psid(ID, PSID) :- psid_boundary(ID, PSID).

imposed_psid(ID, PSID) :- condition_holds(ID, PSID), not psid_boundary(ID, _).

psid_boundary(ID, PSID2)
 :- condition_holds(ID, PSID1),
    dependency_condition(ID, Package, Dependency),
    dependency_holds(Package, PSID1, Dependency, PSID2, _).

% We cut off dependencies of externals (as we don't really know them).
% Don't impose constraints on dependencies that don't exist.
do_not_impose(ID, PSID) :-
  imposed_psid(ID, PSID),
  not dependency_holds(Package, _, Dependency, PSID, _),
  dependency_condition(ID, Package, Dependency).

% declared dependencies are real if they're not virtual AND
% the package is not an external.
% They're only triggered if the associated dependnecy condition holds.
attr("depends_on", Package, PSID1, Dependency, PSID2, Type)
 :- dependency_holds(Package, PSID1, Dependency, PSID2, Type),
    not virtual(Dependency).

% every root must be a node
attr("node", Package, PSID) :- attr("root", Package, PSID).

% dependencies imply new nodes
attr("node", Dependency, PSID2) :- attr("node", Package, PSID1), depends_on(Package, PSID1, Dependency, PSID2).

% all nodes in the graph must be reachable from some root
% this ensures a user can't say `zlib ^libiconv` (neither of which have any
% dependencies) and get a two-node unconnected graph
needed(Package, PSID) :- attr("root", Package, PSID).
needed(Dependency, PSID2) :- needed(Package, PSID1), depends_on(Package, PSID1, Dependency, PSID2).
error(1, "'{0}' is not a valid dependency for any package in the DAG", Package)
  :- attr("node", Package, PSID),
     not needed(Package, PSID).

% Avoid cycles in the DAG
% some combinations of conditional dependencies can result in cycles;
% this ensures that we solve around them
path(Parent, PSID1, Child, PSID2) :- depends_on(Parent, PSID1, Child, PSID2).
path(Parent, PSID1, Descendant, PSID3) :- path(Parent, PSID1, A, PSID2), depends_on(A, PSID2, Descendant, PSID3).
error(2, "Cyclic dependency detected between '{0}' and '{1}'\n    Consider changing variants to avoid the cycle", A, B)
  :- path(A, PSID1, B, PSID2),
     path(B, PSID2, A, PSID1).

#defined dependency_type/2.
#defined dependency_condition/3.

%-----------------------------------------------------------------------------
% Conflicts
%-----------------------------------------------------------------------------
error(0, Msg) :- attr("node", Package, PSID),
   conflict(Package, TriggerID, ConstraintID, Msg),
   condition_holds(TriggerID, PSID),
   condition_holds(ConstraintID, PSID),
   not external(Package, PSID),  % ignore conflicts for externals
   not attr("hash", Package, PSID, _).  % ignore conflicts for installed packages

#defined conflict/4.

%-----------------------------------------------------------------------------
% Virtual dependencies
%-----------------------------------------------------------------------------

% if a package depends on a virtual, it's not external and we have a
% provider for that virtual then it depends on the provider
attr("depends_on", Package, PSID1, Provider, PSID2, Type)
  :- dependency_holds(Package, PSID1, Virtual, PSID2, Type),
     provider(Provider, Virtual, PSID2),
     not external(Package, PSID1).

% dependencies on virtuals also imply that the virtual is a virtual node
attr("virtual_node", Virtual, PSID2)
  :- dependency_holds(Package, PSID1, Virtual, PSID2, Type),
     virtual(Virtual), not external(Package, PSID1).

% If there's a virtual node, we must select one and only one provider.
% The provider must be selected among the possible providers.
{ provider(Package, Virtual, PSID) : possible_provider(Package, Virtual) }
  :- attr("virtual_node", Virtual, PSID).
error(2, "Cannot find valid provider for virtual {0}", Virtual)
  :- attr("virtual_node", Virtual, PSID),
     P = #count{ Package : provider(Package, Virtual, PSID)},
     P < 1.
error(2, "Spec cannot include multiple providers for virtual '{0}'\n    Requested '{1}' and '{2}'", Virtual, P1, P2)
  :- attr("virtual_node", Virtual, PSID),
     provider(P1, Virtual, PSID),
     provider(P2, Virtual, PSID),
     P1 < P2.

% virtual roots imply virtual nodes, and that one provider is a root
attr("virtual_node", Virtual, PSID) :- attr("virtual_root", Virtual, PSID).

% If we asked for a virtual root and we have a provider for that,
% then the provider is the root package.
attr("root", Package, PSID) :- attr("virtual_root", Virtual, PSID), provider(Package, Virtual, PSID).

% If we asked for a root package and that root provides a virtual,
% the root is a provider for that virtual. This rule is mostly relevant
% for environments that are concretized together (e.g. where we
% asks to install "mpich" and "hdf5+mpi" and we want "mpich" to
% be the mpi provider)
provider(Package, Virtual, PSID) :- attr("node", Package, PSID), virtual_condition_holds(Package, Virtual, PSID).

% The provider provides the virtual if some provider condition holds.
virtual_condition_holds(Provider, Virtual, PSID) :-
   provider_condition(ID, Provider, Virtual),
   condition_holds(ID, PSID),
   virtual(Virtual).

% A package cannot be the actual provider for a virtual if it does not
% fulfill the conditions to provide that virtual
:- provider(Package, Virtual, PSID), not virtual_condition_holds(Package, Virtual, PSID),
   internal_error("Virtual when provides not respected").

#defined possible_provider/2.

%-----------------------------------------------------------------------------
% Virtual dependency weights
%-----------------------------------------------------------------------------

% A provider may have different possible weights depending on whether it's an external
% or not, or on preferences expressed in packages.yaml etc. This rule ensures that
% we select the weight, among the possible ones, that minimizes the overall objective function.
1 { provider_weight(Dependency, Virtual, PSID, Weight, Reason) :
    possible_provider_weight(Dependency, Virtual, PSID, Weight, Reason) } 1
 :- provider(Dependency, Virtual, PSID), internal_error("Package provider weights must be unique").

% Get rid or the reason for enabling the possible weight (useful for debugging)
provider_weight(Dependency, Virtual, PSID, Weight) :- provider_weight(Dependency, Virtual, PSID, Weight, _).

% A provider that is an external can use a weight of 0
possible_provider_weight(Dependency, Virtual, PSID, 0, "external")
  :- provider(Dependency, Virtual, PSID),
     external(Dependency, PSID).

% A provider mentioned in packages.yaml can use a weight
% according to its priority in the list of providers
possible_provider_weight(Dependency, Virtual, PSID, Weight, "packages_yaml")
  :- provider(Dependency, Virtual, PSID),
     depends_on(Package, _, Dependency, PSID),
     pkg_provider_preference(Package, Virtual, Dependency, Weight).

% A provider mentioned in the default configuration can use a weight
% according to its priority in the list of providers
possible_provider_weight(Dependency, Virtual, PSID, Weight, "default")
  :- provider(Dependency, Virtual, PSID),
     default_provider_preference(Virtual, Dependency, Weight).

% Any provider can use 100 as a weight, which is very high and discourage its use
possible_provider_weight(Dependency, Virtual, PSID, 100, "fallback") :- provider(Dependency, Virtual, PSID).

% do not warn if generated program contains none of these.
#defined possible_provider/2.
#defined provider_condition/3.
#defined required_provider_condition/3.
#defined required_provider_condition/4.
#defined required_provider_condition/5.
#defined required_provider_condition/6.
#defined declared_dependency/3.
#defined virtual/1.
#defined virtual_condition_holds/2.
#defined external/1.
#defined external_spec/2.
#defined external_version_declared/4.
#defined buildable_false/1.
#defined pkg_provider_preference/4.
#defined default_provider_preference/3.

%-----------------------------------------------------------------------------
% External semantics
%-----------------------------------------------------------------------------

% if a package is external its version must be one of the external versions
{ external_version(Package, PSID, Version, Weight):
    version_declared(Package, Version, Weight, "external") }
    :- external(Package, PSID).
error(2, "Attempted to use external for '{0}' which does not satisfy any configured external spec", Package)
  :- external(Package, PSID),
     not external_version(Package, PSID, _, _).
error(2, "Attempted to use external for '{0}' which does not satisfy any configured external spec", Package)
  :- external(Package, PSID),
     external_version(Package, PSID, Version1, Weight1),
     external_version(Package, PSID, Version2, Weight2),
     (Version1, Weight1) < (Version2, Weight2). % see[1]

version_weight(Package, PSID, Weight) :- external_version(Package, PSID, Version, Weight).
attr("version", Package, PSID, Version) :- external_version(Package, PSID, Version, Weight).

% if a package is not buildable, only externals or hashed specs are allowed
external(Package, PSID) :- buildable_false(Package),
                           attr("node", Package, PSID),
                           not attr("hash", Package, PSID, _).

% a package is a real_node if it is not external
real_node(Package, PSID) :- attr("node", Package, PSID), not external(Package, PSID).

% a package is external if we are using an external spec for it
external(Package, PSID) :- attr("external_spec_selected", Package, PSID, _).

% we can't use the weight for an external version if we don't use the
% corresponding external spec.
:- attr("version", Package, PSID, Version),
   version_weight(Package, PSID, Weight),
   version_declared(Package, Version, Weight, "external"),
   not external(Package, PSID),
   internal_error("External weight used for internal spec").

% determine if an external spec has been selected
attr("external_spec_selected", Package, PSID, LocalIndex) :-
    external_conditions_hold(Package, PSID, LocalIndex),
    attr("node", Package, PSID),
    not attr("hash", Package, PSID, _).

external_conditions_hold(Package, PSID, LocalIndex) :-
    possible_external(ID, Package, LocalIndex), condition_holds(ID, PSID).

% it cannot happen that a spec is external, but none of the external specs
% conditions hold.
error(2, "Attempted to use external for '{0}' which does not satisfy any configured external spec", Package)
 :- external(Package, PSID),
    not external_conditions_hold(Package, PSID, _).

#defined possible_external/3.
#defined external_spec_index/3.
#defined external_spec_condition/3.
#defined external_spec_condition/4.
#defined external_spec_condition/5.
#defined external_spec_condition/6.

%-----------------------------------------------------------------------------
% Config required semantics
%-----------------------------------------------------------------------------

activate_requirement_rules(Package, PSID) :- attr("node", Package, PSID).
activate_requirement_rules(Package, PSID) :- attr("virtual_node", Package, PSID).

requirement_group_satisfied(Package, PSID, X) :-
  1 { condition_holds(Y, PSID) : requirement_group_member(Y, Package, X) } 1,
  activate_requirement_rules(Package, PSID),
  requirement_policy(Package, X, "one_of"),
  requirement_group(Package, X).

requirement_weight(Package, PSID, W) :-
  condition_holds(Y, PSID),
  requirement_has_weight(Y, W),
  requirement_group_member(Y, Package, X),
  requirement_policy(Package, X, "one_of"),
  requirement_group_satisfied(Package, PSID, X).

requirement_group_satisfied(Package, PSID, X) :-
  1 { condition_holds(Y, PSID) : requirement_group_member(Y, Package, X) } ,
  activate_requirement_rules(Package, PSID),
  requirement_policy(Package, X, "any_of"),
  requirement_group(Package, X).

requirement_weight(Package, PSID, W) :-
  W = #min {
    Z : requirement_has_weight(Y, Z), condition_holds(Y, PSID), requirement_group_member(Y, Package, X);
    % We need this to avoid an annoying warning during the solve
    %   concretize.lp:1151:5-11: info: tuple ignored:
    %   #sup@73
    10000
  },
  requirement_policy(Package, X, "any_of"),
  requirement_group_satisfied(Package, PSID, X).

error(2, "Cannot satisfy the requirements in packages.yaml for the '{0}' package. You may want to delete them to proceed with concretization. To check where the requirements are defined run 'spack config blame packages'", Package) :-
  activate_requirement_rules(Package, PSID),
  requirement_group(Package, X),
  not requirement_group_satisfied(Package, PSID, X).

#defined requirement_group/2.
#defined requirement_group_member/3.
#defined requirement_has_weight/2.
#defined requirement_policy/3.

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------
% a variant is a variant of a package if it is a variant under some condition
% and that condition holds
variant(Package, PSID, Variant) :- variant_condition(ID, Package, Variant),
                                   condition_holds(ID, PSID).

% Unconditional variants apply as soon as the package is in the PSID
variant(Package, PSID, Variant) :- variant(Package, Variant), attr("node", Package, PSID).

attr("variant_propagate", Package, PSID2, Variant, Value, Source) :-
  attr("node", Package, PSID2),
  depends_on(Parent, PSID1, Package, PSID2),
  attr("variant_propagate", Parent, PSID1, Variant, Value, Source),
  not attr("variant_set", Package, PSID2, Variant).

attr("variant_value", Package, PSID, Variant, Value) :-
  attr("node", Package, PSID),
  variant(Package, PSID, Variant),
  attr("variant_propagate", Package, PSID, Variant, Value, _),
  variant_possible_value(Package, Variant, Value).

error(2, "{0} and {1} cannot both propagate variant '{2}' to package {3} with values '{4}' and '{5}'", Source1, Source2, Variant, Package, Value1, Value2) :-
  attr("variant_propagate", Package, PSID, Variant, Value1, Source1),
  attr("variant_propagate", Package, PSID, Variant, Value2, Source2),
  variant(Package, PSID, Variant),
  Value1 != Value2.

% a variant cannot be set if it is not a variant on the package
error(2, "Cannot set variant '{0}' for package '{1}' because the variant condition cannot be satisfied for the given spec", Variant, Package)
  :- attr("variant_set", Package, PSID, Variant),
     not variant(Package, PSID, Variant),
     build(Package, PSID).

% a variant cannot take on a value if it is not a variant of the package
error(2, "Cannot set variant '{0}' for package '{1}' because the variant condition cannot be satisfied for the given spec", Variant, Package)
  :- attr("variant_value", Package, PSID, Variant, _),
     not variant(Package, PSID, Variant),
     build(Package, PSID).

% if a variant is sticky and not set its value is the default value
attr("variant_value", Package, PSID, Variant, Value) :-
  variant(Package, PSID, Variant),
  not attr("variant_set", Package, PSID, Variant),
  variant_sticky(Package, Variant),
  variant_default_value(Package, PSID, Variant, Value),
  build(Package, PSID).

% at most one variant value for single-valued variants.
{
  attr("variant_value", Package, PSID, Variant, Value)
  : variant_possible_value(Package, Variant, Value)
}
 :- attr("node", Package, PSID),
    variant(Package, PSID, Variant),
    build(Package, PSID).


error(2, "'{0}' required multiple values for single-valued variant '{1}'\n    Requested 'Spec({1}={2})' and 'Spec({1}={3})'", Package, Variant, Value1, Value2)
  :- attr("node", Package, PSID),
     variant(Package, PSID, Variant),
     variant_single_value(Package, Variant),
     build(Package, PSID),
     attr("variant_value", Package, PSID, Variant, Value1),
     attr("variant_value", Package, PSID, Variant, Value2),
     Value1 < Value2. % see[1]
error(2, "No valid value for variant '{1}' of package '{0}'", Package, Variant)
  :- attr("node", Package, PSID),
     variant(Package, PSID, Variant),
     build(Package, PSID),
     C = #count{ Value : attr("variant_value", Package, PSID, Variant, Value) },
     C < 1.

% if a variant is set to anything, it is considered 'set'.
attr("variant_set", Package, PSID, Variant) :- attr("variant_set", Package, PSID, Variant, _).

% A variant cannot have a value that is not also a possible value
% This only applies to packages we need to build -- concrete packages may
% have been built w/different variants from older/different package versions.
error(1, "'Spec({1}={2})' is not a valid value for '{0}' variant '{1}'", Package, Variant, Value)
 :- attr("variant_value", Package, PSID, Variant, Value),
    not variant_possible_value(Package, Variant, Value),
    build(Package, PSID).

% Some multi valued variants accept multiple values from disjoint sets.
% Ensure that we respect that constraint and we don't pick values from more
% than one set at once
error(2, "{0} variant '{1}' cannot have values '{2}' and '{3}' as they come from disjoing value sets", Package, Variant, Value1, Value2)
  :- attr("variant_value", Package, PSID, Variant, Value1),
     attr("variant_value", Package, PSID, Variant, Value2),
     variant_value_from_disjoint_sets(Package, Variant, Value1, Set1),
     variant_value_from_disjoint_sets(Package, Variant, Value2, Set2),
     Set1 < Set2, % see[1]
     build(Package, PSID).

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
attr("variant_value", Package, PSID, Variant, Value)
 :- attr("node", Package, PSID),
    variant(Package, PSID, Variant),
    attr("variant_set", Package, PSID, Variant, Value).

% The rules below allow us to prefer default values for variants
% whenever possible. If a variant is set in a spec, or if it is
% specified in an external, we score it as if it was a default value.
variant_not_default(Package, PSID, Variant, Value)
 :- attr("variant_value", Package, PSID, Variant, Value),
    not variant_default_value(Package, PSID, Variant, Value),
    % variants set explicitly on the CLI don't count as non-default
    not attr("variant_set", Package, PSID, Variant, Value),
    % variant values forced by propagation don't count as non-default
    not attr("variant_propagate", Package, PSID, Variant, Value, _),
    % variants set on externals that we could use don't count as non-default
    % this makes spack prefer to use an external over rebuilding with the
    % default configuration
    not external_with_variant_set(Package, PSID, Variant, Value),
    attr("node", Package, PSID).


% A default variant value that is not used
variant_default_not_used(Package, PSID, Variant, Value)
  :- variant_default_value(Package, PSID, Variant, Value),
     not attr("variant_value", Package, PSID, Variant, Value),
     attr("node", Package, PSID).

% The variant is set in an external spec
external_with_variant_set(Package, PSID, Variant, Value)
 :- attr("variant_value", Package, PSID, Variant, Value),
    condition_requirement(ID, "variant_value", Package, Variant, Value),
    possible_external(ID, Package, _),
    external(Package, PSID),
    attr("node", Package, PSID).

% The default value for a variant in a package is what is prescribed:
%
% 1. On the command line
% 2. In packages.yaml (if there's no command line settings)
% 3. In the package.py file (if there are no settings in
%    packages.yaml and the command line)
%
variant_default_value(Package, PSID, Variant, Value)
 :- variant_default_value_from_package_py(Package, Variant, Value),
    not variant_default_value_from_packages_yaml(Package, Variant, _),
    not attr("variant_default_value_from_cli", Package, PSID, Variant, _),
    attr("node", Package, PSID).

variant_default_value(Package, PSID, Variant, Value)
 :- variant_default_value_from_packages_yaml(Package, Variant, Value),
    not attr("variant_default_value_from_cli", Package, PSID, Variant, _),
    attr("node", Package, PSID).

variant_default_value(Package, PSID, Variant, Value) :-
    attr("variant_default_value_from_cli", Package, PSID, Variant, Value),
    attr("node", Package, PSID).

% Treat 'none' in a special way - it cannot be combined with other
% values even if the variant is multi-valued
error(2, "{0} variant '{1}' cannot have values '{2}' and 'none'", Package, Variant, Value)
 :- attr("variant_value", Package, PSID, Variant, Value),
    attr("variant_value", Package, PSID, Variant, "none"),
    Value != "none",
    build(Package, PSID).

% patches and dev_path are special variants -- they don't have to be
% declared in the package, so we just allow them to spring into existence
% when assigned a value.
auto_variant("dev_path").
auto_variant("patches").
variant(Package, PSID, Variant)
  :- attr("variant_set", Package, PSID, Variant, _), auto_variant(Variant).
variant_single_value(Package, "dev_path")
  :- attr("variant_set", Package, PSID, "dev_path", _).

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
attr("node_platform", Package, PSID, Platform)
 :- attr("node", Package, PSID),
    not attr("node_platform_set", Package, PSID),
    node_platform_default(Platform).

% setting platform on a node is a hard constraint
attr("node_platform", Package, PSID, Platform)
 :- attr("node", Package, PSID), attr("node_platform_set", Package, PSID, Platform).

% platform is set if set to anything
attr("node_platform_set", Package, PSID) :- attr("node_platform_set", Package, PSID, _).

% each node must have a single platform
error(2, "No valid platform found for {0}", Package)
  :- attr("node", Package, PSID),
     C = #count{ Platform : attr("node_platform", Package, PSID, Platform)},
     C < 1.

error(2, "Cannot concretize {0} with multiple platforms\n    Requested 'platform={1}' and 'platform={2}'", Package, Platform1, Platform2)
  :- attr("node", Package, PSID),
     attr("node_platform", Package, PSID, Platform1),
     attr("node_platform", Package, PSID, Platform2),
     Platform1 < Platform2. % see[1]

%-----------------------------------------------------------------------------
% OS semantics
%-----------------------------------------------------------------------------
% convert weighted OS declarations to simple one
os(OS) :- os(OS, _).

% one os per node
{ attr("node_os", Package, PSID, OS) : os(OS) } :- attr("node", Package, PSID).

error(2, "Cannot find valid operating system for '{0}'", Package)
  :- attr("node", Package, PSID),
     C = #count{ OS : attr("node_os", Package, PSID, OS)},
     C < 1.

error(2, "Cannot concretize {0} with multiple operating systems\n    Requested 'os={1}' and 'os={2}'", Package, OS1, OS2)
  :- attr("node", Package, PSID),
     attr("node_os", Package, PSID, OS1),
     attr("node_os", Package, PSID, OS2),
     OS1 < OS2. %see [1]

% can't have a non-buildable OS on a node we need to build
error(2, "Cannot concretize '{0} os={1}'. Operating system '{1}' is not buildable", Package, OS)
 :- build(Package, PSID),
    attr("node_os", Package, PSID, OS),
    not buildable_os(OS).

% can't have dependencies on incompatible OS's
% TODO GBB: should this only apply in the same process space
error(2, "{0} and dependency {1} have incompatible operating systems 'os={2}' and 'os={3}'", Package, Dependency, PackageOS, DependencyOS)
  :- depends_on(Package, PSID1, Dependency, PSID2),
     attr("node_os", Package, PSID1, PackageOS),
     attr("node_os", Dependency, PSID2, DependencyOS),
     not os_compatible(PackageOS, DependencyOS),
     build(Package, PSID).

% give OS choice weights according to os declarations
node_os_weight(Package, PSID, Weight)
 :- attr("node", Package, PSID),
    attr("node_os", Package, PSID, OS),
    os(OS, Weight).

% match semantics for OS's
node_os_match(Package, Dependency, PSID1) :-
   depends_on(Package, PSID1, Dependency, PSID2), attr("node_os", Package, PSID1, OS), attr("node_os", Dependency, PSID2, OS).
node_os_mismatch(Package, Dependency, PSID) :-
   depends_on(Package, PSID, Dependency, _), not node_os_match(Package, Dependency, PSID).

% every OS is compatible with itself. We can use `os_compatible` to declare
os_compatible(OS, OS) :- os(OS).

% Transitive compatibility among operating systems
os_compatible(OS1, OS3) :- os_compatible(OS1, OS2), os_compatible(OS2, OS3).

% We can select only operating systems compatible with the ones
% for which we can build software. We need a cardinality constraint
% since we might have more than one "buildable_os(OS)" fact.
:- not 1 { os_compatible(CurrentOS, ReusedOS) : buildable_os(CurrentOS) },
   attr("node_os", Package, PSID, ReusedOS),
   internal_error("Reused OS incompatible with build OS").

% If an OS is set explicitly respect the value
attr("node_os", Package, PSID, OS) :- attr("node_os_set", Package, PSID, OS), attr("node", Package, PSID).

#defined os_compatible/2.

%-----------------------------------------------------------------------------
% Target semantics
%-----------------------------------------------------------------------------

% Each node has only one target chosen among the known targets
{ attr("node_target", Package, PSID, Target) : target(Target) } :- attr("node", Package, PSID).

error(2, "Cannot find valid target for '{0}'", Package)
  :- attr("node", Package, PSID),
     C = #count{Target : attr("node_target", Package, PSID, Target)},
     C < 1.

error(2, "Cannot concretize '{0}' with multiple targets\n    Requested 'target={1}' and 'target={2}'", Package, Target1, Target2)
  :- attr("node", Package, PSID),
     attr("node_target", Package, PSID, Target1),
     attr("node_target", Package, PSID, Target2),
     Target1 < Target2. % see[1]

% If a node must satisfy a target constraint, enforce it
error(1, "'{0} target={1}' cannot satisfy constraint 'target={2}'", Package, Target, Constraint)
  :- attr("node_target", Package, PSID, Target),
     attr("node_target_satisfies", Package, PSID, Constraint),
     not target_satisfies(Constraint, Target).

% If a node has a target and the target satisfies a constraint, then the target
% associated with the node satisfies the same constraint
attr("node_target_satisfies", Package, PSID, Constraint)
  :- attr("node_target", Package, PSID, Target), target_satisfies(Constraint, Target).

% If a node has a target, all of its dependencies must be compatible with that target
error(2, "Cannot find compatible targets for {0} and {1}", Package, Dependency)
  :- depends_on(Package, PSID1, Dependency, PSID2),
     attr("node_target", Package, PSID1, Target),
     not node_target_compatible(Dependency, PSID2, Target).

% Intermediate step for performance reasons
% When the integrity constraint above was formulated including this logic
% we suffered a substantial performance penalty
node_target_compatible(Package, PSID, Target)
 :- attr("node_target", Package, PSID, MyTarget),
    target_compatible(Target, MyTarget).

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

% can't use targets on node if the compiler for the node doesn't support them
error(2, "{0} compiler '{2}@{3}' incompatible with 'target={1}'", Package, Target, Compiler, Version)
  :- attr("node_target", Package, PSID, Target),
     not compiler_supports_target(Compiler, Version, Target),
     attr("node_compiler", Package, PSID, Compiler),
     attr("node_compiler_version", Package, PSID, Compiler, Version),
     build(Package, PSID).

% if a target is set explicitly, respect it
attr("node_target", Package, PSID, Target)
 :- attr("node", Package, PSID), attr("node_target_set", Package, PSID, Target).

% each node has the weight of its assigned target
node_target_weight(Package, PSID, Weight)
 :- attr("node", Package, PSID),
    attr("node_target", Package, PSID, Target),
    target_weight(Package, Target, Weight).

% compatibility rules for targets among nodes
node_target_match(Parent, PSID1, Dependency)
  :- depends_on(Parent, PSID1, Dependency, PSID2),
     attr("node_target", Parent, PSID1, Target),
     attr("node_target", Dependency, PSID2, Target).

node_target_mismatch(Parent, PSID, Dependency)
  :- depends_on(Parent, PSID, Dependency, _),
     not node_target_match(Parent, PSID, Dependency).

% disallow reusing concrete specs that don't have a compatible target
error(2, "'{0} target={1}' is not compatible with this machine", Package, Target)
  :- attr("node", Package, PSID),
     attr("node_target", Package, PSID, Target),
     not target(Target).

#defined package_target_weight/3.

%-----------------------------------------------------------------------------
% Compiler semantics
%-----------------------------------------------------------------------------
compiler(Compiler) :- compiler_version(Compiler, _).

% There must be only one compiler set per built node. The compiler
% is chosen among available versions.
{ attr("node_compiler_version", Package, PSID, Compiler, Version) : compiler_version(Compiler, Version) } :-
    attr("node", Package, PSID),
    build(Package, PSID).

error(2, "No valid compiler version found for '{0}'", Package)
  :- attr("node", Package, PSID),
     C = #count{ Version : attr("node_compiler_version", Package, PSID, _, Version)},
     C < 1.
error(2, "'{0}' compiler constraints '%{1}@{2}' and '%{3}@{4}' are incompatible", Package, Compiler1, Version1, Compiler2, Version2)
  :- attr("node", Package, PSID),
     attr("node_compiler_version", Package, PSID, Compiler1, Version1),
     attr("node_compiler_version", Package, PSID, Compiler2, Version2),
     (Compiler1, Version1) < (Compiler2, Version2). % see[1]

% Sometimes we just need to know the compiler and not the version
attr("node_compiler", Package, PSID, Compiler) :- attr("node_compiler_version", Package, PSID, Compiler, _).

% We can't have a compiler be enforced and select the version from another compiler
error(2, "Cannot concretize {0} with two compilers {1}@{2} and {3}@{4}", Package, C1, V1, C2, V2)
 :- attr("node_compiler_version", Package, PSID, C1, V1),
    attr("node_compiler_version", Package, PSID, C2, V2),
    (C1, V1) != (C2, V2).

error(2, "Cannot concretize {0} with two compilers {1} and {2}@{3}", Package, Compiler1, Compiler2, Version)
 :- attr("node_compiler", Package, PSID, Compiler1),
    attr("node_compiler_version", Package, PSID, Compiler2, Version),
    Compiler1 != Compiler2.

% If the compiler of a node cannot be satisfied, raise
error(1, "No valid compiler for {0} satisfies '%{1}'", Package, Compiler)
  :- attr("node", Package, PSID),
     attr("node_compiler_version_satisfies", Package, PSID, Compiler, ":"),
     C = #count{ Version : attr("node_compiler_version", Package, PSID, Compiler, Version), compiler_version_satisfies(Compiler, ":", Version) },
     C < 1.

% If the compiler of a node must satisfy a constraint, then its version
% must be chosen among the ones that satisfy said constraint
error(2, "No valid version for '{0}' compiler '{1}' satisfies '@{2}'", Package, Compiler, Constraint)
  :- attr("node", Package, PSID),
     attr("node_compiler_version_satisfies", Package, PSID, Compiler, Constraint),
     C = #count{ Version : attr("node_compiler_version", Package, PSID, Compiler, Version), compiler_version_satisfies(Compiler, Constraint, Version) },
     C < 1.

% If the node is associated with a compiler and the compiler satisfy a constraint, then
% the compiler associated with the node satisfy the same constraint
attr("node_compiler_version_satisfies", Package, PSID, Compiler, Constraint)
  :- attr("node_compiler_version", Package, PSID, Compiler, Version),
     compiler_version_satisfies(Compiler, Constraint, Version).

#defined compiler_version_satisfies/3.

% If the compiler version was set from the command line,
% respect it verbatim
attr("node_compiler_version", Package, PSID, Compiler, Version) :-
     attr("node_compiler_version_set", Package, PSID, Compiler, Version).

% Cannot select a compiler if it is not supported on the OS
% Compilers that are explicitly marked as allowed
% are excluded from this check
error(2, "{0} compiler '%{1}@{2}' incompatible with 'os={3}'", Package, Compiler, Version, OS)
  :- attr("node_compiler_version", Package, PSID, Compiler, Version),
     attr("node_os", Package, PSID, OS),
     not compiler_supports_os(Compiler, Version, OS),
     not allow_compiler(Compiler, Version),
     build(Package, PSID).

% If a package and one of its dependencies don't have the
% same compiler there's a mismatch.
compiler_match(Package, PSID, Dependency)
  :- depends_on(Package, PSID, Dependency, PSID),
     attr("node_compiler_version", Package, PSID, Compiler, Version),
     attr("node_compiler_version", Dependency, PSID, Compiler, Version).

% don't penalize for mistmatches across process spaces
compiler_match(Package, PSID1, Dependency)
  :- depends_on(Package, PSID1, Dependency, PSID2),
     PSID1 != PSID2.

compiler_mismatch(Package, PSID1, Dependency)
  :- depends_on(Package, PSID1, Dependency, PSID2),
     not attr("node_compiler_set", Dependency, PSID2, _),
     not compiler_match(Package, PSID1, Dependency).

compiler_mismatch_required(Package, PSID1, Dependency)
  :- depends_on(Package, PSID1, Dependency, PSID2),
     attr("node_compiler_set", Dependency, PSID2, _),
     not compiler_match(Package, PSID1, Dependency).

#defined compiler_supports_os/3.
#defined allow_compiler/2.

% compilers weighted by preference according to packages.yaml
compiler_weight(Package, PSID, Weight)
 :- attr("node_compiler_version", Package, PSID, Compiler, V),
    node_compiler_preference(Package, Compiler, V, Weight).
compiler_weight(Package, PSID, Weight)
 :- attr("node_compiler_version", Package, PSID, Compiler, V),
    not node_compiler_preference(Package, Compiler, V, _),
    default_compiler_preference(Compiler, V, Weight).
compiler_weight(Package, PSID, 100)
 :- attr("node_compiler_version", Package, PSID, Compiler, Version),
    not node_compiler_preference(Package, Compiler, Version, _),
    not default_compiler_preference(Compiler, Version, _).

% For the time being, be strict and reuse only if the compiler match one we have on the system
error(2, "Compiler {1}@{2} requested for {0} cannot be found. Set install_missing_compilers:true if intended.", Package, Compiler, Version)
 :- attr("node_compiler_version", Package, PSID, Compiler, Version), not compiler_version(Compiler, Version).

#defined node_compiler_preference/4.
#defined default_compiler_preference/3.

%-----------------------------------------------------------------------------
% Compiler flags
%-----------------------------------------------------------------------------

% only propagate compiler flags within PSID

% propagate flags when compiler match
can_inherit_flags(Package, PSID, Dependency, FlagType)
 :- depends_on(Package, PSID, Dependency, PSID),
    attr("node_compiler", Package, PSID, Compiler),
    attr("node_compiler", Dependency, PSID, Compiler),
    not attr("node_flag_set", Dependency, PSID, FlagType, _),
    compiler(Compiler), flag_type(FlagType).

node_flag_inherited(Dependency, PSID, FlagType, Flag)
 :- attr("node_flag_set", Package, PSID, FlagType, Flag), can_inherit_flags(Package, PSID, Dependency, FlagType),
    attr("node_flag_propagate", Package, PSID, FlagType).
% Ensure propagation
:- node_flag_inherited(Package, PSID, FlagType, Flag),
    can_inherit_flags(Package, PSID, Dependency, FlagType),
    attr("node_flag_propagate", Package, PSID, FlagType).

error(2, "{0} and {1} cannot both propagate compiler flags '{2}' to {3}", Source1, Source2, Package, FlagType) :-
  depends_on(Source1, PSID, Package, PSID),
  depends_on(Source2, PSID, Package, PSID),
  attr("node_flag_propagate", Source1, PSID, FlagType),
  attr("node_flag_propagate", Source2, PSID, FlagType),
  can_inherit_flags(Source1, PSID, Package, FlagType),
  can_inherit_flags(Source2, PSID, Package, FlagType),
  Source1 != Source2.

% remember where flags came from
attr("node_flag_source", Package, PSID, FlagType, Package) :- attr("node_flag_set", Package, PSID, FlagType, _).
attr("node_flag_source", Dependency, PSID, FlagType, Q)
 :- attr("node_flag_source", Package, PSID, FlagType, Q), node_flag_inherited(Dependency, PSID, FlagType, _),
    attr("node_flag_propagate", Package, PSID, FlagType).

% compiler flags from compilers.yaml are put on nodes if compiler matches
attr("node_flag", Package, PSID, FlagType, Flag)
 :- compiler_version_flag(Compiler, Version, FlagType, Flag),
    attr("node_compiler_version", Package, PSID, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

attr("node_flag_compiler_default", Package, PSID)
 :- not attr("node_flag_set", Package, PSID, FlagType, _),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    attr("node_compiler_version", Package, PSID, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

% if a flag is set to something or inherited, it's included
attr("node_flag", Package, PSID, FlagType, Flag) :- attr("node_flag_set", Package, PSID, FlagType, Flag).
attr("node_flag", Package, PSID, FlagType, Flag)
 :- node_flag_inherited(Package, PSID, FlagType, Flag).

% if no node flags are set for a type, there are no flags.
attr("no_flags", Package, PSID, FlagType)
 :- not attr("node_flag", Package, PSID, FlagType, _), attr("node", Package, PSID), flag_type(FlagType).

#defined compiler_version_flag/4.


%-----------------------------------------------------------------------------
% Installed packages
%-----------------------------------------------------------------------------
% the solver is free to choose at most one installed hash for each package
{ attr("hash", Package, PSID, Hash) : installed_hash(Package, Hash) } 1
 :- attr("node", Package, PSID), internal_error("Package must resolve to at most one hash").

% you can't choose an installed hash for a dev spec
:- attr("hash", Package, PSID, Hash), attr("variant_value", Package, PSID, "dev_path", _).

% You can't install a hash, if it is not installed
:- attr("hash", Package, PSID, Hash), not installed_hash(Package, Hash).
% This should be redundant given the constraint above
:- attr("hash", Package, PSID, Hash1), attr("hash", Package, PSID, Hash2), Hash1 != Hash2.

% if a hash is selected, we impose all the constraints that implies
impose(Hash, PSID) :- attr("hash", Package, PSID, Hash).

% if we haven't selected a hash for a package, we'll be building it
build(Package, PSID) :- not attr("hash", Package, PSID, _), attr("node", Package, PSID).

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
build_priority(Package, PSID, 200) :- build(Package, PSID), attr("node", Package, PSID), optimize_for_reuse().
build_priority(Package, PSID, 0)   :- not build(Package, PSID), attr("node", Package, PSID), optimize_for_reuse().

% don't adjust build priorities if reuse is not enabled
build_priority(Package, PSID, 0)   :- attr("node", Package, PSID), not optimize_for_reuse().

% don't assign versions from installed packages unless reuse is enabled
% NOTE: that "installed" means the declared version was only included because
% that package happens to be installed, NOT because it was asked for on the
% command line.  If the user specifies a hash, the origin will be "spec".
%
% TODO: There's a slight inconsistency with this: if the user concretizes
% and installs `foo ^bar`, for some build dependency `bar`, and then later
% does a `spack install --fresh foo ^bar/abcde` (i.e.,the hash of `bar`, it
% currently *won't* force versions for `bar`'s build dependencies -- `--fresh`
% will instead build the latest bar. When we actually include transitive
% build deps in the solve, consider using them as a preference to resolve this.
:- attr("version", Package, PSID, Version),
   version_weight(Package, PSID, Weight),
   version_declared(Package, Version, Weight, "installed"),
   not optimize_for_reuse().

#defined installed_hash/2.

%-----------------------------------------------------------------
% Optimization to avoid errors
%-----------------------------------------------------------------
% Some errors are handled as rules instead of constraints because
% it allows us to explain why something failed. Here we optimize
% HEAVILY against the facts generated by those rules.
#minimize{ 0@1000: #true}.
#minimize{ 0@1001: #true}.
#minimize{ 0@1002: #true}.

#minimize{ 1000@1000+Priority,Msg: error(Priority, Msg) }.
#minimize{ 1000@1000+Priority,Msg,Arg1: error(Priority, Msg, Arg1) }.
#minimize{ 1000@1000+Priority,Msg,Arg1,Arg2: error(Priority, Msg, Arg1, Arg2) }.
#minimize{ 1000@1000+Priority,Msg,Arg1,Arg2,Arg3: error(Priority, Msg, Arg1, Arg2, Arg3) }.
#minimize{ 1000@1000+Priority,Msg,Arg1,Arg2,Arg3,Arg4: error(Priority, Msg, Arg1, Arg2, Arg3, Arg4) }.
#minimize{ 1000@1000+Priority,Msg,Arg1,Arg2,Arg3,Arg4,Arg5: error(Priority, Msg, Arg1, Arg2, Arg3, Arg4, Arg5) }.

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
#minimize { 1@100,Package,PSID : build(Package, PSID), optimize_for_reuse() }.
#defined optimize_for_reuse/0.

% A condition group specifies one or more specs that must be satisfied.
% Specs declared first are preferred, so we assign increasing weights and
% minimize the weights.
opt_criterion(75, "requirement weight").
#minimize{ 0@275: #true }.
#minimize{ 0@75: #true }.
#minimize {
    Weight@75+Priority,PSID
    : requirement_weight(Package, PSID, Weight),
      build_priority(Package, PSID, Priority)
}.

% Minimize the number of deprecated versions being used
opt_criterion(73, "deprecated versions used").
#minimize{ 0@273: #true }.
#minimize{ 0@73: #true }.
#minimize{
    1@73+Priority,Package,PSID
    : attr("deprecated", Package, PSID, _),
      build_priority(Package, PSID, Priority)
}.

% Minimize the:
% 1. Version weight
% 2. Number of variants with a non default value, if not set
% for the root package.
opt_criterion(70, "version weight").
#minimize{ 0@270: #true }.
#minimize{ 0@70: #true }.
#minimize {
    Weight@70+Priority,PSID
    : attr("root", Package, PSID), version_weight(Package, PSID, Weight),
      build_priority(Package, PSID, Priority)
}.

opt_criterion(65, "number of non-default variants (roots)").
#minimize{ 0@265: #true }.
#minimize{ 0@65: #true }.
#minimize {
    1@65+Priority,Package,Variant,Value,PSID
    : variant_not_default(Package, PSID, Variant, Value),
      attr("root", Package, PSID),
      build_priority(Package, PSID, Priority)
}.

opt_criterion(60, "preferred providers for roots").
#minimize{ 0@260: #true }.
#minimize{ 0@60: #true }.
#minimize{
    Weight@60+Priority,Provider,Virtual
    : provider_weight(Provider, Virtual, PSID, Weight),
      attr("root", Provider, PSID),
      build_priority(Provider, PSID, Priority)
}.

opt_criterion(55, "default values of variants not being used (roots)").
#minimize{ 0@255: #true }.
#minimize{ 0@55: #true }.
#minimize{
    1@55+Priority,Package,Variant,Value,PSID
    : variant_default_not_used(Package, PSID, Variant, Value),
      attr("root", Package, PSID),
      build_priority(Package, PSID, Priority)
}.

% Try to use default variants or variants that have been set
opt_criterion(50, "number of non-default variants (non-roots)").
#minimize{ 0@250: #true }.
#minimize{ 0@50: #true }.
#minimize {
    1@50+Priority,Package,Variant,Value,PSID
    : variant_not_default(Package, PSID, Variant, Value),
      not attr("root", Package, PSID),
      build_priority(Package, PSID, Priority)
}.

% Minimize the weights of the providers, i.e. use as much as
% possible the most preferred providers
opt_criterion(45, "preferred providers (non-roots)").
#minimize{ 0@245: #true }.
#minimize{ 0@45: #true }.
#minimize{
    Weight@45+Priority,Provider,Virtual,PSID
    : provider_weight(Provider, Virtual, PSID, Weight), not attr("root", Provider, PSID),
      build_priority(Provider, PSID, Priority)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(40, "compiler mismatches that are not from CLI").
#minimize{ 0@240: #true }.
#minimize{ 0@40: #true }.
#minimize{
    1@40+Priority,Package,Dependency,PSID
    : compiler_mismatch(Package, PSID, Dependency),
      build_priority(Package, PSID, Priority)
}.

opt_criterion(39, "compiler mismatches that are not from CLI").
#minimize{ 0@239: #true }.
#minimize{ 0@39: #true }.
#minimize{
    1@39+Priority,Package,Dependency,PSID
    : compiler_mismatch_required(Package, PSID, Dependency),
      build_priority(Package, PSID, Priority)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(35, "OS mismatches").
#minimize{ 0@235: #true }.
#minimize{ 0@35: #true }.
#minimize{
    1@35+Priority,Package,Dependency,PSID
    : node_os_mismatch(Package, Dependency, PSID),
      build_priority(Package, PSID, Priority)
}.

opt_criterion(30, "non-preferred OS's").
#minimize{ 0@230: #true }.
#minimize{ 0@30: #true }.
#minimize{
    Weight@30+Priority,Package,PSID
    : node_os_weight(Package, PSID, Weight),
      build_priority(Package, PSID, Priority)
}.

% Choose more recent versions for nodes
opt_criterion(25, "version badness").
#minimize{ 0@225: #true }.
#minimize{ 0@25: #true }.
#minimize{
    Weight@25+Priority,Package,PSID
    : version_weight(Package, PSID, Weight),
      build_priority(Package, PSID, Priority)
}.

% Try to use all the default values of variants
opt_criterion(20, "default values of variants not being used (non-roots)").
#minimize{ 0@220: #true }.
#minimize{ 0@20: #true }.
#minimize{
    1@20+Priority,Package,Variant,Value,PSID
    : variant_default_not_used(Package, PSID, Variant, Value),
      not attr("root", Package, PSID),
      build_priority(Package, PSID, Priority)
}.

% Try to use preferred compilers
opt_criterion(15, "non-preferred compilers").
#minimize{ 0@215: #true }.
#minimize{ 0@15: #true }.
#minimize{
    Weight@15+Priority,Package,PSID
    : compiler_weight(Package, PSID, Weight),
      build_priority(Package, PSID, Priority)
}.

% Minimize the number of mismatches for targets in the DAG, try
% to select the preferred target.
opt_criterion(10, "target mismatches").
#minimize{ 0@210: #true }.
#minimize{ 0@10: #true }.
#minimize{
    1@10+Priority,Package,Dependency,PSID
    : node_target_mismatch(Package, PSID, Dependency),
      build_priority(Package, PSID, Priority)
}.

opt_criterion(5, "non-preferred targets").
#minimize{ 0@205: #true }.
#minimize{ 0@5: #true }.
#minimize{
    Weight@5+Priority,Package,PSID
    : node_target_weight(Package, PSID, Weight),
      build_priority(Package, PSID, Priority)
}.

%-----------------
% Domain heuristic
%-----------------
#heuristic attr("version", Package, PSID, Version) : version_declared(Package, Version, 0), attr("node", Package, PSID). [10, true]
#heuristic version_weight(Package, PSID, 0) : version_declared(Package, Version, 0), attr("node", Package, PSID). [10, true]
#heuristic attr("node_target", Package, PSID, Target) : package_target_weight(Target, Package, 0), attr("node", Package, PSID). [10, true]
#heuristic node_target_weight(Package, PSID, 0) : attr("node", Package, PSID). [10, true]
#heuristic attr("variant_value", Package, PSID, Variant, Value) : variant_default_value(Package, PSID, Variant, Value), attr("node", Package, PSID). [10, true]
#heuristic provider(Package, Virtual, PSID) : possible_provider_weight(Package, Virtual, PSID, 0, _), attr("virtual_node", Virtual, PSID). [10, true]
#heuristic attr("node", Package, PSID) : possible_provider_weight(Package, Virtual, PSID, 0, _), attr("virtual_node", Virtual, PSID). [10, true]
#heuristic attr("node_os", Package, PSID, OS) : buildable_os(OS). [10, true]

%-----------
% Notes
%-----------

% [1] Clingo ensures a total ordering among all atoms. We rely on that total ordering
%     to reduce symmetry in the solution by checking `<` instead of `!=` in symmetric
%     cases. These choices are made without loss of generality.
