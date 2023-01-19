% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

% OS compatibility rules for reusing solves.
% os_compatible(RecentOS, OlderOS)
% OlderOS binaries can be used on RecentOS

% macOS
os_compatible("monterey", "bigsur").
os_compatible("bigsur", "catalina").

% Ubuntu
os_compatible("ubuntu22.04", "ubuntu21.10").
os_compatible("ubuntu21.10", "ubuntu21.04").
os_compatible("ubuntu21.04", "ubuntu20.10").
os_compatible("ubuntu20.10", "ubuntu20.04").
os_compatible("ubuntu20.04", "ubuntu19.10").
os_compatible("ubuntu19.10", "ubuntu19.04").
os_compatible("ubuntu19.04", "ubuntu18.10").
os_compatible("ubuntu18.10", "ubuntu18.04").

%EL8
os_compatible("rhel8", "rocky8").
