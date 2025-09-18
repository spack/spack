% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Heuristic to speed-up solves
%=============================================================================

#heuristic attr("virtual_node", node(X, Virtual)). [1000, init]
#heuristic attr("virtual_node", node(X, Virtual)). [-1, sign]
#heuristic attr("virtual_node", node(0, Virtual)) : node_depends_on_virtual(PackageNode, Virtual). [1@2, sign]
#heuristic attr("virtual_node", node(0, "c")).       [1@3, sign]
#heuristic attr("virtual_node", node(0, "cxx")).     [1@3, sign]
#heuristic attr("virtual_node", node(0, "libc")).    [1@3, sign]

#heuristic node_compiler(ParentNode, CompilerNode, Language). [200, init]
#heuristic node_compiler(ParentNode, CompilerNode, Language). [ -1, sign]
#heuristic node_compiler(ParentNode, CompilerNode, Language) : attr("depends_on", ParentNode, CompilerNode, "build"), provider_weight(CompilerNode, Language, 0), language(Language). [1@2, sign]

#heuristic attr("node", PackageNode). [100, init]
#heuristic attr("node", PackageNode). [  4, factor]
#heuristic attr("node", PackageNode). [ -1, sign]
#heuristic attr("node", node(0, Dependency)) : attr("dependency_holds", ParentNode, Dependency, Type), not virtual(Dependency). [1@2, sign]
#heuristic attr("node", node(0, Provider)) : provider_weight_from_config("c", Provider, 0).       [ 1@3, sign]
#heuristic attr("node", node(0, Provider)) : provider_weight_from_config("cxx", Provider, 0).     [ 1@3, sign]
#heuristic attr("node", node(0, Provider)) : provider_weight_from_config("fortran", Provider, 0). [ 1@3, sign]

#heuristic attr("depends_on", ParentNode, ChildNode, Type). [100, init]
#heuristic attr("depends_on", ParentNode, ChildNode, Type). [4,  factor]
#heuristic attr("depends_on", ParentNode, ChildNode, Type). [-1, sign]
#heuristic attr("depends_on", ParentNode, node(0, Dependency), Type) : attr("dependency_holds", ParentNode, Dependency, Type), not virtual(Dependency). [1@2, sign]
#heuristic attr("depends_on", ParentNode, ProviderNode       , Type) : node_depends_on_virtual(ParentNode, Virtual, Type), provider(ProviderNode, node(VirtualID, Virtual)). [1@2, sign]

#heuristic attr("version", node(PackageID, Package), Version). [30, init]
#heuristic attr("version", node(PackageID, Package), Version). [-1, sign]

#heuristic version_weight(node(PackageID, Package), Weight).                                          [30, init]
#heuristic version_weight(node(PackageID, Package), Weight).                                          [-1  , sign]

% Use default variants
#heuristic attr("variant_value", PackageNode, Variant, Value). [50, init]
#heuristic attr("variant_value", PackageNode, Variant, Value). [-1, sign]

% Use default targets
#heuristic attr("node_target", node(PackageID, Package), Target). [-1, sign]
#heuristic attr("node_target", node(PackageID, Package), Target) : target_weight(Target, 0), attr("node", node(PackageID, Package)). [1@2, sign]
