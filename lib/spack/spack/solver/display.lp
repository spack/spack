% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================-
% Display Results
%
% This section determines what parts of the model are printed at the end
%==============================================================================

% Spec attributes
#show attr/2.
#show attr/3.
#show attr/4.

% names of optimization criteria
#show opt_criterion/3.

% error types
#show error/2.
#show error/3.
#show error/4.
#show error/5.
#show error/6.
#show error/7.

% debug
#show depth/2.
%#show depends_on/2.

%node(Package) :- attr("node", Package).
%#show node/1.

%version(Package, Version) :- attr("version", Package, Version).
%#show version/2.

#show impose/1.
