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
#show node/1.
#show hash/2.
#show depends_on/3.
#show version/2.
#show variant_value/3.
#show node_platform/2.
#show node_os/2.
#show node_target/2.
#show node_compiler/2.
#show node_compiler_version/3.
#show node_flag/3.
#show node_flag_compiler_default/1.
#show node_flag_source/2.
#show no_flags/2.
#show external_spec_selected/2.

#show build/1.

% names of optimization criteria
#show opt_criterion/2.

% deprecated packages
#show deprecated/2.

% error types
#show error_conflict_triggered/1.
#show error_no_version/1.
#show error_versions_conflict/3.
#show error_no_variant_value/2.
#show error_multiple_values_sv_variant/4.
#show error_invalid_variant_value/3.
#show error_version_unsatisfiable/2.
#show error_unnecessary/1.
#show error_cyclic_dependency/2.
#show error_no_provider/1.
#show error_multiple_providers/3.
#show error_invalid_external_spec/1.
#show error_inactive_variant_set/2.
#show error_disjoint_variant_values/4.
#show error_variant_none_and_other/3.
#show error_no_os/1.
#show error_multiple_os/3.
#show error_os_not_buildable/2.
#show error_os_incompatible/4.
#show error_no_target/1.
#show error_multiple_targets/3.
#show error_target_unsatisfiable/3.
#show error_target_incompatible/2.
#show error_compiler_target_mismatch/4.
#show error_invalid_target/2.
#show error_no_compiler_version/1.
#show error_multiple_compiler_versions/5.
#show error_compiler_os_mismatch/4.
#show error_no_platform/1.
#show error_multiple_platforms/3.
#show error_node_compiler_version_unsatisfiable/3.

% debug
