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

% More specific error message if the version cannot satisfy some constraint
% Otherwise covered by `no_version_error` and `versions_conflict_error`.
error(0, "AAACannot satisfy '{0}@{1}'", node(ID, Package), Constraint, startcauses, ID, ConstraintCause)
  :- attr("node_version_satisfies", node(ID, Package), Constraint),
     pkg_fact(Package, condition_effect(ConstraintCause, EffectID)),
     imposed_constraint(EffectID, "node_version_satisfies", Package, Constraint),
     condition_holds(ConstraintCause, node(ID, Package)),
     attr("version", node(ID, Package), Version),
     not pkg_fact(Package, version_satisfies(Constraint, Version)).
