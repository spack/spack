%=============================================================================
% Generate
%=============================================================================

%-----------------------------------------------------------------------------
% Version semantics
%-----------------------------------------------------------------------------

% versions are declared w/priority -- declared with priority implies declared
version_declared(P, V) :- version_declared(P, V, _).

% If something is a package, it has only one version and that must be a
% possible version.
1 { version(P, V) : version_possible(P, V) } 1 :- node(P).

% If a version is declared but conflicted, it's not possible.
version_possible(P, V) :- version_declared(P, V), not version_conflict(P, V).

version_weight(P, V, N) :- version(P, V), version_declared(P, V, N).

#defined version_conflict/2.

%-----------------------------------------------------------------------------
% Dependency semantics
%-----------------------------------------------------------------------------
% Dependencies of any type imply that one package "depends on" another
depends_on(P, D) :- depends_on(P, D, _).

% declared dependencies are real if they're not virtual
depends_on(P, D, T) :- declared_dependency(P, D, T), not virtual(D), node(P).

% if you declare a dependency on a virtual, you depend on one of its providers
1 { depends_on(P, Q, T) : provides_virtual(Q, V) } 1
    :- declared_dependency(P, V, T), virtual(V), node(P).

% for any virtual, there can be at most one provider in the DAG
provider(P, V) :- node(P), provides_virtual(P, V).
0 { provider(P, V) : node(P) } 1 :- virtual(V).

% give dependents the virtuals they want
provider_weight(D, N)
    :- virtual(V), depends_on(P, D), provider(D, V),
       pkg_provider_preference(P, V, D, N).
provider_weight(D, N)
    :- virtual(V), depends_on(P, D), provider(D, V),
       not pkg_provider_preference(P, V, D, _),
       default_provider_preference(V, D, N).

% if there's no preference for something, it costs 100 to discourage its
% use with minimization
provider_weight(D, 100)
    :- virtual(V), depends_on(P, D), provider(D, V),
       not pkg_provider_preference(P, V, D, _),
       not default_provider_preference(V, D, _).

% all nodes must be reachable from some root
needed(D) :- root(D), node(D).
needed(D) :- root(P), depends_on(P, D).
needed(D) :- needed(P), depends_on(P, D), node(P).
:- node(P), not needed(P).

% real dependencies imply new nodes.
node(D) :- node(P), depends_on(P, D).

% do not warn if generated program contains none of these.
#defined depends_on/3.
#defined declared_dependency/3.
#defined virtual/1.
#defined provides_virtual/2.
#defined pkg_provider_preference/4.
#defined default_provider_preference/3.
#defined root/1.

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------
% one variant value for single-valued variants.
1 { variant_value(P, V, X) : variant_possible_value(P, V, X) } 1
    :- node(P), variant(P, V), variant_single_value(P, V).

% if a variant is set to anything, it is considered 'set'.
variant_set(P, V) :- variant_set(P, V, _).

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(P, V, X) :- node(P), variant(P, V), variant_set(P, V, X).

% prefer default values.
variant_not_default(P, V, X, 1)
    :- variant_value(P, V, X),
       not variant_default_value(P, V, X),
       node(P).

variant_not_default(P, V, X, 0)
    :- variant_value(P, V, X),
       variant_default_value(P, V, X),
       node(P).

% suppress wranings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant_set/3.
#defined variant_single_value/2.

%-----------------------------------------------------------------------------
% Architecture semantics
%-----------------------------------------------------------------------------

% one platform, os, target per node.
1 { arch_platform(P, A) : arch_platform(P, A) } 1 :- node(P).
1 { arch_os(P, A) : arch_os(P, A) } 1             :- node(P).
1 { arch_target(P, T) : arch_target(P, T) } 1     :- node(P).

% arch fields for pkg P are set if set to anything
arch_platform_set(P) :- arch_platform_set(P, _).
arch_os_set(P) :- arch_os_set(P, _).
arch_target_set(P) :- arch_target_set(P, _).

% avoid info warnings (see variants)
#defined arch_platform_set/2.
#defined arch_os_set/2.
#defined arch_target_set/2.

% if architecture value is set, it's the value
arch_platform(P, A) :- node(P), arch_platform_set(P, A).
arch_os(P, A) :- node(P), arch_os_set(P, A).
arch_target(P, A) :- node(P), arch_target_set(P, A).

% if no architecture is set, fall back to the default architecture value.
arch_platform(P, A) :- node(P), not arch_platform_set(P),
                       arch_platform_default(A).
arch_os(P, A)       :- node(P), not arch_os_set(P), arch_os_default(A).
arch_target(P, A)   :- node(P), not arch_target_set(P), arch_target_default(A).

% propagate platform, os, target downwards
% TODO: handle multiple dependents and arch compatibility
arch_platform_set(D, A) :- node(D), depends_on(P, D), arch_platform_set(P, A).
arch_os_set(D, A) :- node(D), depends_on(P, D), arch_os_set(P, A).
arch_target_set(D, A) :- node(D), depends_on(P, D), arch_target_set(P, A).

%-----------------------------------------------------------------------------
% Compiler semantics
%-----------------------------------------------------------------------------

% one compiler per node
1 { node_compiler(P, C) : compiler(C) } 1 :- node(P).
1 { node_compiler_version(P, C, V) : compiler_version(C, V) } 1 :- node(P).
1 { compiler_weight(P, N) : compiler_weight(P, N) } 1 :- node(P).

% dependencies imply we should try to match hard compiler constraints
% todo: look at what to do about intersecting constraints here. we'd
% ideally go with the "lowest" pref in the DAG
node_compiler_match_pref(P, C) :- node_compiler_hard(P, C).
node_compiler_match_pref(D, C)
    :- depends_on(P, D), node_compiler_match_pref(P, C),
       not node_compiler_hard(D, _).
compiler_match(P, 1) :- node_compiler(P, C), node_compiler_match_pref(P, C).

node_compiler_version_match_pref(P, C, V)
    :- node_compiler_version_hard(P, C, V).
node_compiler_version_match_pref(D, C, V)
    :- depends_on(P, D), node_compiler_version_match_pref(P, C, V),
       not node_compiler_version_hard(D, C, _).
compiler_version_match(P, 1)
    :- node_compiler_version(P, C, V),
       node_compiler_version_match_pref(P, C, V).

#defined node_compiler_hard/2.
#defined node_compiler_version_hard/3.

% compilers weighted by preference acccording to packages.yaml
compiler_weight(P, N)
    :- node_compiler(P, C), node_compiler_version(P, C, V),
       node_compiler_preference(P, C, V, N).
compiler_weight(P, N)
    :- node_compiler(P, C), node_compiler_version(P, C, V),
       not node_compiler_preference(P, C, _, _),
       default_compiler_preference(C, V, N).
compiler_weight(P, 100)
    :- node_compiler(P, C), node_compiler_version(P, C, V),
       not node_compiler_preference(P, C, _, _),
       not default_compiler_preference(C, _, _).

#defined node_compiler_preference/4.
#defined default_compiler_preference/3.

%-----------------------------------------------------------------------------
% How to optimize the spec (high to low priority)
%-----------------------------------------------------------------------------
% weight root preferences higher
%
% TODO: how best to deal with this issue?  It's not clear how best to
% weight all the constraints. Without this root preference, `spack solve
% hdf5` will pick mpich instead of openmpi, even if openmpi is the
% preferred provider, because openmpi has a version constraint on hwloc.
% It ends up choosing between settling for an old version of hwloc, or
% picking the second-best provider.  This workaround weights root
% preferences higher so that hdf5's prefs are more important, but it's
% not clear this is a general solution.  It would be nice to weight by
% distance to root, but that seems to slow down the solve a lot.
%
% One option is to make preferences hard constraints.  Or maybe we need
% to look more closely at where a constraint came from and factor that
% into our weights.  e.g., a non-default variant resulting from a version
% constraint counts like a version constraint.  Needs more thought later.
%
root(D, 2) :- root(D), node(D).
root(D, 1) :- not root(D), node(D).

% prefer default variants
#minimize { N*R@5,P,V,X : variant_not_default(P, V, X, N), root(P, R) }.

% pick most preferred virtual providers
#minimize{ N*R@4,D : provider_weight(D, N), root(P, R) }.

% prefer more recent versions.
#minimize{ N@3,P,V : version_weight(P, V, N) }.

% compiler preferences
#maximize{ N@2,P : compiler_match(P, N) }.
#minimize{ N@1,P : compiler_weight(P, N) }.
