% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%-----------------
% Domain heuristic
%-----------------
#heuristic attr("hash", node(0, Package), Hash) : literal(_, "root", Package). [45, init]
#heuristic attr("root", node(0, Package)) : literal(_, "root", Package). [45, true]
#heuristic attr("node", node(0, Package)) : literal(_, "root", Package). [45, true]
#heuristic attr("node", node(0, Package)) : literal(_, "node", Package). [45, true]

#heuristic attr("version", node(0, Package), Version) : facts(Package, version_declared(Version, 0)), attr("root", node(0, Package)). [40, true]
#heuristic version_weight(node(0, Package), 0) : facts(Package, version_declared(Version, 0)), attr("root", node(0, Package)). [40, true]
#heuristic attr("variant_value", node(0, Package), Variant, Value) : variant_default_value(Package, Variant, Value), attr("root", node(0, Package)). [40, true]
#heuristic attr("node_target", node(0, Package), Target) : facts(Package, target_weight(Target, 0)), attr("root", node(0, Package)). [40, true]
#heuristic node_target_weight(node(0, Package), 0) : attr("root", node(0, Package)). [40, true]
#heuristic node_compiler(node(0, Package), CompilerID) : default_compiler_preference(ID, 0), compiler_id(ID), attr("root", node(0, Package)). [40, true]

#heuristic version_weight(node(0, Package), 0) : attr("node", node(0, Package)). [20, true]

#heuristic attr("node_target", node(0, Package), Target) : facts(Package, target_weight(Target, 0)), attr("node", node(0, Package)). [20, true]
#heuristic node_target_weight(PackageNode, 0) : attr("node", PackageNode). [20, true]
#heuristic node_compiler(node(0, Package), ID) : default_compiler_preference(ID, 0), compiler_id(ID), attr("node", node(0, Package)). [15, true]
