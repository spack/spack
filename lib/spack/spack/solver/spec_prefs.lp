% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%-----------------------------------------------------------------
% Lockfile preferences.
%
% Attributes from specs in the lockfile are added to the solve as
% spec_pref(attr(Package, ...)) facts.
%
% Normally we *require* what is in the lockfile, but no_spec_pref
% let us tell the user what we would have to change from the
% lockfile to make the solve succeed. With `concretize --force`,
% these prefs keep us as close to the lockfile as possible.
%-----------------------------------------------------------------

% generated attribute may not be present
#defined spec_pref/1.

% Node is present and missing some spec preference attribute
no_spec_pref(Name, attr(Name, node(ID, Package)))
    :- attr("node", node(ID, Package)),
       not attr(Name, node(ID, Package)),
       spec_pref(attr(Name, Package)).

% Rules below just repeat the scenario above for attributes with
% different arity.
% TODO: redo the encoding to avoid all the arity repetition.
no_spec_pref(Name, attr(Name, node(ID, Package), A1))
    :- attr("node", node(ID, Package)),
       not attr(Name, node(ID, Package), A1),
       spec_pref(attr(Name, Package, A1)).

no_spec_pref(Name, attr(Name, node(ID, Package), A1, A2))
    :- attr("node", node(ID, Package)),
       not attr(Name, node(ID, Package), A1, A2),
       spec_pref(attr(Name, Package, A1, A2)),
       not multiple_nodes_attribute(Name).  % special case

no_spec_pref(Name, attr(Name, node(ID, Package), A1, A2, A3))
    :- attr("node", node(ID, Package)),
       not attr(Name, node(ID, Package), A1, A2, A3),
       spec_pref(attr(Name, Package, A1, A2, A3)),
       not multiple_nodes_attribute(Name).  % special case

no_spec_pref(Name, attr(Name, node(ID, Package), A1, A2, A3, A4))
    :- attr("node", node(ID, Package)),
       not attr(Name, node(ID, Package), A1, A2, A3, A4),
       spec_pref(attr(Name, Package, A1, A2, A3, A4)).

%-----------------------------------------------------------------
% Optimization for spec prefs
%-----------------------------------------------------------------
% Try hardest to prefer what was in the lockfile, with priority given to
% versions, then variants, then the rest.
def_spec_pref_priority("version", 2).
def_spec_pref_priority("variant_value", 1).

% if we defined a priority use it
spec_pref_priority(Name, Priority) :-
    no_spec_pref(Name, Attribute), def_spec_pref_priority(Name, Priority).
% otherwise use priority zero
spec_pref_priority(Name, 0) :-
    no_spec_pref(Name, Attribute), not def_spec_pref_priority(Name, _).
