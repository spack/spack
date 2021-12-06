% Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================-
% Display Results
%
% This section determines what parts of the model are printed at the end
%==============================================================================

% Spec-related functions.
% Used to build the result of the solve.
#show node/2.
#show hash/3.
#show depends_on/4.
#show version/3.
#show variant_value/4.
#show node_platform/3.
#show node_os/3.
#show node_target/3.
#show node_compiler/3.
#show node_compiler_version/4.
#show node_flag/4.
#show node_flag_compiler_default/2.
#show node_flag_source/3.
#show no_flags/3.
#show external_spec_selected/3.

#show build/2.

% names of optimization criteria
#show opt_criterion/2.

% deprecated packages
#show deprecated/3.
