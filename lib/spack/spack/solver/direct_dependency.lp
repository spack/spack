% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

% A direct dependency is either a runtime requirement, or a build requirement
1 {
  build_requirement(PackageNode, node(0..X-1, DirectDependency)) : max_dupes(DirectDependency, X)
} 1 :- attr("direct_dependency", PackageNode, node_requirement("node", DirectDependency)),
       not external(PackageNode),
       not concrete(PackageNode).

%%%%
% Build requirement
%%%%

% A build requirement that is not concrete has a "build" only dependency
attr("depends_on", node(X, Parent), node(Y, BuildDependency), "build") :-
 build_requirement(node(X, Parent), node(Y, BuildDependency)),
 build(node(X, Parent)).

attr("direct_dependency", PackageNode, build_requirement(A1, A2)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2)).
attr("direct_dependency", PackageNode, build_requirement(A1, A2, A3)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2, A3)).
attr("direct_dependency", PackageNode, build_requirement(A1, A2, A3, A4)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2, A3, A4)).
attr("direct_dependency", PackageNode, build_requirement(A1, A2, A3, A4, A5)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2, A3, A4, A5)).
