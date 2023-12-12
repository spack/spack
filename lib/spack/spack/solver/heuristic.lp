% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Heuristic to speed-up solves (node with ID 0)
%=============================================================================


%-----------------
% Domain heuristic
%-----------------

% Root node
#heuristic attr("version", node(0, Package), Version) : pkg_fact(Package, version_declared(Version, 0)), attr("root", node(0, Package)). [35, true]
#heuristic version_weight(node(0, Package), 0) : pkg_fact(Package, version_declared(Version, 0)), attr("root", node(0, Package)). [35, true]
#heuristic attr("variant_value", node(0, Package), Variant, Value) : variant_default_value(Package, Variant, Value), attr("root", node(0, Package)). [35, true]
#heuristic attr("node_target", node(0, Package), Target) : target_weight(Target, 0), attr("root", node(0, Package)). [35, true]
#heuristic node_target_weight(node(0, Package), 0) : attr("root", node(0, Package)). [35, true]
#heuristic node_compiler(node(0, Package), CompilerID) : compiler_weight(ID, 0), compiler_id(ID), attr("root", node(0, Package)). [35, true]

% Providers
#heuristic attr("node", node(0, Package)) : default_provider_preference(Virtual, Package, 0), possible_in_link_run(Package). [30, true]
