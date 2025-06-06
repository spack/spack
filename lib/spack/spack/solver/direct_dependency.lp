% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

% A direct dependency is either a runtime requirement, or a build requirement
1 {
  build_requirement(PackageNode, node(0..X-1, DirectDependency)) : max_dupes(DirectDependency, X);
  runtime_requirement(PackageNode, node(0..X-1, DirectDependency)) : max_dupes(DirectDependency, X)
} 1 :- attr("direct_dependency", PackageNode, node_requirement("node", DirectDependency)),
       not external(PackageNode),
       not concrete(PackageNode).

1 {
  concrete_build_requirement(PackageNode, DirectDependency);
  runtime_requirement(PackageNode, node(0..X-1, DirectDependency)) : max_dupes(DirectDependency, X)
} 1 :- attr("direct_dependency", PackageNode, node_requirement("node", DirectDependency)),
       concrete(PackageNode).

%%%%
% Build requirement
%%%%

% A build requirement that is not concrete has a "build" only dependency
attr("depends_on", node(X, Parent), node(Y, BuildDependency), "build") :-
 build_requirement(node(X, Parent), node(Y, BuildDependency)),
 build(node(X, Parent)).

% Any other dependency type is forbidden
:- build_requirement(ParentNode, ChildNode),
   build(ParentNode),
   attr("depends_on", ParentNode, ChildNode, Type), Type != "build".

:- concrete_build_requirement(ParentNode, ChildPackage),
   concrete(ParentNode),
   attr("depends_on", ParentNode, node(_, ChildPackage), _).

%%%%
% Runtime requirement
%%%%

:- runtime_requirement(ParentNode, ChildNode),
   not 1 { attr("depends_on", ParentNode, ChildNode, "link"); attr("depends_on", ParentNode, ChildNode, "run") }.

attr(AttributeName, node(X, ChildPackage), A1)
  :- runtime_requirement(ParentNode, node(X, ChildPackage)),
     attr("direct_dependency", ParentNode, node_requirement(AttributeName, ChildPackage, A1)),
     AttributeName != "provider_set".

attr(AttributeName, node(X, ChildPackage), A1, A2)
  :- runtime_requirement(ParentNode, node(X, ChildPackage)),
     attr("direct_dependency", ParentNode, node_requirement(AttributeName, ChildPackage, A1, A2)).

attr(AttributeName, node(X, ChildPackage), A1, A2, A3)
  :- runtime_requirement(ParentNode, node(X, ChildPackage)),
     attr("direct_dependency", ParentNode, node_requirement(AttributeName, ChildPackage, A1, A2, A3)).

attr(AttributeName, node(X, ChildPackage), A1, A2, A3, A4)
  :- runtime_requirement(ParentNode, node(X, ChildPackage)),
     attr("direct_dependency", ParentNode, node_requirement(AttributeName, ChildPackage, A1, A2, A3, A4)).
