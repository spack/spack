% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Heuristic to speed-up solves (node with ID > 0)
%=============================================================================

% node(ID, _)
#heuristic attr("version", node(ID, Package), Version) : pkg_fact(Package, version_declared(Version, 0)), attr("node", node(ID, Package)), ID > 0. [25-5*ID, true]
#heuristic version_weight(node(ID, Package), 0) : pkg_fact(Package, version_declared(Version, 0)), attr("node", node(ID, Package)), ID > 0. [25-5*ID, true]
#heuristic attr("variant_value", node(ID, Package), Variant, Value) : variant_default_value(Package, Variant, Value), attr("node", node(ID, Package)), ID > 0. [25-5*ID, true]
#heuristic attr("node_target", node(ID, Package), Target) : pkg_fact(Package, target_weight(Target, 0)), attr("node", node(ID, Package)), ID > 0. [25-5*ID, true]
#heuristic node_target_weight(node(ID, Package), 0) : attr("node", node(ID, Package)), ID > 0. [25-5*ID, true]
#heuristic node_compiler(node(ID, Package), CompilerID) : compiler_weight(CompilerID, 0), compiler_id(CompilerID), attr("node", node(ID, Package)), ID > 0. [25-5*ID, true]

% node(ID, _), split build dependencies
#heuristic attr("version", node(ID, Package), Version) : pkg_fact(Package, version_declared(Version, 0)), attr("node", node(ID, Package)), multiple_unification_sets(Package), ID > 0. [25, true]
#heuristic version_weight(node(ID, Package), 0) : pkg_fact(Package, version_declared(Version, 0)), attr("node", node(ID, Package)), multiple_unification_sets(Package), ID > 0. [25, true]
#heuristic attr("variant_value", node(ID, Package), Variant, Value) : variant_default_value(Package, Variant, Value), attr("node", node(ID, Package)), multiple_unification_sets(Package), ID > 0. [25, true]
#heuristic attr("node_target", node(ID, Package), Target) : pkg_fact(Package, target_weight(Target, 0)), attr("node", node(ID, Package)), multiple_unification_sets(Package), ID > 0. [25, true]
#heuristic node_target_weight(node(ID, Package), 0) : attr("node", node(ID, Package)), multiple_unification_sets(Package), ID > 0. [25, true]
#heuristic node_compiler(node(ID, Package), CompilerID) : compiler_weight(CompilerID, 0), compiler_id(CompilerID), attr("node", node(ID, Package)), multiple_unification_sets(Package), ID > 0. [25, true]
