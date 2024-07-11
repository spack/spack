% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Heuristic to speed-up solves
%=============================================================================

% No duplicates by default (most of them will be true)
#heuristic attr("node",         node(PackageID, Package)). [100, init]
#heuristic attr("node",         node(PackageID, Package)). [  2, factor]
#heuristic attr("virtual_node", node(VirtualID, Virtual)). [100, init]
#heuristic attr("node",         node(1..X-1, Package)) : max_dupes(Package, X), not virtual(Package), X > 1. [-1, sign]
#heuristic attr("virtual_node", node(1..X-1, Package)) : max_dupes(Package, X), virtual(Package)    , X > 1. [-1, sign]

% Pick preferred version
#heuristic attr("version", node(PackageID, Package), Version) : pkg_fact(Package, version_declared(Version, Weight)), attr("node", node(PackageID, Package)).             [40, init]
#heuristic version_weight(node(PackageID, Package), 0)        : pkg_fact(Package, version_declared(Version, 0     )), attr("node", node(PackageID, Package)).             [ 1, sign]
#heuristic attr("version", node(PackageID, Package), Version) : pkg_fact(Package, version_declared(Version, 0     )), attr("node", node(PackageID, Package)).             [ 1, sign]
#heuristic attr("version", node(PackageID, Package), Version) : pkg_fact(Package, version_declared(Version, Weight)), attr("node", node(PackageID, Package)), Weight > 0. [-1, sign]

% Use default variants
#heuristic attr("variant_value", node(PackageID, Package), Variant, Value) : variant_default_value(Package, Variant, Value),     attr("node", node(PackageID, Package)). [40, true]
#heuristic attr("variant_value", node(PackageID, Package), Variant, Value) : not variant_default_value(Package, Variant, Value), attr("node", node(PackageID, Package)). [40, false]

% Use default operating system and platform
#heuristic attr("node_os", node(PackageID, Package), OS) : os(OS, 0), attr("root", node(PackageID, Package)). [40, true]
#heuristic attr("node_platform", node(PackageID, Package), Platform) : allowed_platform(Platform), attr("root", node(PackageID, Package)). [40, true]

% Use default targets
#heuristic attr("node_target", node(PackageID, Package), Target) : target_weight(Target, Weight), attr("node", node(PackageID, Package)). [30, init]
#heuristic attr("node_target", node(PackageID, Package), Target) : target_weight(Target, Weight), attr("node", node(PackageID, Package)). [ 2, factor]
#heuristic attr("node_target", node(PackageID, Package), Target) : target_weight(Target,      0), attr("node", node(PackageID, Package)). [ 1, sign]
#heuristic attr("node_target", node(PackageID, Package), Target) : target_weight(Target, Weight), attr("node", node(PackageID, Package)), Weight > 0. [-1, sign]

% Use the default compilers
#heuristic node_compiler(node(PackageID, Package), ID) : compiler_weight(ID, 0), compiler_id(ID), attr("node", node(PackageID, Package)). [30, init]
