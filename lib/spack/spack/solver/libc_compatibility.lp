% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Libc compatibility rules for reusing solves.
%
% These rules are used on Linux
%=============================================================================

% A package cannot be reused if the libc is not compatible with it
error(100, "Cannot reuse {0} since we cannot determine libc compatibility", ReusedPackage)
  :- provider(node(X, LibcPackage), node(0, "libc")),
     attr("version", node(X, LibcPackage), LibcVersion),
     attr("hash", node(R, ReusedPackage), Hash),
     % Libc packages can be reused without the "compatible_libc" attribute
     ReusedPackage != LibcPackage,
     not attr("compatible_libc", node(R, ReusedPackage), LibcPackage, LibcVersion).

% Check whether the DAG has any built package
has_built_packages() :- build(X), not external(X).

% A libc is needed in the DAG
:- has_built_packages(), not provider(_, node(0, "libc")).

% The libc must be chosen among available ones
:- has_built_packages(),
   provider(node(X, LibcPackage), node(0, "libc")),
   attr("node", node(X, LibcPackage)),
   attr("version", node(X, LibcPackage), LibcVersion),
   not allowed_libc(LibcPackage, LibcVersion).

% A built node must depend on libc
:- build(PackageNode),
   provider(LibcNode, node(0, "libc")),
   not external(PackageNode),
   not depends_on(PackageNode, LibcNode).
