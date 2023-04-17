% Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

% OS compatibility rules for reusing solves.
% os_compatible(RecentOS, OlderOS)
% OlderOS binaries can be used on RecentOS

% macOS
os_compatible("ventura", "monterey").
os_compatible("monterey", "bigsur").
os_compatible("bigsur", "catalina").

% glibc mapping
os_compatible("glibc2.37", "glibc2.36").
os_compatible("glibc2.36", "glibc2.35").
os_compatible("glibc2.35", "glibc2.34").
os_compatible("glibc2.34", "glibc2.33").
os_compatible("glibc2.33", "glibc2.32").
os_compatible("glibc2.32", "glibc2.31").
os_compatible("glibc2.31", "glibc2.30").
os_compatible("glibc2.30", "glibc2.29").
os_compatible("glibc2.29", "glibc2.28").
os_compatible("glibc2.28", "glibc2.27").
os_compatible("glibc2.27", "glibc2.26").
os_compatible("glibc2.26", "glibc2.25").
os_compatible("glibc2.25", "glibc2.24").
os_compatible("glibc2.24", "glibc2.23").

% musl mapping
os_compatible("musl1.2.3", "musl1.2.2").
os_compatible("musl1.2.2", "musl1.2.1").
os_compatible("musl1.2.1", "musl1.2.0").

% ubuntu <=> glibc mapping
os_compatible("ubuntu16.04", "glibc2.23"). os_compatible("glibc2.23", "ubuntu16.04").
os_compatible("ubuntu16.10", "glibc2.24"). os_compatible("glibc2.24", "ubuntu16.10").
os_compatible("ubuntu17.04", "glibc2.24"). os_compatible("glibc2.24", "ubuntu17.04").
os_compatible("ubuntu17.10", "glibc2.26"). os_compatible("glibc2.26", "ubuntu17.10").
os_compatible("ubuntu18.04", "glibc2.27"). os_compatible("glibc2.27", "ubuntu18.04").
os_compatible("ubuntu18.10", "glibc2.28"). os_compatible("glibc2.28", "ubuntu18.10").
os_compatible("ubuntu19.04", "glibc2.29"). os_compatible("glibc2.29", "ubuntu19.04").
os_compatible("ubuntu19.10", "glibc2.30"). os_compatible("glibc2.30", "ubuntu19.10").
os_compatible("ubuntu20.04", "glibc2.31"). os_compatible("glibc2.31", "ubuntu20.04").
os_compatible("ubuntu20.10", "glibc2.32"). os_compatible("glibc2.32", "ubuntu20.10").
os_compatible("ubuntu21.04", "glibc2.33"). os_compatible("glibc2.33", "ubuntu21.04").
os_compatible("ubuntu21.10", "glibc2.34"). os_compatible("glibc2.34", "ubuntu21.10").
os_compatible("ubuntu22.04", "glibc2.35"). os_compatible("glibc2.35", "ubuntu22.04").
os_compatible("ubuntu22.10", "glibc2.36"). os_compatible("glibc2.36", "ubuntu22.10").
os_compatible("ubuntu23.04", "glibc2.37"). os_compatible("glibc2.37", "ubuntu23.04").

% EL8
os_compatible("rhel8", "rocky8").
os_compatible("rhel8", "glibc2.28"). os_compatible("glibc2.28", "rhel8").
os_compatible("rhel7", "glibc2.17"). os_compatible("glibc2.17", "rhel7").

% sles
% note: `spack arch` reported major versions for opensuse, which is not a useful glibc
% proxy, since it was updated in minor releases:
%   opensuse 15.3 - 15.5: glibc 2.31
%   opensuse 15.0 - 15.2: glibc 2.26
os_compatible("opensuse15", "glibc2.26"). os_compatible("glibc2.31", "opensuse15")

% alpine <=> musl mapping
os_compatible("alpine3", "musl1.2.3"). os_compatible("musl1.2.3", "alpine3").
