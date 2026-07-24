% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% This logic program implements variant and compiler flag propagation
%
% This file is conditionally loaded when:
% - A spec propagates variant values, OR
% - A spec propagates compiler flags
%
% Propagation allows attributes to flow from parent packages to their
% dependencies through the dependency graph.
%=============================================================================

%-----------------------------------------------------------------------------
% Propagation semantics
%-----------------------------------------------------------------------------

non_default_propagation(variant_value(Name, Value)) :- attr("propagate", RootNode, variant_value(Name, Value)).

% Propagation roots have a corresponding attr("propagate", ...)
propagate(RootNode, PropagatedAttribute) :- attr("propagate", RootNode, PropagatedAttribute), not non_default_propagation(PropagatedAttribute).
propagate(RootNode, PropagatedAttribute, EdgeTypes) :- attr("propagate", RootNode, PropagatedAttribute, EdgeTypes).

% Special case variants, to inject the source node in the propagated attribute
propagate(RootNode, variant_value(Name, Value, RootNode)) :- attr("propagate", RootNode, variant_value(Name, Value)).

% Propagate an attribute along edges to child nodes
propagate(ChildNode, PropagatedAttribute) :-
  propagate(ParentNode, PropagatedAttribute),
  depends_on(ParentNode, ChildNode).

% Project the source-tag (and value, respectively) out of propagate/2 explicitly.
% clingo v5 grounded `propagate(N, variant_value(V, Val, _))` via an internal
% #p_propagate projection auxiliary; clingo v6's --project-anonymous does the
% syntactic `_` -> `*` rewrite but skips the auxiliary, leaving `*` as a literal
% constant that never matches concrete sources derived through recursion.
propagated_variant_value(PackageNode, Variant, Value) :-
  propagate(PackageNode, variant_value(Variant, Value, Source)).

self_propagated_variant(PackageNode, Variant) :-
  propagate(PackageNode, variant_value(Variant, AnyValue, PackageNode)).

propagate(ChildNode, PropagatedAttribute, edge_types(DepType1, DepType2)) :-
  propagate(ParentNode, PropagatedAttribute, edge_types(DepType1, DepType2)),
  depends_on(ParentNode, ChildNode),
  1 { attr("depends_on", ParentNode, ChildNode, DepType1);  attr("depends_on", ParentNode, ChildNode, DepType2) }.

%-----------------------------------------------------------------------------
% Activation of propagated values
%-----------------------------------------------------------------------------

%----
% Variants
%----

% If a variant is propagated, and can be accepted, set its value
attr("variant_value", PackageNode, Variant, Value) :-
  propagated_variant_value(PackageNode, Variant, Value),
  node_has_variant(PackageNode, Variant, _),
  variant_possible_value(PackageNode, Variant, Value).

% If a variant is propagated, we cannot have extraneous values
variant_is_propagated(PackageNode, Variant) :-
  attr("variant_value", PackageNode, Variant, Value),
  propagated_variant_value(PackageNode, Variant, Value),
  not attr("variant_set", PackageNode, Variant).

:- variant_is_propagated(PackageNode, Variant),
   attr("variant_value", PackageNode, Variant, Value),
   not propagated_variant_value(PackageNode, Variant, Value).

error(100, "{0} and {1} cannot both propagate variant '{2}' to the shared dependency: {3}",
  Package1, Package2, Variant, Dependency) :-
  % The variant is a singlevalued variant
  variant_single_value(node(X, Package1), Variant),
  % Dependency is trying to propagate Variant with different values and is not the source package
  propagate(node(Z, Dependency), variant_value(Variant, Value1, node(X, Package1))),
  propagate(node(Z, Dependency), variant_value(Variant, Value2, node(Y, Package2))),
  % Package1 and Package2 and their values are different
  Package1 > Package2,  Value1 != Value2,
  not self_propagated_variant(node(Z, Dependency), Variant).

% Cannot propagate the same variant from two different packages if one is a dependency of the other
error(100, "{0} and {1} cannot both propagate variant '{2}'", Package1, Package2, Variant) :-
  % The variant is a single-valued variant
  variant_single_value(node(X, Package1), Variant),
  % Package1 and Package2 and their values are different
  Package1 != Package2,  Value1 != Value2,
  % Package2 is set to propagate the value from Package1
  propagate(node(Y, Package2), variant_value(Variant, Value2, node(X, Package2))),
  propagate(node(Y, Package2), variant_value(Variant, Value1, node(X, Package1))),
  variant_is_propagated(node(Y, Package2), Variant).

% Cannot propagate a variant if a different value was set for it in a dependency
error(100, "Cannot propagate the variant '{0}' from the package: {1} because package: {2} is set to exclude it", Variant, Source, Package) :-
  % Package has a Variant and Source is propagating Variant
  attr("variant_set", node(X, Package), Variant, Value1),
  % The packages and values are different
  Source != Package,  Value1 != Value2,
  % The variant is a single-valued variant
  variant_single_value(node(X, Package1), Variant),
  % A different value is being propagated from somewhere else
  propagate(node(X, Package), variant_value(Variant, Value2, node(Y, Source))).

%----
% Flags
%----

% A propagated flag implies:
% 1. The same flag type is not set on this node
% 2. This node has the same compilers as the propagation source
% Note: node_compiler predicates are defined in concretize.lp

propagated_flag(node(PackageID, Package), node_flag(FlagType, Flag, FlagGroup, Source), SourceNode) :-
  propagate(node(PackageID, Package), node_flag(FlagType, Flag, FlagGroup, Source), _),
  not pkg_has_literal_flag_set(node(PackageID, Package), FlagType),
  % Same compilers as propagation source
  node_compiler(node(PackageID, Package), CompilerNode, Language) : node_compiler(SourceNode, CompilerNode, Language);
  attr("propagate", SourceNode, node_flag(FlagType, Flag, FlagGroup, Source), _),
  node(PackageID, Package) != SourceNode,
  not runtime(Package).

attr("node_flag", PackageNode, NodeFlag) :- propagated_flag(PackageNode, NodeFlag, _).

% Cannot propagate the same flag from two distinct sources
error(100, "{0} and {1} cannot both propagate compiler flags '{2}' to {3}", Source1, Source2, FlagType, Package) :-
  propagated_flag(node(ID, Package), node_flag(FlagType, _, _, _), node(_, Source1)),
  propagated_flag(node(ID, Package), node_flag(FlagType, _, _, _), node(_, Source2)),
  Source1 < Source2.

%----
% Compiler constraints
%----

% If a node is built, impose constraints on the compiler coming from dependents
attr("node_version_satisfies", node(Y, Compiler), VersionRange) :-
   propagate(node(X, Package), node_version_satisfies(Compiler, VersionRange)),
   attr("depends_on", node(X, Package), node(Y, Compiler), "build"),
   not runtime(Package).
