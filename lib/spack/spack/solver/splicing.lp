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
    hash_attr(BaseHash, Attr, BasePackageName) : can_splice_attr(SID, Attr, PackageName, BasePackageName), attr(Attr, node(NID, PackageName));
    hash_attr(BaseHash, Attr, BasePackageName, BA1) : can_splice_attr(SID, Attr, PackageName, PA1, BasePackageName, BA1), attr(Attr, node(NID, PackageName), PA1);
    hash_attr(BaseHash, Attr, BasePackageName, BA1, BA2) : can_splice_attr(SID, Attr, PackageName, PA1, PA2, BasePackageName, BA1, BA2), attr(Attr, node(NID, PackageName), PA1, PA2)
  } N.


% These rules just recover the precise hash semantics, namely that pure hashes 
% impose their attributes
imposed_constraint(Hash, Attr, PackageName) :- 
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, Attr, PackageName).

% "virtual_node" is a weird attribute, since it does not reference the name of
% of the package its referring to, but the name of the virtual it provides
imposed_constraint(Hash, "virtual_node", VirtName) :-
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, "virtual_node", VirtName).

% "hash" is a weird attribute, it's where splices can occur
imposed_constraint(Hash, Attr, PackageName, Arg1) :- 
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, Attr, PackageName, Arg1),
  Attr != "hash".

% Similarly, since splices can affect the names of dependent hashes, we need to 
% treat is special as well
imposed_constraint(Hash, Attr, PackageName, Arg1, Arg2) :- 
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, Attr, PackageName, Arg1, Arg2),
  Attr != "depends_on".

imposed_constraint(Hash, Attr, PackageName, Arg1, Arg2, Arg3) :- 
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, Attr, PackageName, Arg1, Arg2, Arg3).
  
% The general idea is that splicing need only be introduced on hashes that are
% dependencies of other hashes. If a hash is not a dependency of another hash, 
% then it is either a root, or the dependency of a package that we are building, 
% neither of which require a splice. 

% The base case, where the dependent hash does not have any ABI compatibility 
% with the selected node
imposed_constraint(Hash, "hash", HashName, ImpHash) :- 
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, "hash", HashName, ImpHash),
  not abi_splice_conditions_hold(_, _, HashName, ImpHash).
  
% The choice case of whether to keep the hash pure, or introduce a splice into 
% the dependencies 
1 { 
  imposed_constraint(ParentHash, "hash", ChildName, ChildHash); 
  attr("splice_hash", node(SID, SpliceName), ChildName, ChildHash, node(ID, PackageName)) : attr("node", node(SID, SpliceName))
} 1 :-
  attr("hash", node(ID, PackageName), ParentHash),
  hash_attr(ParentHash, "hash", ChildName, ChildHash),
  abi_splice_conditions_hold(_, node(SID, SpliceName), ChildName, ChildHash).

:- attr("hash", _, ChildHash), attr("splice_hash", _, _, ChildHash, _), internal_error("Cannot splice into a hash in use").

% depends_on works normally if the hash is not a splice, since the name will not 
% have changed 
imposed_constraint(Hash, "depends_on", PackageName, DepName, Type) :-
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, "depends_on", PackageName, DepName, Type),
  hash_attr(Hash, "hash", DepName, DepHash),
  not attr("splice_hash", _, DepName, DepHash, _).

% If there is a splice, the name of the dependency might change (e.g. splicing 
% a different virtual provider), but the splice_hash attribute has enough info 
% to make this change 
imposed_constraint(Hash, "depends_on", PackageName, SpliceName, Type) :-
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, "depends_on", PackageName, DepName, Type),
  hash_attr(Hash, "hash", DepName, DepHash),
  attr("splice_hash", node(SID, SpliceName), DepName, DepHash, _).

imposed_constraint(Hash, "virtual_on_edge", PackageName, SpliceName, VirtName) :-
  attr("hash", node(ID, PackageName), Hash),
  hash_attr(Hash, "virtual_on_edge", PackageName, DepName, VirtName),
  attr("splice_hash", node(SID, SpliceName), DepName, _, _).
