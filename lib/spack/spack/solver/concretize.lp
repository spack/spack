%=============================================================================
% Generate
%=============================================================================
% One version, arch, etc. per package
{ version(P, V) : version(P, V)} = 1              :- node(P).
{ arch_platform(P, A) : arch_platform(P, A) } = 1 :- node(P).
{ arch_os(P, A) : arch_os(P, A) } = 1             :- node(P).
{ arch_target(P, T) : arch_target(P, T) } = 1     :- node(P).

% one variant value for single-valued variants.
{ variant_value(P, V, X) : variant_value(P, V, X) } = 1
    :- node(P), variant(P, V), not variant_single_value(P, V).

%=============================================================================
% Define
%=============================================================================
% dependencies imply new nodes.
node(D) :- node(P), depends_on(P, D).

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------

% if a variant is set to anything, it is considered 'set'.
variant_set(P, V) :- variant_set(P, V, _).

% suppress wranings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant_set/3.

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(P, V, X) :- node(P), variant(P, V), variant_set(P, V, X).
variant_value(P, V, X) :- node(P), variant(P, V), not variant_set(P, V),
                 variant_default_value(P, V, X).

%-----------------------------------------------------------------------------
% Architecture semantics
%-----------------------------------------------------------------------------

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
