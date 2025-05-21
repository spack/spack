% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

attr("direct_dependency", PackageNode, build_requirement(A1, A2)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2)).
attr("direct_dependency", PackageNode, build_requirement(A1, A2, A3)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2, A3)).
attr("direct_dependency", PackageNode, build_requirement(A1, A2, A3, A4)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2, A3, A4)).
attr("direct_dependency", PackageNode, build_requirement(A1, A2, A3, A4, A5)) :- attr("direct_dependency", PackageNode, node_requirement(A1, A2, A3, A4, A5)).