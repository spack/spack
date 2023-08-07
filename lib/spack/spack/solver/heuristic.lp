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

% Root node
#heuristic attr("version", node(0, Package), Version) : pkg_fact(Package, version_declared(Version, 0)), attr("root", node(0, Package)). [35, true]
#heuristic version_weight(node(0, Package), 0) : pkg_fact(Package, version_declared(Version, 0)), attr("root", node(0, Package)). [35, true]
#heuristic attr("variant_value", node(0, Package), Variant, Value) : variant_default_value(Package, Variant, Value), attr("root", node(0, Package)). [35, true]
#heuristic attr("node_target", node(0, Package), Target) : pkg_fact(Package, target_weight(Target, 0)), attr("root", node(0, Package)). [35, true]
#heuristic node_target_weight(node(0, Package), 0) : attr("root", node(0, Package)). [35, true]
#heuristic node_compiler(node(0, Package), CompilerID) : default_compiler_preference(ID, 0), compiler_id(ID), attr("root", node(0, Package)). [35, true]

% Providers
#heuristic attr("node", node(0, Package)) : default_provider_preference(Virtual, Package, 0), possible_in_link_run(Package). [30, true]
%#heuristic provider(node(0, Package), node(0, Virtual)) : default_provider_preference(Virtual, Package, 0), possible_in_link_run(Package). [30, true]
%#heuristic provider_weight(node(0, Package), node(0, Virtual), 0) : default_provider_preference(Virtual, Package, 0), possible_in_link_run(Package). [30, true]

% node(ID, _)
#heuristic attr("version", node(ID, Package), Version) : pkg_fact(Package, version_declared(Version, ID)), attr("node", node(ID, Package)). [25-5*ID, true]
#heuristic version_weight(node(ID, Package), ID) : pkg_fact(Package, version_declared(Version, ID)), attr("node", node(ID, Package)). [25-5*ID, true]
#heuristic attr("variant_value", node(ID, Package), Variant, Value) : variant_default_value(Package, Variant, Value), attr("node", node(ID, Package)). [25-5*ID, true]
#heuristic attr("node_target", node(ID, Package), Target) : pkg_fact(Package, target_weight(Target, ID)), attr("node", node(ID, Package)). [25-5*ID, true]
#heuristic node_target_weight(node(ID, Package), ID) : attr("node", node(ID, Package)). [25-5*ID, true]
#heuristic node_compiler(node(ID, Package), CompilerID) : default_compiler_preference(ID, ID), compiler_id(ID), attr("node", node(ID, Package)). [25-5*ID, true]

% node(ID, _), split build dependencies
#heuristic attr("version", node(ID, Package), Version) : pkg_fact(Package, version_declared(Version, ID)), attr("node", node(ID, Package)), multiple_unification_sets(Package). [25, true]
#heuristic version_weight(node(ID, Package), ID) : pkg_fact(Package, version_declared(Version, ID)), attr("node", node(ID, Package)), multiple_unification_sets(Package). [25, true]
#heuristic attr("variant_value", node(ID, Package), Variant, Value) : variant_default_value(Package, Variant, Value), attr("node", node(ID, Package)), multiple_unification_sets(Package). [25, true]
#heuristic attr("node_target", node(ID, Package), Target) : pkg_fact(Package, target_weight(Target, ID)), attr("node", node(ID, Package)), multiple_unification_sets(Package). [25, true]
#heuristic node_target_weight(node(ID, Package), ID) : attr("node", node(ID, Package)), multiple_unification_sets(Package). [25, true]
#heuristic node_compiler(node(ID, Package), CompilerID) : default_compiler_preference(ID, ID), compiler_id(ID), attr("node", node(ID, Package)), multiple_unification_sets(Package). [25, true]
