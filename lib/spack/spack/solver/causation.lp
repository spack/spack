% Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

% associated conditions by cause -> effect
condition_cause(Effect, Cause) :-
  condition_holds(Effect), condition_holds(Cause),
  attr(Name, A1),
  condition_requirement(Effect, Name, A1),
  imposed_constraint(Cause, Name, A1).
condition_cause(Effect, Cause) :-
  condition_holds(Effect), condition_holds(Cause),
  attr(Name, A1, A2),
  condition_requirement(Effect, Name, A1, A2),
  imposed_constraint(Cause, Name, A1, A2).
condition_cause(Effect, Cause) :-
  condition_holds(Effect), condition_holds(Cause),
  attr(Name, A1, A2, A3),
  condition_requirement(Effect, Name, A1, A2, A3),
  imposed_constraint(Cause, Name, A1, A2, A3).
condition_cause(Effect, Cause) :-
  condition_holds(Effect), condition_holds(Cause),
  attr(Name, A1, A2, A3, A4),
  condition_requirement(Effect, Name, A1, A2, A3, A4),
  imposed_constraint(Cause, Name, A1, A2, A3, A4).

% At most one variant for single valued variants
error(0, "'{0}' required multiple values for single-valued variant '{1}'\n    Requested 'Spec({1}={2})' and 'Spec({1}={3})'", Package, Variant, Value1, Value2, startcauses, Cause1, Cause2)
  :- attr("node", Package),
     variant(Package, Variant),
     variant_single_value(Package, Variant),
     build(Package),
     attr("variant_value", Package, Variant, Value1),
     imposed_constraint(Cause1, "variant_set", Package, Variant, Value1),
     condition_holds(Cause1),
     attr("variant_value", Package, Variant, Value2),
     imposed_constraint(Cause2, "variant_set", Package, Variant, Value2),
     condition_holds(Cause2),
     Value1 < Value2. % see[1] in concretize.lp

% We cannot have a version that violates another version constraint
error(0, "Version '{0}' of {1} does not satisfy '@{2}'", Version, Package, Constraint, startcauses, VersionCause, ConstraintCause)
 :- attr("node", Package),
    attr("version", Package, Version),
    imposed_constraint(VersionCause, "node_version_satisfies", Package, Version),
    condition_holds(VersionCause),
    attr("node_version_satisfies", Package, Constraint),
    imposed_constraint(ConstraintCause, "node_version_satisfies", Package, Constraint),
    condition_holds(ConstraintCause),
    not version_satisfies(Package, Constraint, Version).

% A virtual package may or may not have a version, but never has more than one
% Error to catch how it happens
error(0, "Version '{0}' of {1} does not satisfy '@{2}'", Version, Virtual, Constraint, startcauses, VersionCause, ConstraintCause)
 :- attr("virtual_node", Virtual),
    attr("version", Virtual, Version),
    imposed_constraint(VersionCause, "node_version_satisfies", Virtual, Version),
    condition_holds(VersionCause),
    attr("node_version_satisfies", Virtual, Constraint),
    imposed_constraint(ConstraintCause, "node_version_satisfies", Virtual, Constraint),
    condition_holds(ConstraintCause),
    not version_satisfies(Virtual, Constraint, Version).

% More specific error message if the version cannot satisfy some constraint
% Otherwise covered by `no_version_error` and `versions_conflict_error`.
error(0, "No valid version for '{0}' satisfies '@{1}'", Package, Constraint, startcauses, ConstraintCause)
  :- attr("node_version_satisfies", Package, Constraint),
     imposed_constraint(ConstraintCause, "node_version_satisfies", Package, Constraint),
     condition_holds(ConstraintCause),
     C = #count{ Version : attr("version", Package, Version), version_satisfies(Package, Constraint, Version)},
     C < 1.
