% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% This logic program adds detailed error messages to Spack's concretizer
%=============================================================================

% Create a causal tree between trigger conditions by locating the effect conditions
% that are triggers for another condition. Condition2 is caused by Condition1
condition_cause(Condition2, Condition1, ID) :-
  condition_holds(Condition2, node(ID, Package)),
  pkg_fact(Package, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package),
  attr(Name, node(ID, Package)),
  condition_holds(Condition1, node(ID, Package)),
  pkg_fact(Package, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package).

condition_cause(Condition2, Condition1, ID) :-
  condition_holds(Condition2, node(ID, Package)),
  pkg_fact(Package, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package, A1),
  attr(Name, node(ID, Package), A1),
  condition_holds(Condition1, node(ID, Package)),
  pkg_fact(Package, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package, A1).

condition_cause(Condition2, Condition1, ID) :-
  condition_holds(Condition2, node(ID, Package)),
  pkg_fact(Package, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package, A1, A2),
  attr(Name, node(ID, Package), A1, A2),
  condition_holds(Condition1, node(ID, Package)),
  pkg_fact(Package, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package, A1, A2).

condition_cause(Condition2, Condition1, ID) :-
  condition_holds(Condition2, node(ID, Package)),
  pkg_fact(Package, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package, A1, A2, A3),
  attr(Name, node(ID, Package), A1, A2, A3),
  condition_holds(Condition1, node(ID, Package)),
  pkg_fact(Package, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package, A1, A2, A3).

% special condition cause for dependency conditions
% we can't simply impose the existence of the node for dependency conditions
% because we need to allow for the choice of which dupe ID the node gets
condition_cause(Condition2, Condition1, ID) :-
  condition_holds(Condition2, node(ID2, Package2)),
  pkg_fact(Package2, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, "node", Package),
  attr("node", node(ID, Package)),
  condition_holds(Condition1, node(ID1, Package1)),
  pkg_fact(Package1, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, "dependency_holds", Parent, Package, Type),
  attr("depends_on", node(X, Parent), node(ID, Package), Type).

% More specific error message if the version cannot satisfy some constraint
% Otherwise covered by `no_version_error` and `versions_conflict_error`.
error(1, "Cannot satisfy '{0}@{1}'", Package, Constraint, startcauses, ConstraintCause)
  :- attr("node_version_satisfies", node(ID, Package), Constraint),
     pkg_fact(TriggerPkg, condition_effect(ConstraintCause, EffectID)),
     imposed_constraint(EffectID, "node_version_satisfies", Package, Constraint),
     condition_holds(ConstraintCause, node(_, TriggerPkg)),
     attr("version", node(ID, Package), Version),
     not pkg_fact(Package, version_satisfies(Constraint, Version)).

error(0, "Cannot satisfy '{0}@{1}' and '{0}@{2}", Package, Constraint1, Constraint2, startcauses, Cause1, Cause2)
  :- attr("node_version_satisfies", node(ID, Package), Constraint1),
     pkg_fact(TriggerPkg1, condition_effect(Cause1, EffectID1)),
     imposed_constraint(EffectID1, "node_version_satisfies", Package, Constraint1),
     condition_holds(Cause1, node(_, TriggerPkg1)),
     % two constraints
     attr("node_version_satisfies", node(ID, Package), Constraint2),
     pkg_fact(TriggerPkg2, condition_effect(Cause2, EffectID2)),
     imposed_constraint(EffectID2, "node_version_satisfies", Package, Constraint2),
     condition_holds(Cause2, node(_, TriggerPkg2)),
     % version chosen
     attr("version", node(ID, Package), Version),
     % version satisfies one but not the other
     pkg_fact(Package, version_satisfies(Constraint1, Version)),
     not pkg_fact(Package, version_satisfies(Constraint2, Version)).

% At most one variant value for single-valued variants
error(0, "'{0}' required multiple values for single-valued variant '{1}'\n    Requested 'Spec({1}={2})' and 'Spec({1}={3})'", Package, Variant, Value1, Value2, startcauses, Cause1, Cause2)
  :- attr("node", node(X, Package)),
     node_has_variant(node(X, Package), Variant),
     pkg_fact(Package, variant_single_value(Variant)),
     build(node(X, Package)),
     attr("variant_value", node(X, Package), Variant, Value1),
     imposed_constraint(EID1, "variant_set", Package, Variant, Value1),
     pkg_fact(TriggerPkg1, condition_effect(Cause1, EID1)),
     condition_holds(Cause1, node(X, TriggerPkg1)),
     attr("variant_value", node(X, Package), Variant, Value2),
     imposed_constraint(EID2, "variant_set", Package, Variant, Value2),
     pkg_fact(TriggerPkg2, condition_effect(Cause2, EID2)),
     condition_holds(Cause2, node(X, TriggerPkg2)),
     Value1 < Value2. % see[1] in concretize.lp
