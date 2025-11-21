% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Heuristic to speed-up solves
%=============================================================================

% Decide about DAG atoms, before trying to guess facts used only in
% the internal representation
#heuristic attr("virtual_node", node(X, Virtual)). [80, level]
#heuristic attr("node", PackageNode). [80, level]
#heuristic attr("version", node(PackageID, Package), Version). [80, level]
#heuristic attr("variant_value", PackageNode, Variant, Value). [80, level]
#heuristic attr("node_target", node(PackageID, Package), Target). [80, level]

#heuristic attr("virtual_node", node(X, Virtual)). [600, init]
#heuristic attr("virtual_node", node(X, Virtual)). [-1, sign]
#heuristic attr("virtual_node", node(0, Virtual)) : node_depends_on_virtual(PackageNode, Virtual). [1@2, sign]
#heuristic attr("virtual_node", node(0, "c")).     [1@3, sign]
#heuristic attr("virtual_node", node(0, "cxx")).   [1@3, sign]
#heuristic attr("virtual_node", node(0, "libc")).   [1@3, sign]

#heuristic attr("node", PackageNode). [300, init]
#heuristic attr("node", PackageNode). [  4, factor]
#heuristic attr("node", PackageNode). [ -1, sign]
#heuristic attr("node", node(0, Dependency)) : attr("dependency_holds", ParentNode, Dependency, Type), not virtual(Dependency). [1@2, sign]

#heuristic attr("version", node(PackageID, Package), Version). [30, init]
#heuristic attr("version", node(PackageID, Package), Version). [-1, sign]
#heuristic attr("version", node(PackageID, Package), Version) : pkg_fact(Package, version_declared(Version, 0)), attr("node", node(PackageID, Package)). [ 1@2, sign]

% Use default targets
#heuristic attr("node_target", node(PackageID, Package), Target). [-1, sign]
#heuristic attr("node_target", node(PackageID, Package), Target) : target_weight(Target, 0), attr("node", node(PackageID, Package)). [1@2, sign]

% Use default variants
#heuristic attr("variant_value", PackageNode, Variant, Value). [30, init]
#heuristic attr("variant_value", PackageNode, Variant, Value). [-1, sign]
#heuristic attr("variant_value", PackageNode, Variant, Value) : variant_default_value(PackageNode, Variant, Value), attr("node", PackageNode). [1@2, sign]
