% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Splicing
%=============================================================================
% Splicing alters the encoding of hashes, because splices are always introduced
% in the dependency of hashes. Without splicing, hashes impose their constraints
% directly; with splicing we introduce a layer of indirection using the atom
% `hash_attr`


% splice_set_id describes the compatible set of attributes which must hold for 
% splice to be valid between the NodePackage and the BasePackage. It has the 
% following form: splice_set_id(Index, NodePackageName, BasePackageName, N)
% where N is the number of conditions which must hold for a valid spice (i.e., the
% number of can_splice_attrs associated with this splice set)
#defined splice_set_id/4.

% can_splice_attr is a family of package facts that determine when a package may 
% be substituted for a hash. It has the general form:
% can_splice_attr(SpiceSetId, NodePackageName, NodeArgs*, BasePackageName, BaseArgs*)
#defined can_splice_attr/4.
#defined can_splice_attr/6.
#defined can_splice_attr/8.
#defined can_splice_attr/10.

% These are the previously concretized attributes of the installed package as 
% a hash. It has the general form:
% hash_attr(Hash, Attribute, PackageName, Args*)
#defined hash_attr/3.
#defined hash_attr/4.
#defined hash_attr/5.
#defined hash_attr/6.
#defined hash_attr/7.

% hash_attrs are versions, but can_splice_attr are usually node_version_satisfies
hash_attr(Hash, "node_version_satisfies", PackageName, Constraint)
  :- hash_attr(Hash, "version", PackageName, Version),
     pkg_fact(PackageName, version_satisfies(Constraint, Version)).

% Whether a package can be spliced is specified by an indexed set of facts for
% each package (indexed by SID) which must match between the "splice node",
% identified by PackageName, and the "base hash", identified by BaseName.
% N is the number of conditions which must hold for the set to be valid
abi_splice_conditions_hold(SID, node(NID, PackageName), BasePackageName, BaseHash) :-
  splice_set_id(SID, PackageName, BasePackageName, N),
  installed_hash(BasePackageName, BaseHash),
  attr("node", node(NID, PackageName)),
  N { 
    hash_attr(BaseHash, Attr, BasePackageName) :
      can_splice_attr(SID, Attr, PackageName, BasePackageName),
      attr(Attr, node(NID, PackageName));
    hash_attr(BaseHash, Attr, BasePackageName, BA1) :
      can_splice_attr(SID, Attr, PackageName, PA1, BasePackageName, BA1),
      attr(Attr, node(NID, PackageName), PA1);
    hash_attr(BaseHash, Attr, BasePackageName, BA1, BA2) :
      can_splice_attr(SID, Attr, PackageName, PA1, PA2, BasePackageName, BA1, BA2),
      attr(Attr, node(NID, PackageName), PA1, PA2)
  } N.


% In general, hashes impose the constraints of their concrete specs,
% but "hash", "depends_on", and "virtual_on_edge" are special.  "hash"
% and "depends_on" are special because the choice to splice is done
% when imposing the dependencies of hashes.  "virtual_on_edge" is
% special because when splicing a virtual, the actual name of the
% dependency might change
imposed_constraint(Hash, Attr, PackageName) :-
  hash_attr(Hash, Attr, PackageName).
imposed_constraint(Hash, Attr, PackageName, A1) :-
  hash_attr(Hash, Attr, PackageName, A1), Attr != "hash".
imposed_constraint(Hash, Attr, PackageName, Arg1, Arg2) :- 
  hash_attr(Hash, Attr, PackageName, Arg1, Arg2),
  Attr != "depends_on",
  Attr != "virtual_on_edge".
imposed_constraint(Hash, Attr, PackageName, A1, A2, A3) :-
  hash_attr(Hash, Attr, PackageName, A1, A2, A3).

% Without abi_splice_conditions_hold, a splice is not possible, so it
% is safe to just impose the hash
imposed_constraint(Hash, "hash", HashName, ImpHash) :- 
  hash_attr(Hash, "hash", HashName, ImpHash),
  not abi_splice_conditions_hold(_, _, HashName, ImpHash).

% If a splice is possible make a choice as to whether to impose the exact hash,
% or introduce the splice 
{ imposed_constraint(ParentHash, "hash", ChildName, ChildHash) } :-
  hash_attr(ParentHash, "hash", ChildName, ChildHash),
  abi_splice_conditions_hold(_, node(SID, SpliceName), ChildName, ChildHash).

attr("splice_hash", node(SID, SpliceName), ChildName, ChildHash, node(ID, PackageName)) :- 
  attr("hash", node(ID, PackageName), ParentHash),
  hash_attr(ParentHash, "hash", ChildName, ChildHash),
  abi_splice_conditions_hold(_, node(SID, SpliceName), ChildName, ChildHash),
  not imposed_constraint(ParentHash, "hash", ChildName, ChildHash). 

% If there is no splice, the normal dependency can be imposed 
% NOTE: the use of dependency_holds is for performance, using depends_on directly
% introduced a 10x slowdown in grounding     
imposed_constraint(Hash, "dependency_holds", PackageName, DepName, Type) :-
  hash_attr(Hash, "depends_on", PackageName, DepName, Type),
  hash_attr(Hash, "hash", DepName, DepHash),
  not attr("splice_hash", _, DepName, DepHash, _).

% Otherwise we can impose the spliced dependency 
imposed_constraint(Hash, "dependency_holds", PackageName, SpliceName, Type) :-
  hash_attr(Hash, "depends_on", PackageName, DepName, Type),
  hash_attr(Hash, "hash", DepName, DepHash),
  attr("splice_hash", node(SID, SpliceName), DepName, DepHash, node(ID, PackageName)).

imposed_constraint(Hash, "virtual_on_edge", PackageName, DepName, VirtName) :-
  hash_attr(Hash, "virtual_on_edge", PackageName, DepName, VirtName),
  not attr("splice_hash", _, DepName, _, _).

imposed_constraint(Hash, "virtual_on_edge", PackageName, SpliceName, VirtName) :-
  hash_attr(Hash, "virtual_on_edge", PackageName, DepName, VirtName),
  attr("splice_hash", node(SID, SpliceName), DepName, _, _).


