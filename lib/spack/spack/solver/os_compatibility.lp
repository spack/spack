% Copyright Spack Project Developers. See COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% OS compatibility rules for reusing solves.
% os_compatible(RecentOS, OlderOS)
% OlderOS binaries can be used on RecentOS
%
% These rules are used on every platform, but Linux
%=============================================================================

% macOS
os_compatible("goldengate", "tahoe").
os_compatible("tahoe", "sequoia").
os_compatible("sequoia", "sonoma").
os_compatible("sonoma", "ventura").
os_compatible("ventura", "monterey").
os_compatible("monterey", "bigsur").
os_compatible("bigsur", "catalina").

% every OS is compatible with itself. We can use `os_compatible` to declare
os_compatible(OS, OS) :- os(OS).

% Transitive compatibility among operating systems
os_compatible(OS1, OS3) :- os_compatible(OS1, OS2), os_compatible(OS2, OS3).

% Dependency operating systems compatible with a node's own OS. This is O(N * OS^2)
dep_os_compatible(PackageNode, DependencyOS)
  :- attr("node_os", PackageNode, PackageNodeOS),
     os_compatible(PackageNodeOS, DependencyOS).

% can't have dependencies on incompatible OS's.  This is O(E * OS)
error(100, "{0} cannot use dependency {1} built for 'os={2}' (incompatible operating system)", Package, Dependency, DependencyOS)
  :- depends_on(node(X, Package), node(Y, Dependency)),
     attr("node_os", node(Y, Dependency), DependencyOS),
     not dep_os_compatible(node(X, Package), DependencyOS),
     build(node(X, Package)).

% We can select only operating systems compatible with the ones
% for which we can build software. We need a cardinality constraint
% since we might have more than one "buildable_os(OS)" fact.
:- not 1 { os_compatible(CurrentOS, ReusedOS) : buildable_os(CurrentOS) },
   attr("node_os", Package, ReusedOS).
