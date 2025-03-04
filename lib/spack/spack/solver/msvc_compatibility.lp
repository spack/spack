% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% msvc compatibility rules for reusing solves.
%
% These rules are used on Windows w/ MSVC
%=============================================================================

% A package cannot be reused if the msvc is not compatible with it
error(100, "Cannot reuse {0} since we cannot determine msvc compatibility", ReusedPackage)
  :- provider(node(X, MsvcRuntimePackage), node(0, "msvc-runtime")),
     attr("version", node(X, MsvcRuntimePackage), MsvcRuntimeVersion),
     concrete(node(R, Reusedpackage)),
     attr("needs_msvc_runtime", node(R, ReusedPackage)),
     not attr("compatible_msvc_runtime", node(R, ReusedPackage), MsvcRuntimePackage, MsvcRuntimeVersion).

% If we have a compiler we're guarunteed to have an MSVC Runtime
% Ensure it's compatible
error(100, "Cannot reuse {0} since we cannot determine msvc-runtime compatibility", ReusedPackage)
  :- not provider(_, node(0, "msvc-runtime")),
     concrete(node(R, ReusedPackage)),
     attr("needs_msvc_runtime", node(R, ReusedPackage)),
     not attr("compatible_msvc_runtime", node(R, ReusedPackage), _, _).

% Non-libc reused specs must be host libc compatible. In case we build packages, we get a
% host compatible libc provider from other rules. If nothing is built, there is no libc provider,
% since it's pruned from reusable specs, meaning we have to explicitly impose reused specs are host
% compatible.
%:- attr("hash", node(R, ReusedPackage), Hash),
%   not provider(node(R, ReusedPackage), node(0, "msvc-runtime")),
%   not attr("compatible_msvc_runtime", node(R, ReusedPackage), _, _).

% The msvc-runtime provider must be one that a compiler can target
:- has_built_packages(),
   provider(node(X, MsvcRuntimePackage), node(0, "msvc-runtime")),
   attr("node", node(X, MsvcRuntimePackage)),
   attr("version", node(X, MsvcRuntimePackage), MsvcRuntimeVersion),
   not host_msvc(MsvcRuntimePackage, MsvcRuntimeVersion).
