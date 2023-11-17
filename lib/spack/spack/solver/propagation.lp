% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% TODO: Later
%=============================================================================

% propagate flags when compiler match
attr("node_flag_propagate", PackageNode, FlagType, Flag, Source) :- % source is a node() attribute
  attr("node_flag_propagation_candidate", PackageNode, FlagType, Flag, Source),
  not attr("node_flag_set", PackageNode, FlagType, _).

attr("node_flag_propagation_candidate", PackageNode, FlagType, Flag, Source) :- % source is a node() attribute
  same_compiler(ParentNode, PackageNode),
  attr("node_flag_propagation_candidate", ParentNode, FlagType, _, Source),
  attr("node_flag", Source, FlagType, Flag),
  flag_type(FlagType).

error(100, "{0} and {1} cannot both propagate compiler flags '{2}' to {3}", Source1, Source2, PackageNode, FlagType) :-
  same_compiler(Source1, PackageNode),
  same_compiler(Source2, PackageNode),
  attr("node_flag_propagate", _, FlagType, _, Source1),
  attr("node_flag_propagate", _, FlagType, _, Source2),
  Source1 < Source2.

attr("node_flag_source", PackageNode, FlagType, Q)
  :- attr("node_flag_propagate", PackageNode, FlagType, _, Q).

attr("node_flag", PackageNode, FlagType, Flag) :- attr("node_flag_propagate", PackageNode, FlagType, Flag, _).
