% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% This logic program adds detailed error messages to Spack's concretizer
%
% Note that functions used in rule bodies here need to have a corresponding
% #show line in display.lp, otherwise they won't be passed through to the
% error solve.
%=============================================================================

#program error_messages.

% The following "condition_cause" rules create a causal tree between trigger
% conditions by locating the effect conditions that are triggers for another
% condition. In all these rules, Condition2 is caused by Condition1

% For condition_cause rules, it is not necessary to confirm that the attr is present
% on the node because `condition_holds` and `impose_constraint` collectively
% guarantee it.
% We omit those facts to reduce the burden on the grounder/solver.

condition_cause(Condition2, ID2, Condition1, ID1) :-
  condition_holds(Condition2, node(ID2, Package2)),
  pkg_fact(Package2, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package),
  condition_nodes(TriggerNode, node(ID, Package)),
  trigger_node(Trigger, TriggerNode, node(ID2, Package2)),
  condition_holds(Condition1, node(ID1, Package1)),
  pkg_fact(Package1, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package),
  imposed_nodes(node(ID1, Package1), node(ID, Package)).

condition_cause(Condition2, ID2, Condition1, ID1) :-
  condition_holds(Condition2, node(ID2, Package2)),
  pkg_fact(Package2, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package, A1),
  condition_nodes(TriggerNode, node(ID, Package)),
  trigger_node(Trigger, TriggerNode, node(ID2, Package2)),
  condition_holds(Condition1, node(ID1, Package1)),
  pkg_fact(Package1, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package, A1),
  imposed_nodes(node(ID1, Package1), node(ID, Package)).

condition_cause(Condition2, ID2, Condition1, ID1) :-
  condition_holds(Condition2, node(ID2, Package2)),
  pkg_fact(Package2, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package, A1, A2),
  condition_nodes(TriggerNode, node(ID, Package)),
  trigger_node(Trigger, TriggerNode, node(ID2, Package2)),
  condition_holds(Condition1, node(ID1, Package1)),
  pkg_fact(Package1, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package, A1, A2),
  imposed_nodes(node(ID1, Package1), node(ID, Package)).

condition_cause(Condition2, ID2, Condition1, ID1) :-
  condition_holds(Condition2, node(ID2, Package2)),
  pkg_fact(Package2, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, Name, Package, A1, A2, A3),
  condition_nodes(TriggerNode, node(ID, Package)),
  trigger_node(Trigger, TriggerNode, node(ID2, Package2)),
  condition_holds(Condition1, node(ID1, Package1)),
  pkg_fact(Package1, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, Name, Package, A1, A2, A3),
  imposed_nodes(node(ID1, Package1), node(ID, Package)).

% special condition cause for dependency conditions
% we can't simply impose the existence of the node for dependency conditions
% because we need to allow for the choice of which dupe ID the node gets
condition_cause(Condition2, ID2, Condition1, ID1) :-
  condition_holds(Condition2, node(ID2, Package2)),
  pkg_fact(Package2, condition_trigger(Condition2, Trigger)),
  condition_requirement(Trigger, "node", Package),
  condition_nodes(TriggerNode, node(ID, Package)),
  trigger_node(Trigger, TriggerNode, node(ID2, Package2)),
  condition_holds(Condition1, node(ID1, Package1)),
  pkg_fact(Package1, condition_effect(Condition1, Effect)),
  imposed_constraint(Effect, "dependency_holds", Parent, Package, Type),
  imposed_nodes(node(ID1, Package1), node(ID, Package)),
  attr("depends_on", node(X, Parent), node(ID, Package), Type).

#defined choose_version/2.

% error_cause/4 links each error/3 fact to its causation conditions.
% Format: error_cause(ErrorType, NodeTerm, ConditionID, CauseNodeID)

% More specific error message if the version cannot satisfy some constraint
error_cause(version_constraint_unsatisfied(Constraint), node(ID, Package), ConstraintCause, CauseID)
  :- error(version_constraint_unsatisfied(Constraint), _, node(ID, Package)),
     pkg_fact(TriggerPkg, condition_effect(ConstraintCause, EffectID)),
     imposed_constraint(EffectID, "node_version_satisfies", Package, Constraint),
     condition_holds(ConstraintCause, node(CauseID, TriggerPkg)).

% Also track the competing constraint that drove the actual version selection,
% preventing Constraint from being satisfied (the "other side" of a diamond conflict)
error_cause(version_constraint_unsatisfied(Constraint), node(ID, Package), VersionCause, CauseID)
  :- error(version_constraint_unsatisfied(Constraint), _, node(ID, Package)),
     attr("version", node(ID, Package), ActualVersion),
     imposed_constraint(EffectID, "node_version_satisfies", Package, OtherConstraint),
     OtherConstraint != Constraint,
     pkg_fact(Package, version_satisfies(OtherConstraint, ActualVersion)),
     pkg_fact(TriggerPkg, condition_effect(VersionCause, EffectID)),
     condition_holds(VersionCause, node(CauseID, TriggerPkg)).

% causation tracking for no valid provider
error_cause(no_valid_provider, node(X, Virtual), Cause, CID)
  :- error(no_valid_provider, _, node(X, Virtual)),
     imposed_constraint(EID, "dependency_holds", Parent, Virtual, Type),
     pkg_fact(TriggerPkg, condition_effect(Cause, EID)),
     condition_holds(Cause, node(CID, TriggerPkg)).

% causation tracking for variant value conflicts — one rule per conflicting value
error_cause(variant_value_conflict(Variant, Value1, Value2), node(X, Package), Cause, X)
  :- error(variant_value_conflict(Variant, Value1, Value2), _, node(X, Package)),
     attr("variant_value", node(X, Package), Variant, Value1),
     imposed_constraint(EID1, "variant_set", Package, Variant, Value1),
     pkg_fact(TriggerPkg, condition_effect(Cause, EID1)),
     condition_holds(Cause, node(X, TriggerPkg)).

error_cause(variant_value_conflict(Variant, Value1, Value2), node(X, Package), Cause, X)
  :- error(variant_value_conflict(Variant, Value1, Value2), _, node(X, Package)),
     attr("variant_value", node(X, Package), Variant, Value2),
     imposed_constraint(EID2, "variant_set", Package, Variant, Value2),
     pkg_fact(TriggerPkg, condition_effect(Cause, EID2)),
     condition_holds(Cause, node(X, TriggerPkg)).

% causation tracking for conflicts (trigger side)
error_cause(conflict(Msg), node(ID, Package), TriggerID, ID1)
  :- error(conflict(Msg), _, node(ID, Package)),
     pkg_fact(Package, conflict(TriggerID, ConstraintID, Msg)),
     condition_holds(TriggerID, node(ID1, _)).

% causation tracking for conflicts (constraint side)
error_cause(conflict(Msg), node(ID, Package), ConstraintID, ID2)
  :- error(conflict(Msg), _, node(ID, Package)),
     pkg_fact(Package, conflict(TriggerID, ConstraintID, Msg)),
     condition_holds(ConstraintID, node(ID2, Package)).

pkg_fact(Package, version_satisfies(Constraint, Version)) :-
    pkg_fact(Package, version_order(Version, VersionIdx)),
    pkg_fact(Package, version_range(Constraint, MinIdx, MaxIdx)),
    VersionIdx >= MinIdx, VersionIdx <= MaxIdx.

% variables to show
#show error/3.
#show error_cause/4.
#show condition_cause/4.
#show condition_reason/2.

% Define all variables used to avoid warnings at runtime when the model doesn't happen to have one
#defined error/3.
#defined error_cause/4.
#defined attr/2.
#defined attr/3.
#defined attr/4.
#defined attr/5.
#defined pkg_fact/2.
#defined imposed_constraint/3.
#defined imposed_constraint/4.
#defined imposed_constraint/5.
#defined imposed_constraint/6.
#defined condition_cause/4.
#defined condition_nodes/2.
#defined condition_requirement/3.
#defined condition_requirement/4.
#defined condition_requirement/5.
#defined condition_requirement/6.
#defined condition_holds/2.
#defined unification_set/2.
#defined external/1.
#defined trigger_and_effect/3.
#defined build/1.
#defined node_has_variant/3.
#defined provider/2.
#defined variant_single_value/2.
